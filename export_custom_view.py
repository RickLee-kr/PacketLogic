import packetlogic2

PL_HOST = '192.168.1.55'
PL_USER = 'admin'
PL_PASS = 'procera'


conn = packetlogic2.connect(PL_HOST, PL_USER, PL_PASS)
rt = conn.Realtime()


v = rt.get_view_builder()
v.filter("Service", "SSL v3")
v.distribution("Server Hostname")
count = 0

def faggr(data):
	global count

	if count > 2:
		rt.stop_updating()
	if data:
		for node in data.children:
			print node.name, node.speed
		count = count + 1	


rt.add_aggr_view_callback(v, faggr)

rt.update_forever()