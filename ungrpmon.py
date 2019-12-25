#!/usr/bin/python

import sys
import packetlogic2
import optparse

def main():

	opt = optparse.OptionParser()

	opt.add_option("--host", dest="host",
		help="host to connect to")

	opt.add_option("--user", dest="user",
		help="username when connecting")

	opt.add_option("--pass", dest="password",
		help="password when connecting")

	(options, args) = opt.parse_args()

	if len(args) > 0:
		opt.error("Inconnect number of arguments")

	print("%s %s %s" % (options.host, options.user, options.password))	

	try:
		pl = packetlogic2.connect(options.host, options.user, options.password)
		rt = pl.Realtime()
	except:
		print "failed"
		return 0

	def cb(data):
 	  if len(data.hosts) > 0:
		print "Number of hosts: %d" % len(data.hosts)
		rt.stop_updating()

	rt.add_netobj_callback(cb, under="/NetObjects/<Ungrouped>", include_hosts=True)
	rt.update_forever()
	rt.close()

if __name__ == '__main__':
    sys.exit(main())

