PSM_IP = "37.152.5.67"
PSM_PORT = 3995
VERBOSE = False
 
class Trigger(HostTrigger):
    def __init__(self):
        import socket
        HostTrigger.__init__(self) # don't forget this!'
        self.addr = (PSM_IP, PSM_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
    def trigger(self):
        self.sendToPSM(self.ip)
 
    def sendToPSM(self, ip):
        template = '{"sessionIp": "%s","tethering": "true"}'
        encoded = template % ip
        if VERBOSE:
            print "Sending message to PSM (%s): '%s'" % (PSM_IP, encoded)
        self.udpSock.sendto(encoded, self.addr)
 
    def reset(self):
        if VERBOSE:
            print "%s not matching '%s' anymore" % (self.ip, self.name)