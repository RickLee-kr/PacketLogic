user = "admin"
password = "pldemo00"
host = "localhost"
netobject_root = "/NetObjects/PSM"

import packetlogic2 as pl2

c = pl2.connect(host, user, password)
rt = c.Realtime()
rs = c.Ruleset()

root_id = rs.object_find(netobject_root).id
netobjects = dict((no.id, (no.fullpath, [])) for no in rs.object_list(netobject_root))

dynitems = rt.dyn.list(netobject=root_id, recurse=True, properties=[rt.dyn.SUBSCRIBER_NAME])

for ip, items in dynitems:
    for noid, props in items:
    	info = netobjects.get(noid)
    	if info is not None:
    		info[1].append((ip, props[rt.dyn.SUBSCRIBER_NAME]))

for no, dynitems in netobjects.itervalues():
		print no
		for ip, name in dynitems:
			print "\t%15s %16s" %(ip, name)
