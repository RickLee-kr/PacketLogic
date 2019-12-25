#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import packetlogic2
import ConfigParser
import time
import operator
from operator import itemgetter

config = ConfigParser.ConfigParser()
config.read("config.ini")
pre_ip = config.get('MAIN','pre_ip')
pluser = config.get('MAIN','username')
plpass = config.get('MAIN','password')
filename = config.get('Stat','filename')
startdate = config.get('Stat','startdate')
enddate = config.get('Stat','enddate')
path = config.get('Stat','path')

# Connect to PacketLogic
try:
    pl = packetlogic2.connect(pre_ip, pluser, plpass)
    r = pl.Ruleset()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)
    
s = pl.Statistics()
hosts = []

print "---------------------------------------------------"
print "---------------------------------------------------"

    
for d in s.list(startdate, enddate, path):
    #print d
    hosts.append((d['values']['bytes in'] + d['values']['bytes out'], d['name']))

print "There was %d different IP Groups recorded active between %s and %s" % (len(hosts), startdate, enddate)