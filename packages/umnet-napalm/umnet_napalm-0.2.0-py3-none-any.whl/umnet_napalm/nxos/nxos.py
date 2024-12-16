from typing import List
import re
import logging

from napalm.nxos_ssh import NXOSSSHDriver
from napalm.base.helpers import textfsm_extractor
from napalm.base.models import FactsDict

from ..base import UMnetNapalmError, UMnetNapalm
from ..models import RouteDict, MPLSDict, IPInterfaceDict, VNIDict, InventoryDict
from ..utils import abbr_interface

logger = logging.getLogger(__name__)


class NXOS(UMnetNapalm, NXOSSSHDriver):
    """
    NXOS Parser
    """

    LABEL_VALUE_MAP = {
        "No": [],
        "Pop": ["pop"],
    }

    # for nexus we're going to map the 'description' provided by
    # show inventory to the type
    INVENTORY_TO_TYPE = {
        # note we're using the fact that this dict gets evaluated
        # sequentially
        r"Fabric Module$": "fabric_module",
        r"Supervisor Module$": "re",
        r"Fan Module$": "fan",
        r"Module$": "linecard",
        r"Power Supply$": "psu",
        r"^Transceiver": "optic",
        # don't care about chassis or system controller types
        r"Chassis": None,
        r"System Controller": None,
    }


    def _get_nxos_inventory_type(self, name: str, desc: str) -> str:
        """
        Figures out the inventory type based on the 'name' and 'desc'
        fields from 'show inventory all'
        """

        # the description field is all over the place for 3rd party
        # optics, so we want to rely on the 'name' field, which
        # is always the interface name
        if name.startswith("Ethernet"):
            return "optic"

        # otherwise we want to figure this out based on description
        return self._get_inventory_type(desc)

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses 'sh ip route detail vrf all'
        """

        parsed_routes = []

        raw_routes = self._send_command("show ip route detail vrf all")
        routes = textfsm_extractor(self, "sh_ip_route_detail_vrf_all", raw_routes)

        for route in routes:
            # skip 'broadcast' and 'local' routes, we don't really care about these
            if route["protocol"] in ["broadcast", "local"]:
                continue

            # "learned from" is one of the keys in our route table that determines
            # uniqueness, as such we need to make sure it's set. Usually it's
            # the IP of the advertising router, but for local/direct/static it should
            # get set to 'self'
            if route["nh_ip"]:
                learned_from = route["nh_ip"]
            elif route["protocol"] in ["direct", "local", "vrrp", "static"]:
                learned_from = "self"
            else:
                raise UMnetNapalmError(f"Could not determine learned from for {route}")

            parsed_routes.append(
                {
                    "vrf": route["vrf"],
                    "prefix": route["prefix"],
                    "nh_interface": route["nh_interface"],
                    "learned_from": learned_from,
                    "protocol": route["protocol"],
                    "age": route["age"],
                    "nh_ip": route["nh_ip"],
                    "mpls_label": [route["label"]] if route["label"] else [],
                    "vxlan_vni": int(route["vni"]) if route["vni"] else None,
                    "vxlan_endpoint": route["nh_ip"],
                    "nh_table": (
                        "default" if route["label"] or route["vni"] else route["vrf"]
                    ),
                }
            )

        return parsed_routes

    def get_facts(self) -> FactsDict:
        """
        Cleans up model number on napalm get_facts
        """

        results = super().get_facts()

        model = results["model"]
        m = re.match(r"Nexus(3|9)\d+ (\S+) (\(\d Slot\) )*Chassis$", model)

        # some models have the "N9K" or "N3K already in them, some don't.
        if m and re.match(r"N\dK", m.group(2)):
            results["model"] = m.group(2)
        elif m:
            results["model"] = f"N{m.group(1)}K-{m.group(2)}"

        return results

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        parses show mpls into a dict that outputs
        aggregate labels and
        """
        output = []

        raw_entries = self._send_command("show mpls switching detail")
        entries = textfsm_extractor(self, "sh_mpls_switching_detail", raw_entries)

        for entry in entries:
            # for aggregate labels the next hop is the VRF
            nh_interface = entry["vrf"] if entry["vrf"] else entry["nh_interface"]
            output.append(
                {
                    "in_label": entry["in_label"],
                    "out_label": self._parse_label_value(entry["out_label"]),
                    "fec": entry["fec"] if entry["fec"] else None,
                    "nh_ip": entry["nh_ip"],
                    "nh_interface": nh_interface,
                    "rd": entry["rd"],
                    "aggregate": bool(entry["vrf"]),
                }
            )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        Parses "show inventory"
        """
        raw_inventory = self._send_command("show inventory all")
        inventory = textfsm_extractor(self, "sh_inventory_all", raw_inventory)

        output = []
        for entry in inventory:

            # removing quotes from name and description fields,
            # which are enquoted for certain types
            for key in ["name", "desc"]:
                entry[key] = entry[key].replace('"', "")

            inventory_type = self._get_nxos_inventory_type(entry["name"], entry["desc"])
            if not inventory_type:
                continue

            # if this is a linecard in slot 1 and the model number
            # doesn't look like a linecard, then this is a fixed config device
            # and the "lincard" is really the chassis and we want to ingore it
            if (
                inventory_type == "linecard"
                and entry["name"] == "Slot 1"
                and re.match(r"N[39]K-C", entry["pid"])
            ):
                continue

            output.append(
                {
                    "type": inventory_type,
                    "name": entry["name"],
                    "part_number": entry["pid"],
                    "serial_number": entry["sn"],
                    "parent": None,
                }
            )

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        output = []

        # NOTE: because "get_interfaces" currently has a bug for loopback and mgmt IPs on Nexus,
        # we're going to do our own parsing. WE can actually get everything we need
        # with a combination of "show ip int vrf all" and the napalm get_interfaces
        # function
        raw_interfaces = self._send_command("show ip interface vrf all")
        ip_interfaces = textfsm_extractor(
            self, "sh_ip_interface_vrf_all", raw_interfaces
        )
        phy_interfaces = super().get_interfaces()

        for i in ip_interfaces:
            # some l3 interfaces don't have IP addresses (like EVPN L3VPN vrf SVIs)
            # we want to skip those.
            if not i["ip_address"]:
                continue
            phy_i = phy_interfaces.get(i["interface"], {})
            output.append(
                {
                    "ip_address": f'{i["ip_address"]}/{i["prefixlen"]}',
                    "interface": abbr_interface(i["interface"]),
                    "description": phy_i.get("description", ""),
                    "mtu": int(i["mtu"]),
                    "admin_up": (i["admin_state"] == "admin-up"),
                    "oper_up": (i["protocol_state"] == "protocol-up"),
                    "vrf": i["vrf"],
                }
            )

        return output

    def get_vni_information(self) -> List[VNIDict]:
        """
        Runs "show nve vni" to get vni info
        """
        output = []
        raw_vnis = self._send_command("show nve vni")
        vnis = textfsm_extractor(self, "sh_nve_vni", raw_vnis)

        for vni in vnis:

            output.append(
                {
                    "vni": vni["vni"],
                    "mcast_group": (
                        None
                        if vni["mcast_grp"] == "n/a"
                        else vni["mcast_grp"]
                    ),
                    "vrf": vni["bd_vrf"] if vni["type"] == "L3" else None,
                    "vlan_id": (
                        vni["bd_vrf"]
                        if vni["type"] == "L2" and vni["bd_vrf"] != "UC"
                        else None
                    ),
                },
            )

        return output
