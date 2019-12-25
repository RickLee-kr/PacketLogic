import socket
import json

PSM_IP_1 = '172.23.144.83'
PSM_IP_2 = '172.23.144.84'
PSM_PORT = 3997

addr1 = (PSM_IP_1, PSM_PORT)
addr2 = (PSM_IP_2, PSM_PORT)

class Trigger(FirewallTrigger):
    def __init__(self):
        FirewallTrigger.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
        try:
            data = {
                'sessionId': self.client_ip,
                'trigger': 'tetheringServ'
            }
            self.sock.sendto(json.dumps(data), addr1)
            self.sock.sendto(json.dumps(data), addr2)
        except Exception, e:
            print str(e)
            raise e
