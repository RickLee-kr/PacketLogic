#!/usr/bin/env python

"""Script to retrieve statistics about how much data the 1%, 5%, 10%, and
   20% of most active hosts have transferred."""

__version__ = "1.2 2006-11-14 Procera Networks"

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
import packetlogic2

try:
    [host, user, pwd, startdate, enddate] = sys.argv[1:]
except ValueError:
    print "Usage: top_stats.py plhost pluser plpass startdate enddate"
    print "Example: top_stats.py 192.168.1.25 admin pldemo00 2005-05-09 2005-05-16"
    sys.exit(1)

# Connect to PacketLogic
try:
    pl = packetlogic2.connect(host, user, pwd)
    s = pl.Statistics()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)

#Get a list of all host active the requested days
hosts = []
for d in s.list(startdate, enddate, "/Hosts"):
    hosts.append((d['in'] + d['out'], d['name']))

print "There was %d different hosts recorded active between %s and %s" % (len(hosts), startdate, enddate)

# Make hosts with most transferred data come first in list
hosts.sort()
hosts.reverse()

# Remove hostname
xfers = [a for a, b in hosts]

# The most active host is first
tophost = hosts[0]

print "Top host (%s) transferred a total of %dMiB" % (tophost[1].split("/")[-1], tophost[0]>>20)
print

def get_top(lst, x, tot):
    num = len(lst)*x/100+1
    amount = sum(lst[:num])
    perc = 100*amount/tot
    print "The top %d%% (%d) active hosts transferred %d%% (%dMiB)" % (x, num, perc, amount>>20)

total = sum(xfers)
print "A total of %dMiB was transferred between %s and %s" % (total>>20, startdate, enddate)
print

get_top(xfers, 1, total)
get_top(xfers, 5, total)
get_top(xfers, 10, total)
get_top(xfers, 20, total)
