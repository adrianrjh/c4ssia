from pysnmp.hlapi import *

def get_oids(ip_address):
    community = "YAA-INTERNET"
    oid = "1.3.6.1.6.3.15"

    errorIndication, errorStatus, errorIndex, varBinds = \
        getCmd(SnmpEngine(), CommunityData(community), UdpTransportTarget(ip_address, 161), ObjectType(oid), bulk=True)

    if errorIndication:
        print(errorIndication)
        return

    if errorStatus:
        print("Error: %s at %s" % (errorStatus.prettyPrint(), errorIndex))
        return

    for varBind in varBinds:
        print(varBind)

get_oids("10.0.10.2")