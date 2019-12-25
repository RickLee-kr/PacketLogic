#!/usr/bin/env python
""" 
Script to export statistics data to CSV format.

Example:

If "name1" and "name2" are nodes under the specified path and 4
datapoints are requested the output would look like the following:

name1 (inbound),123,321,12,143
name1 (outbound),111,222,111,222
name2 (inbound),311,623,135,623
name2 (outbound),523,31,25,14

stats_csv_export.py -d 4 -H 192.168.1.25 -U admin -P pldemo00 -s 2006-05-09 /NetObjects/Users

"""

__version__ = "2.1 2006-08-19 Procera"

###############################################################################
#
#                          NO WARRANTY
#
#  BECAUSE THE PROGRAM IS PROVIDED FREE OF CHARGE, THERE IS NO WARRANTY
#  FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
#  OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
#  PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
#  OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
#  TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
#  PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
#  REPAIR OR CORRECTION.
#
#  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
#  WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
#  REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
#  INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
#  OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
#  TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
#  YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
#  PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGES.
#
###############################################################################

import sys
import os
import getopt
import packetlogic2

CMD_NAME = os.path.basename(sys.argv[0])

def error(message):
    print "%s: %s" % (CMD_NAME, message)
    print "Try `%s --help' for more information." % (CMD_NAME)
    sys.exit(1)

def usage():
    print """Usage: %s [OPTION] -H hostname -U username -P password -s startdate PATHS...

    Exports statistics data for PATHS into CSV format.

    -H, --hostname   Hostname of PacketLogic
    -U, --username   Username to connect with
    -P, --password   Password for user

    -s, --startdate  First date to include in exported data (YYYY-MM-DD)
    -e, --enddate    Last date to include in exportded data (YYYY-MM-DD) (default=startdate)

    -c, --count      Number of entries to include, 0 for all (default 0)
    -d, --datapoints Number of datapoints to include for each entry (default 24)

    -h, --help       Display this help and exit

    """ % CMD_NAME

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "hH:U:P:s:e:c:d:", ["help", "hostname=", "username=", "password=", "startdate=", "enddate=", "count=", "datapoints="])
except getopt.GetoptError, (msg, opt):
    error(msg)

hostname = None
username = None
password = None
startdate = None
enddate = None
count = 0
datapoints = 24

for option, argument in opts:
    if option in ("-h", "--help"):
        usage()
        sys.exit(0)
    if option in ("-H", "--hostname"):
        hostname = argument
    if option in ("-U", "--username"):
        username = argument
    if option in ("-P", "--password"):
        password = argument
    if option in ("-s", "--startdate"):
        startdate = argument
    if option in ("-e", "--enddate"):
        enddate = argument
    if option in ("-c", "--count"):
        count = int(argument)
    if option in ("-d", "--datapoints"):
        datapoints = int(argument)

# check for mandatory arguments
if hostname is None:
    error("missing hostname argument")
if username is None:
    error("missing username argument")
if password is None:
    error("missing password argument")
if startdate is None:
    error("missing startdate argument")
if enddate is None:
    enddate = startdate

if len(args) == 0:
    error("at least one path must be specified")

# Connect to PacketLogic
try:
    pl = packetlogic2.connect(hostname, username, password)
    s = pl.Statistics()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)

#Handle all paths
for path in args:
    if path[-1] != '/':
        path = path + '/'
    print "%s" % path

    # Get list of available data on specified path
    data = s.list (startdate, enddate, path)

    if not data:
        print "Error: no data available for '%s'" % path
        continue

    # Sort the list by in+out
    tdata = [(x['in']+x['out'], x) for x in data]
    tdata.sort()
    data = [x[1] for x in tdata]

    # Reverse the list (most consuming on top)
    data.reverse()

    if count != 0:
        data = data[:count]

    for node in data:
        inb = []
        outb = []
    
        # Retrive the graph data for this node.
        for dp in s.graph(startdate, enddate, path+node["name"], datapoints):
            inb.append(str(dp["in"]))
            outb.append(str(dp["out"]))
        
        # Print it
        print "%s (inbound),%s" % (node["name"], ",".join(inb))
        print "%s (outbound),%s" % (node["name"], ",".join(outb))

    print