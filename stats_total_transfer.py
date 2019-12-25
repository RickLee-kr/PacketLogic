#!/usr/bin/python

"""
 Display statistics for protocols and services
"""

__version__ = "1.1 2008-11-14 Procera Networks"

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
import getopt
import packetlogic2

def hashtable_hash_str(value):
    return reduce( lambda h, x : long((h<<5) - h + x), map(lambda x : ord(x), value)) & 0x3fff
        
def usage(a=None):
    print "usage: %s -s startdate -H hostname -U username -P password [-e end date] [-c number] [-i IP] [-p path] [-t number]" % sys.argv[0]
    print "dateformat is YYYY-MM-DD"
    print "-s -H, -U, -P are mandatory"
    print "Options:" 
    print "-e : End date (YYYY-MM-DD)"
    print "-c : Number of services, 0 for all"
    print "-i : host ip"
    print "-p : path to netobject"
    print "-t : Number of protocols, 0 for all"
    if a is not None:
        print "Error: %s" % a
        
if len(sys.argv) <2:
    usage()
    sys.exit(2)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:e:c:i:t:p:H:U:P:", ["help", "startdate=", "enddate=", "numservices=", "ip=", "numprotocols=", "path=", "hostname=", "username=", "password="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

startdate = None
enddate = None
numprotocols = 0
numservices = 0
ip = None
path = None
hostname = None
username = None
password = None

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit(2)
    if o in ("-s", "--startdate"):
        startdate = a
    if o in ("-e", "--enddate"):
        enddate = a
    if o in ("-c", "--protocols"):
        numprotocols = int(a)
    if o in ("-i", "--ip"):
        ip = a
    if o in ("-t", "--services"):
        numservices = int(a)
    if o in ("-p", "--path"):
        path = a
    if o in ("-H", "--hostname"):
        hostname = a
    if o in ("-U", "--username"):
        username = a
    if o in ("-P", "--password"):
        password = a

# check for mandatory arguments
if not startdate:
    usage("Please specify startdate")
    sys.exit(2)
elif not hostname:
    usage("No hostname specified (-H)")
    sys.exit(2)
elif not username:
    usage("No username specified (-U)")
    sys.exit(2)
elif not password:
    usage("No password specified (-P)")
    sys.exit(2)

# check for optional args
if not enddate:
    enddate = startdate
if not path:
    path = "/Services/TCPv4"
if ip:
    path = "/Hosts/%s/%s" % (hashtable_hash_str(ip), ip)

# Connect to PLDB
try:
    pl = packetlogic2.connect(hostname, username, password)
    pld = pl.Statistics()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)

if pld.PLDBVersion > 11:
    print "Error: This script isn't designed for v12 stats"
    sys.exit(1)

print "All values are in bytes"

# Retrive the list of protocols
protol = pld.list(startdate, enddate, "/Services")

# Sort the list
protol.sort()

# Reverse the list (most consuming on top)
protol.reverse()

# Retrive the list of services (Defaultpath: /Services/TCPv4)
servl = pld.list(startdate, enddate, path)

# Sort the list
servl.sort()

# Reverse the list (most consuming on top)
servl.reverse()

# generate protocols output
print "Total protocol transfer (All hosts)(in/out):"

if len(protol) < numprotocols or numprotocols == 0:
    numprotocols = len(protol) 

for i in range(numprotocols):
    if protol[i]["in"] > 0 and protol[i]["out"] > 0:
        print "%s,%s,%s" % (protol[i]["name"], protol[i]["in"], protol[i]["out"])

# generate services output
print ""
if ip:
    print "Total service transfer for %s" % ip
else:
    print "Total service transfer (in/out):"

if len(servl) < numservices or numservices == 0:
    numservices = len(servl) 

for i in range(numservices):
    if servl[i]["in"] > 0 and servl[i]["out"] > 0:
        print "%s,%s,%s" % (servl[i]["name"], servl[i]["in"], servl[i]["out"])