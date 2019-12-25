import socket
import struct

JSON_IP = "210.94.2.219"
JSON_PORT = 1235

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
        localIP=str(self.client_ip)
        rawIP = socket.inet_aton(self.client_ip)
        fakeBillingId = struct.unpack("!L", rawIP)[0]


        if localIP.startswith("2001:"):
            jsonData = '{"msisdn":"%d","ip":"%s","rat":"SKT","tier":"SKT","cellId":"nodebSKTIPv6"}' % (fakeBillingId, self.client_ip) 
            print jsonData
            self.sendToPSM(jsonData)
        
        else: