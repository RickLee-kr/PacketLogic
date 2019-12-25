import packetlogic2

"""
Adds the host to OBJECTNAME

"""
OBJECTNAME = "/NetObjects/DDoS_Attacked"

host = '127.0.0.1'
user = 'admin'
pwd = 'pldemo000'

class Trigger(HostTrigger):
    def trigger(self):
        print ("The Trigger '%s' matching: %s" % (self.name, self.ip))
        obj = self.pldb.object_get(OBJECTNAME)
        if obj is None:
            print "Couldn't find object '%s'" % OBJECTNAME
            return
        try:
            pl = packetlogic2.connect(host, user, pwd)
        except Exception, e:
            print "Error: Couldn't connect to PRE " + str(e)
            return
        rt = pl.Realtime()
        rt.dyn_add(obj.id, self.ip)