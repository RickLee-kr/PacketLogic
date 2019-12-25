#!/usr/bin/env python

"""
Script to show services per NetObject from Statistics
"""

__version__ = "1.2 2008-11-14 Procera Networks"

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

if len(sys.argv) < 8:
    print "usage: %s <host> <user> <password> <startdate> <enddate> <path> <service>"
    sys.exit(1)

try:
    pl = packetlogic2.connect(sys.argv[1], sys.argv[2], sys.argv[3])
    s = pl.Statistics()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)


nodes = s.list(sys.argv[4], sys.argv[5], sys.argv[6])

total_in = 0
total_out = 0

for node in nodes:
    print node["name"]
    node_data = s.list(sys.argv[4], sys.argv[5], sys.argv[6] + "/" + node["name"])
    for serv in node_data:
        if serv["name"] == sys.argv[7]:
            total_in += serv["in"]
            total_out += serv["out"]
print "Total in: " + str(total_in)
print "Total out: " + str(total_out)

            