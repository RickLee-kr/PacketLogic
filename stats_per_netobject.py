#!/usr/bin/env python

"""
Script that generate statistics for a NetObject
"""

__version__ = "1.1 2007-12-17 Procera Networks"

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


# Import PacketLogic DB API.
import packetlogic2

# Standard Imports
import sys
import time

# We also Require PIL and PyChart
#import Image
from pychart import canvas, theme, axis, area, line_plot, line_style, text_box

# Check arguments
if len(sys.argv) < 6:
    print "usage: %s <host> <user> <password> <startdate> <stopdate>" % sys.argv[0]

# Connect to stats machine.
try:
    pl = packetlogic2.connect(sys.argv[1], sys.argv[2], sys.argv[3])
    s = pl.Statistics()
except:
    t, v, tb = sys.exc_info()
    print "Couldn't connect to PacketLogic: %s" % v
    sys.exit(1)


argd1 = sys.argv[4]
argd2 = sys.argv[5]

# This verifies that we have data for this period of time
dates = s.date_list()
if not argd1 in dates:
    print "Opos, don't have data for date %s" % argd1
    sys.exit(-1)
elif not argd2 in dates:
    print "Ooops, don't have data for date %s" % argd2
    sys.exit(-1)


# Convert dates into unixTime
startdate = time.mktime(time.strptime(argd1, "%Y-%m-%d"))
stopdate = time.mktime(time.strptime(argd2, "%Y-%m-%d"))

# the interval is?
#interval = startdate - stopdate;
interval = 5

values = int((stopdate-startdate))/(60*int(interval))

print "interval %d, values: %d" % (interval, values);

# init pychart
theme.get_options()

def update_f(f):
    ret = f[0]
    #   f[0] = f[0] + (60 * int(interval))
    #   f[0] += interval
    f[0] += 1
    return int(ret)
    

def print_xtick(x):
    return time.ctime(startdate + (x * (5 * 60)))

def do_graph(name):
    # list all netobjects
    netobjects = s.list(argd1, argd2, name) #[0:10]

    if netobjects:
        netobjects.sort()
        netobjects.reverse()

        for n in netobjects:
            f = [0]

            # this is kind of a fulhack. This makes sure that the
            # node is a netobject acutally.
            if n["priority"] == 10 or n["priority"] == 138:
                continue

            fullname = name+"/"+n["name"]
            print "drawing %s" % fullname

            # get som graph data
            graph = s.graph(argd1, argd2, name+"/"+n["name"], values)
            indata = [(update_f(f),g["in"]) for g in graph]
            outdata = [(update_f(f),g["out"]) for g in graph]

            ymax = 0
            for g in indata + outdata:
                if g[1] > ymax:
                    ymax = g[1]

                    
            xaxis = axis.X(label="time", tic_interval=288, format=print_xtick)
            yaxis = axis.Y(label="kbps", tic_interval=(ymax/10)+1)

            ar = area.T(size=(640, 480), x_axis=xaxis, y_axis=yaxis, 
                    y_range=(0, ymax * 1.1))

            plot = line_plot.T(label="in", data=indata, line_style=line_style.red)
            ar.add_plot(plot)
            
            plot = line_plot.T(label="out", data=outdata, line_style=line_style.black)
            ar.add_plot(plot)

            can = canvas.init(fullname.replace("/","_")+".png", "png")
            ar.draw(can)
            tb = text_box.T(loc=(10, 400), text="Object: %s\nTotal in: %d\nTotal out: %d" % (n["name"], n["in"], n["out"]), line_style=None)
            tb.draw()
            can.close()
            
            # recurse deeper
            do_graph(name+"/"+n["name"])

do_graph("/NetObjects/")
