SQSD_IP = "1.235.126.133"
SQSD_PORT = 5050

MAX_MAP_SIZE = 30000
TIMEOUT = 10
TIMEOUT_INTERVAL = 10

class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
        
        FirewallTrigger.__init__(self)

        self.ipMap = {}
        self.lastTimeout = 0
        self.sqsd_addr = (SQSD_IP, SQSD_PORT)
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self):
        import time
        currentTime = int(time.time())

        if self.ipMap.get(self.client_ip, None) is None:
            if(len(self.ipMap) > MAX_MAP_SIZE):
                print "SQSD: ipMap size is above threshold %i, will not send request." % (MAX_MAP_SIZE)
            else:
                self.ipMap[self.client_ip] = currentTime
                self.sendToSQSD(self.client_ip)

        if self.lastTimeout < currentTime-TIMEOUT_INTERVAL:
            delQueue = []

            for (ip, times) in self.ipMap.iteritems():
                if times < currentTime-TIMEOUT:
                    delQueue.append(ip)

            print "SQSD: timing out %i entries out of %i" % (len(delQueue), len(self.ipMap))

            for ip in delQueue:
                del self.ipMap[ip]

            self.lastTimeout = currentTime

    def sendToSQSD(self, ip):
        msg = ip + '!'
        #print "SQSD Message: %s" % str(msg)
        self.udpSock.sendto(msg, self.sqsd_addr)
