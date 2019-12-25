import packetlogic2
import time
import sys

# host IP address
host=sys.argv[1]

pl=packetlogic2.connect("v13.1.demo.proceranetworks.com","admin","pldemo00")
rt=pl.Realtime()

def cb(ip, connections):
    print "=" * 30
    print time.ctime()
    print ip
    if connections is None:
        print "Host removed"
        rt.stop_updating()
    else:
        services = {}
        for c in connections:
            #print c.base_service
            #print c.service
            if c.service not in services:
                services[c.service] = []
            services[c.service].append(c)

        for s,cs in services.iteritems():
            totin = totout = 0
            for c in cs:
                totin += c.speed[0]
                totout += c.speed[1]
                print " * %s in=%dbps out=%dbps" % (s, totin, totout)
            for c in cs:
                f = "   - "
                f += "%s:%d" % c.client
                f += "->%s:%d" % c.server
                if c.server_hostname:
                    f += "[%r]" % c.server_hostname
                f += " in=%dbps out=%dbps" % c.speed
                if c.shaping_rules:
                    f += " prio=%d rules=" % c.shaping_prio
                    f += ",".join(c.shaping_rules)
                # assume synced clocks
                f += " age=%ss" % int(time.time()-c.starttime)
                print f

rt.add_host_callback(host, cb)
rt.update_forever(5.0)
print "Done I guess"
