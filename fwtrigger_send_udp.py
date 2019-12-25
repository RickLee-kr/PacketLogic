import socket

PSM_IP = '192.168.2.3'
PSM_PORT = 3996

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Trigger(FirewallTrigger):
    def trigger(self):
        #self.name
        #self.server_ip
        #self.server_port
        #self.client_ip
        #self.client_port
        #self.protocol
        #self.flags
        #self.client_is_local
        #self.server_is_local
        #self.untracked
        #self.flowsync
        #self.established

        local_ip = self.client_ip
        if self.server_is_local:
            local_ip = self.server_ip

        message = '{"sessionId": "%s"}' % local_ip
        sock.sendto(message, (PSM_IP, PSM_PORT))
