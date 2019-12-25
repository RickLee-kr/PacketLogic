#!/usr/bin/env python

"""
Generates a list of most popular HTTP server hostnames (VHOST) from Statistics.
You have to use a ShapingRule named "HTTP statistics" that stores VHOST data.

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
import packetlogic2

try:
    [plhost, pluser, plpass, startdate, enddate] = sys.argv[1:]
except:
    print "Usage: %s plhost pluser plpass startdate enddate" % sys.argv[0]
    sys.exit(1)

try:
    pl = packetlogic2.connect(plhost, pluser, plpass)
except:
    t, v, tb = sys.exc_info()
    print "Error: Couldn't connect: %s" % v
    sys.exit(1)

s = pl.Statistics()

if s.PLDBVersion > 11:
    # vhosts are split into different levels in v12,
    # which this script doesn't understand, also the
    # path is "/Shaping Rules"
    print "Error: This script isn't designed for v12 stats"
    sys.exit(1)

rule = '/Shaping Rules/HTTP statistics/VHosts/Remote/'

d = {}
for i in s.list(startdate, enddate, rule):
    try:
        if ".co." in i['name']:
            domain = i['name'].split(".")[-2:-1][0]
        else:
            domain = i['name'].split(".")[-2:-1][0]
    except: 
        continue

    transfer = i['in'] + i['out']

    if domain in d:
        d[domain] = d[domain] + transfer
    else:
        d[domain] = transfer

domains = []                
for domain in d:
    domains.append((d[domain], domain))

domains.sort()
domains.reverse()
for domain in domains:
    print domain[1].capitalize(), domain[0]