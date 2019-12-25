#!/usr/bin/python

import packetlogic2
import struct
import socket

pl = packetlogic2.connect("x.x.x.x", "admin", "pldemo00")

rt = pl.Realtime()

bgp = rt.dump_bgptable()

aspaths = dict(bgp[1])

def ntoa(x):
    return socket.inet_ntoa(struct.pack('!I', x))

print "%15s/mask\tAS Path"
for data in bgp[0]:
    aspath = ", ".join([ "%s" % (x,) for x in aspaths[data[3]] ])
    print "%15s/%2d  \t%s" % (ntoa(data[1]), data[2], aspath)