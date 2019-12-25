#!/usr/bin/env python

"""
Export comma separated values from a NetObject path
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

# Default measurepoint value.
measurepoints = 10

#Default countlist
countlist = 0
try:
    pladdr, pluser, plpass, startdate, enddate, measurepoints, path, numdisplay = sys.argv[1:]
except:
    print "Usage: %s PLADDRESS USER PASSWORD STARTDATE ENDDATE MEASUREPOINTS PATH NUMBERTODISPLAY" % sys.argv[0]
    print "Example:"
    print "%s PLADDRESS USER PASSWORD 2007-03-01 2007-03-31 10 /Services 0" % sys.argv[0]
    sys.exit(1)


pl = packetlogic2.connect(pladdr, pluser, plpass)
s = pl.Statistics()

# Retrive the list of services specified by
nodel = s.list(startdate, enddate, path)

if not nodel:
    print "Error: no data available for that day"
    sys.exit(1)

# Sort the list
nodel.sort()

# Reverse the list (most consuming on top)
nodel.reverse()

# list all if numdisplay is 0 or >bigger than number of entries
if int(numdisplay) == 0:
    countnum = int(len(nodel))
elif int(numdisplay) < int(len(nodel)): 
    countnum = int(numdisplay)
else:
    countnum = int(len(nodel))

for i in range(countnum):
    inb = []
    outb = []

    # Retrive the graph data for this service.
    for x in s.graph(startdate, enddate, path+"/"+nodel[i]["name"], numvals=int(measurepoints)):
        inb.append(str (x["in"]))
        outb.append(str (x["out"]))
        
    # Print it
    print "%s (inbound),%s" % (nodel[i]["name"], ','.join(inb))
    print "%s (outbound),%s" % (nodel[i]["name"], ','.join(outb))