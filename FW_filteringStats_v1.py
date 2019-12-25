import socket
import json

PSM_IP = '172.23.144.84'
PSM_PORT = 3996

addr = (PSM_IP, PSM_PORT)


class Trigger(FirewallTrigger):
    def __init__(self):
        FirewallTrigger.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
        try:
            data = {
                'sessionId': self.client_ip,
                'serverHostname': self.server_hostname,
                'ruleName': self.name
            }
            self.sock.sendto(json.dumps(data), addr)
        except Exception, e:
            print str(e)
            raise e
