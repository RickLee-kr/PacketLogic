#!/bin/env/python

"""
A simple script to generate json set commands, from an csv file

Usage:

if the CSV file (test.csv) looks like:

subscriberId,plan
12345,testplan

then run it as:

python parseCSVfile.py test.csv > psmCommands.json

and then push them to PSM using:

cat psmCommands.json | nc <IP TO PSM> <JSON RPC PORT>

set PSM_RESPONSE to True to get reply from PSM for each command (not recommended if you are sending lots of commands)
"""

import csv
import sys
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("parser")

if not len(sys.argv) == 2:
    sys.exit("Must pass CSVfile as argument")

infile = sys.argv[1]
logging.info("Parsing file: %s", infile)

PSM_RESPONSE = False

c = 0
with open(infile, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',') # set quotechar='"' if values are quoted
    for row in reader:
        if not row:
            continue
        c += 1
        aid = row['subscriberId']
        plan = row['plan']

        logger.info("Got: %s, %s", aid, plan)

        cmd = {
            "method": "object.set",
            "params": [
                "subscriber",
                "%s" % aid,
                {
                    "plan": "%s" % plan
                }
            ]
        }

        if PSM_RESPONSE:
            cmd['id'] = c

        print json.dumps(cmd)

logger.info("Done, processed %d rows", c)