import packetlogic2
import time
import datetime
import sys

pl = packetlogic2.connect("10.0.23.243", "admin", "pldemo11")

def repeatedly_print_value(z, v):
    z.refresh()
    if v.type == z.TYPE_MOMENT:
        for x in v.values():
            mints = datetime.datetime.fromtimestamp(x.min_tstamp-32400)
            maxts = datetime.datetime.fromtimestamp(x.max_tstamp-32400)
            for i in x.level:
                str = i.replace(',','-')
                sys.stdout.write(str+'/')
            print ",%d,%d,%d,%d,%s,%s" % (x.value, x.rate, x.min, x.max, mints, maxts)
    elif v.type == z.TYPE_SPEED:
        for x in v.values():
            mints = datetime.datetime.fromtimestamp(x.min_tstamp-32400)
            maxts = datetime.datetime.fromtimestamp(x.max_tstamp-32400)
            for i in x.level:
                str = i.replace(',','-')
                sys.stdout.write(str+'/')
            print ",%d,%d,%d,%d,%s,%s" % (x.value, x.rate*8, x.min*8, x.max*8, mints, maxts)
    else:
        for x in v.values():
            mints = datetime.datetime.fromtimestamp(x.min_tstamp-32400)
            maxts = datetime.datetime.fromtimestamp(x.max_tstamp-32400)
            for i in x.level:
                str = i.replace(',','-')
                sys.stdout.write(str+'/')
            print ",%d,0,%d,%d,%s,%s" % (x.value, x.min, x.max, mints, maxts)

sd = pl.SysDiag()
zones = sd.zone_list()

for key,zone in zones.iteritems():
    print zone.name,",Value,Rate,Minimum,Maximum,Min Timestamp, Max Timestamp"
    for _,val in zone.valuedefs.iteritems():
        repeatedly_print_value(zone, val)
    print
