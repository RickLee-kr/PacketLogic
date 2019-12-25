#!/usr/bin/python

import sys
import errno
import optparse
import psmcdr
try:
       import json
except ImportError:
       import simplejson as json

parser = optparse.OptionParser("usage: %prog <filename>")

options, args = parser.parse_args()
if len(args) != 1:
	parse.error('Invalid number of parameters.')

data = open(args[0],'r').read()
result = psmcdr.parseCdrs(data)
print json.dumps(result, sort_keys=True, indent=4)
