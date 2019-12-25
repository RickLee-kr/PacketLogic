"""
Adds the host to OBJECTNAME and sends an SNMP Trap
"""
OBJECTNAME = "/NetObjects/HostTrigger/CPS"

from simpletrap import trapGenerator

class Trigger(HostTrigger):
    # Trigger for Matching 
    def trigger(self):
        obj = self.pldb.object_get(OBJECTNAME)
        if obj is None:
            print "Couldn't find object '%s'" % OBJECTNAME
            return
        self.pld.dyn_add(obj.id, self.ip)

        print "%s is matching trigger '%s' - added to '%s'" % (self.ip, self.name, OBJECTNAME)

        # Begin SNMP
        # an explicit manager and community can be specified in the
        # call below to have it use something else than the
        # system-wide configured values.
        # i.e  manager="192.168.1.250", community="mytraps"
        err = trapGenerator.send(trapoid=('PACKETLOGIC-MIB', 'pl2TrapGenericMsg'),
                                 vars=[('PACKETLOGIC-MIB',
                                        'pl2TrapMessage',
                                        '%s matching hosttrigger' % self.ip)])
        
        if err is False:
            print 'No manager defined, did not send trap.'
        elif err is not None:
            print 'Failed to send trap to manager', err

    # Trigger for Non-Matching
    def reset(self):
        obj = self.pldb.object_get(OBJECTNAME)
        if obj is None:
            return
        self.pld.dyn_remove(obj.id, self.ip)
        print "%s removed from '%s' matching rule '%s' " % (self.ip, OBJECTNAME, self.name)
        # Begin SNMP 
        err = trapGenerator.send(trapoid=('PACKETLOGIC-MIB', 'pl2TrapGenericMsg'),
                                 vars=[('PACKETLOGIC-MIB',
                                        'pl2TrapMessage',
                                        '%s cleared from hosttrigger' % self.ip)])
        
        if err is False:
            print 'No manager defined, did not send trap.'
        elif err is not None:
            print 'Failed to send trap to manager', err