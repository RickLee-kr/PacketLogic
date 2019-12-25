"""
Host based P2P identification filtering rule trigger.
Apply on all confirmed P2P traffic, such as BT tracker or normal non-encrypted BT.
Version 0.1
"""

# Defaults should be good for most
TIMEOUT = 1800
MAX_MAP_SIZE = 500000
TIMEOUT_INTERVAL = 10
OBJECTNAME = "/NetObjects/du/P2P/Current P2P Users" # You need to manually create this


class Trigger(FirewallTrigger):
    def __init__(self):
        import socket
        import packetlogic2
        import time
        
        FirewallTrigger.__init__(self) # don't forget this!'
        self.ipMap = {}
        self.lastTimeout = 0
        self.myTime = time

        self.obj = self.pldb.object_get(OBJECTNAME)
        if self.obj is None:
            print "!!!!! You need to create: %s" % OBJECTNAME

        print "Starting P2P unknown host trigger"
        pl = packetlogic2.connect('127.0.0.1','packetlogicd','secret2')
        pldd = pl.Realtime()
        
        cleanlist = pldd.dyn_list_no(self.obj.id)
        print "Purging %i IPs" % (len(cleanlist))
        for k in cleanlist:
         pldd.dyn_remove(self.obj.id, k[1])
        pldd.close()

    def trigger(self):
         currentTime = int(self.myTime.time())
         
         if self.ipMap.get(self.client_ip, None) is None:
             if(len(self.ipMap) > MAX_MAP_SIZE):
                 print "P2P ipMap size is above threshold: %i" % (MAX_MAP_SIZE)
             else:
                 self.ipMap[self.client_ip] = currentTime
                 self.pld.dyn_add(self.obj.id, self.client_ip)
         else:
             self.ipMap[self.client_ip] = currentTime

         if self.lastTimeout < currentTime-TIMEOUT_INTERVAL:
             delQueue = []
             for (ip, times) in self.ipMap.iteritems():
                 if times < currentTime-TIMEOUT:
                     delQueue.append(ip)
             if len(delQueue) > 0:
                 print "Timing out: %i entries out of: %i" % (len(delQueue), len(self.ipMap))
                 for ip in delQueue:
                     del self.ipMap[ip]
                     self.pld.dyn_remove(self.obj.id, ip)
                     
             self.lastTimeout = currentTime
