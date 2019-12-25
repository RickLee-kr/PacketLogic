# Firewall trigger for setting one_redirect_done attribute to TRUE based on redirect firewall trigger.
PSMTRIGGER_IP_1 = "172.25.2.17"
PSMTRIGGER_PORT = 3872
 
 
class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
  
        FirewallTrigger.__init__(self) # don't forget this!'
        self.addr1 = (PSMTRIGGER_IP_1, PSMTRIGGER_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
 
    def trigger(self):
        self.sendToPoller(self.client_ip, "one_redirect_done", "true")
 
 
    def sendToPoller(self, ip, attribute, value):
        data = "%s:%s=%s" % (ip,attribute,value)
        self.udpSock.sendto(data, self.addr1)