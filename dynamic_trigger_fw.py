
import socket

DST_IP = "172.21.21.113"
DST_PORT = 3020


class Trigger(FirewallTrigger):
    def __init__(self):
        FirewallTrigger.__init__(self)

        self.dst = (DST_IP, DST_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
        msg = '{"ip": "%s", "hostname": "%s"}' % (self.client_ip, socket.gethostname())
        self.udpSock.sendto(msg, self.dst)