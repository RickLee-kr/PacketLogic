#!/usr/bin/env python

import packetlogic2
import sys
import string
import time
import datetime
import optparse
from operator import itemgetter

p = optparse.OptionParser(description="Statistics Retriever")
p.add_option("-s", "--start", dest="start", help="Start of search period")
p.add_option("-e", "--end", dest="end", help="End of search period")
p.add_option("-p", "--path", dest="path", help="Statistics Path")


(opt, args) = p.parse_args()

opt.path= "%s"%opt.path

pl = packetlogic2.connect("127.0.0.1", "admin", "pldemo11")
s = pl.Statistics()
hosts = []

t1 = datetime.datetime.strptime(opt.start, '%Y-%m-%d %H:%M:%S')
t3 = datetime.datetime.strptime(opt.end, '%Y-%m-%d %H:%M:%S')

def GetPathTypeStr(pathType):
    if pathType == s.VALUETYPE_DUMMY:
        return "Statistics Object"
    elif pathType == s.VALUETYPE_NETOBJECT:
        return "NetObject"
    elif pathType == s.VALUETYPE_HOST:
        return "Local Host"
    elif pathType == s.VALUETYPE_SERVOBJECT:
        return "ServiceObject"
    elif pathType == s.VALUETYPE_SERVICE:
        return "Service"
    else:
        return pathType


pathPrefix = opt.path
startTime = opt.start
endTime = opt.end
if pathPrefix != "/":
    pathPrefix = opt.path + "/"



for d in s.list(startTime, endTime, pathPrefix):
    #print d
    hosts.append((d['values']['bytes in'] + d['values']['bytes out'], d['name']))

print "%s %d" % (startTime, len(hosts))