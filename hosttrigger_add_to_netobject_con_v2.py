"""
Adds the host to OBJECTNAME

"""
OBJECTNAME = "/NetObjects/HostTrigger/Congested"
TIMEOUT_INTERVAL = 30

class Trigger(HostTrigger):

	def __init__(self):
		import time
		self.lastTimeout = 0
		print "Hey there! I am using Congestion Detection for Dummies"
		
	def trigger(self):
			obj = self.pldb.object_get(OBJECTNAME)
			if obj is None:
				print "Couldn't find object '%s'" % OBJECTNAME
				return
			self.pld.dyn_add(obj.id, self.ip)
			print "Add '%s' to Congested" % self.ip

	def reset(self):
			obj = self.pldb.object_get(OBJECTNAME)
			if obj is None:
				return
			self.pld.dyn_remove(obj.id, self.ip)
			print "Remove '%s' from Congested" % self.ip
