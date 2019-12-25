# Change these
MARKET = "TBC"
LEASEPOLLER_IP = "192.168.83.22"
LEASEPOLLER_PORT = 3882


# Defaults should be good for most use cases
TIMEOUT = 60
MAX_MAP_SIZE = 40000
TIMEOUT_INTERVAL = 10
OBJECTNAME = "/NetObjects/LeasePollerDamped" # You need to create this NetObject in the PRE
class Trigger(FirewallTrigger):
	def __init__(self):
		import socket
		import packetlogic2
		FirewallTrigger.__init__(self) # don't forget this!
		self.ipMap = {}
		self.lastTimeout = 0
		self.addr = (LEASEPOLLER_IP, LEASEPOLLER_PORT)
		self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.dampObj = self.pldb.object_get(OBJECTNAME)
		print "You need to see this in the log to know that I am working..."
		if self.dampObj is None:
			 print "!!!!! You need to create: %s" % OBJECTNAME
        # Purge existing dyns
		pl = packetlogic2.connect('127.0.0.1','packetlogicd','secret2')
		pldd = pl.Realtime()
		cleanlist = pldd.dyn_list_no(self.dampObj.id)
		print "Purging %i IPs" % (len(cleanlist))
		for k in cleanlist:
			pldd.dyn_remove(self.dampObj.id, k[1])
		pldd.close()
	
	def trigger(self):
		import time
		currentTime = int(time.time())
		if self.ipMap.get(self.client_ip, None) is None:
			if(len(self.ipMap) > MAX_MAP_SIZE):
				print "ipMap size is above threshold: %i, will not send request." % (MAX_MAP_SIZE)
             		else:
				self.ipMap[self.client_ip] = currentTime
				self.pld.dyn_add(self.dampObj.id, self.client_ip)
				print "Send to Poller %s" %self.client_ip
				self.sendToPoller(self.client_ip)


			if self.lastTimeout < currentTime-TIMEOUT_INTERVAL:
				delQueue = []
				for (ip, times) in self.ipMap.iteritems():
					if times < currentTime-TIMEOUT:
						delQueue.append(ip)

				print "Timing out: %i entries out of: %i" % (len(delQueue),len(self.ipMap))
				for ip in delQueue:
 					del self.ipMap[ip]
				self.pld.dyn_remove(self.dampObj.id, ip)
			self.lastTimeout = currentTime
	
	def sendToPoller(self, ip):
		self.udpSock.sendto("%s:%s" % (MARKET, ip), self.addr)

