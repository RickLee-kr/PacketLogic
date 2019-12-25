"""
Send a message to the PSM with Client IP and Device Name/Category based on rule name
"""

PSM_IPS = ["210.94.2.219"]
PSM_PORT = 3995

class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
        
        FirewallTrigger.__init__(self)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def trigger(self):
        on = self.name.replace("Device Trigger: ","")
        deviceinfo = on.split(',')
        
        self.sendToPsm(on)
        
    def sendToPsm(self, category):
        import json
        
        data = {}
        data["ipaddr"] = self.client_ip
        data["devicename"] = category
            
        for psmIp in PSM_IPS:
            self.udpSock.sendto(json.dumps(data), (psmIp, PSM_PORT))
