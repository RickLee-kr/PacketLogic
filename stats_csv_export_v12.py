#!/usr/bin/env python

"""

"""

__version__ = "1.0 2009-04-03 Procera Networks"

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

import packetlogic2
import sys
import string
import datetime

VALUE_TYPE_BASE = 0x0200

try:
  pladdr, pluser, plpass, startdate, enddate, path, type, mode, numdisplay = sys.argv[1:]
except:
  print "Usage: %s PLADDRESS USER PASSWORD STARTDATE ENDDATE PATH TYPE MODE NUMBERTODISPLAY" % sys.argv[0]
  print "Example:"
  print "%s PLADDRESS USER PASSWORD 2007-03-01 2007-03-31 /Services 4 1 0" % sys.argv[0]
  print ""
  print "Type parameter:  Type of value path, possible Types :"
  print "Object Root : 0"
  print "NetObject : 1"
  print "Host : 2"
  print "LocalVhost : 3"
  print "RemoteVhost : 4"
  print "ServiceObject : 5"
  print "Service : 6"
  print "Client Aspath : 7"
  print "Server Aspath : 8"
  print "Vlan : 9"
  print ""
  print "Mode parameter: 1 = graphs in bytes, 2 = graphs in kbps"

  sys.exit(1)

pathtype = int(type)
if (pathtype != 0):
	pathtype += VALUE_TYPE_BASE

mode = int(mode)
topn = int(numdisplay)

dt1=datetime.date(*map(int, startdate.split('-')))
dt2=datetime.date(*map(int, enddate.split('-')))

measurepoints = (1 + (dt2 - dt1).days) * 288
pl = packetlogic2.connect(pladdr, pluser, plpass)
s = pl.Statistics()

# Retrive the list of services specified by
nodel = s.toplist(startdate, enddate, path, max=topn, pathtype=pathtype)

if not nodel:
  print "Error: no data available for that day"
  sys.exit(1)
# We receive a toplist for each field stored, we will just grab the top list for
# incoming and outgoing bytes and get graph  data for them
nodes={}
for list in (nodel['Toplist, bytes in'], nodel['Toplist, bytes out']):
	for n in list:
		nodes[n['name']] = [n['values']['bytes in'] + n['values']['bytes out'], n["name"], n["type"]]

nnodes=nodes.values ()
nnodes.sort ()
nnodes.reverse ()
for n in nnodes:
	inb = []
 	outb = []
	try:
  		# Retrive the graph data for this service.
  		for x in s.graph(startdate, enddate, path + "/" + n[1], measurepoints, n[2], mode):
			inb.append(str (x["bytes in"]))
			outb.append(str (x["bytes out"]))
	except:
		continue
		
  	# Print it
  	print "%s (inbound),%s" % (n[1], string.join (inb, ","))
  	print "%s (outbound),%s" % (n[1], string.join (outb, ","))