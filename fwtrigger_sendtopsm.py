"""
Send IP address with /48 prefix to PSM for provisioning
"""


PSM_IP = "153.128.77.213"
PSM_PORT = 3997

TEMPLATE6 = '{"ip":"%s/48"}\n'
TEMPLATE4 = '{"ip":"%s/32"}\n'

class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
        FirewallTrigger.__init__(self)
        self.addr = (PSM_IP, PSM_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
	if self.client_is_local:
	        self.sendToPSM(self.client_ip)
	elif self.server_is_local:
	        self.sendToPSM(self.server_ip)

    def sendToPSM(self, ip):
	if ":" in ip:
	        self.udpSock.sendto(TEMPLATE6 % ip, self.addr)
	else:
	        self.udpSock.sendto(TEMPLATE4 % ip, self.addr)
