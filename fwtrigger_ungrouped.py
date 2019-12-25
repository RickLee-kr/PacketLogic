PSM_IPS = ["94.25.209.164"]
PSM_PORT = 3996

class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
        
        FirewallTrigger.__init__(self)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def trigger(self):
        on = self.name.replace("Unknown Trigger: ","")
        self.sendToPsm(on)
        
    def sendToPsm(self, category):
        import json
        
        data = {}
        data["ipaddr"] = self.client_ip
            
        for psmIp in PSM_IPS:
            self.udpSock.sendto(json.dumps(data), (psmIp, PSM_PORT))