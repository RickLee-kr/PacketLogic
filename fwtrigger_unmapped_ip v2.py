import socket
import struct

JSON_IP = "58.123.218.55"
JSON_PORT = 3996

class Trigger(FirewallTrigger):

    def connectToPSM(self):
        self.psmSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.psmSock.connect((JSON_IP, JSON_PORT))

    def sendToPSM(self, data):
        try:
            if self.psmSock.send(data + "\n") <= 0:
                self.connectToPSM()
        except:
            self.connectToPSM()

    def __init__(self):
        #self.connectToPSM()
        FirewallTrigger.__init__(self)

    def trigger(self):
        localIP = ""
        fakeBillingId = 0

        if self.client_is_local:
            localIP = self.client_ip
        else:
            localIP = self.server_ip

        if localIP.startswith("39.122.") or localIP.startswith("39.123.") or localIP.startswith("39.124.") or localIP.startswith("39.125.") or localIP.startswith("39.127."):
            fakeBillingId = struct.unpack("!L", socket.inet_aton(localIP))[0]

        if fakeBillingId != 0:
            jsonData = '{"BILLINGID":"%d","IP":"%s","LEASETIME":3600}' % (fakeBillingId, localIP)
            self.sendToPSM(jsonData)
            #print "fakeBillingId %d ip %s" % (fakeBillingId, localIP)
