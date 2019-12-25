#!/usr/bin/env python

import packetlogic2
import sys
import string
import datetime

pl = packetlogic2.connect("192.168.194.225", "admin", "pldemo00")
c = pl.Config()

for i in xrange(1,10):
    cfgKey = "SHUNT_IPV4_EXTRA" + str(i)
    c.set(key=cfgKey, value="")

c.commit()
