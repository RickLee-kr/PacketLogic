#!/usr/bin/python

import packetlogic2
import datetime

pl = packetlogic2.connect("49.231.44.58","admin","Aisths01")

services = []

rt = pl.Realtime()

def calc_quality(quality):

	# packets,retrans,drops,packets,retrans,drop

	if(quality[0] == 0):
		int_in = 1
		int_out = 1
	else:
		int_in = float(1.0 - (float(quality[1]) / float(quality[0])))
		int_out = float(1.0 - (float(quality[2]) / float(quality[0])))


	if(quality[3] == 0):
		ext_out = 1
		ext_in = 1
	else:
		ext_out = float(1.0 - (float(quality[4]) / float(quality[3])))
		ext_in = float(1.0 - (float(quality[5]) / float(quality[3])))

	return(int_in, int_out, ext_in, ext_out)


def display_view(root):
	#print "UPDATE"
	for service in root.children:
		dl_data = service.data
		if(dl_data.has_key('quality')):
			quality = calc_quality(dl_data['quality'])
			speed = dl_data['speed']
			if(quality[0] < 0.95 or quality[1] < 0.95):
				if service.name not in services:
					if(speed[0] > 5000000):
						print "%s Trigger: %s Speed: %d %d Quality: %.2f %.2f" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), service.name, speed[0], speed[1], quality[0], quality[1])
						services.append(service.name)
			else:
				if service.name in services:
					print "%s Reset: %s Speed: %d %d Quality: %.2f %.2f" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), service.name, speed[0], speed[1], quality[0], quality[1])
					services.remove(service.name)
				

v = rt.get_view_builder()
v.filter("Visible NetObject", "PSM")
v.distribution("Service")

rt.add_aggr_view_callback(v, display_view)

rt.update_forever()
