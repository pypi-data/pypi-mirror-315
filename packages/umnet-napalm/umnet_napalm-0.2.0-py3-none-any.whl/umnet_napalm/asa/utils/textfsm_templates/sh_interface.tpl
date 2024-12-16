Value INTERFACE (\S+)
Value IFNAME (\S*)
Value ADMIN_STATE (up|down|administratively down)
Value OPER_STATE (up|down)
Value MAC (\w{4}.\w{4}.\w{4})
Value MTU (\d+)
Value IP (\d+.\d+.\d+.\d+)
Value NETMASK (\d+.\d+.\d+.\d+)


Start
 ^Interface ${INTERFACE} "${IFNAME}", is ${ADMIN_STATE}, line protocol is ${OPER_STATE}
 ^\s+MAC address ${MAC}, MTU ${MTU}
 ^\s+IP address ${IP}, subnet mask ${NETMASK} -> Record

EOF