import socket, struct, sys
import packetlogic2

filteron = None
if len(sys.argv) > 1:
    filteron = sys.argv[1]

pl = packetlogic2.connect("127.0.0.1", "admin", "pldemo00")
rc = pl.Plrc()

def shapedcnt(idx,oid,sk,flags,_in,_out):
    global filteron
    # idx = shaping counter idx
    # oid = shaping object id
    # sk = split key (ip / subscriber / ...)
    #ip = socket.inet_ntoa(struct.pack('!L', sk))
    if filteron != None:
        if str(sk) != filteron:
            return
    print idx,oid,sk,flags,_in,_out

rc.add_shapingcnt_callback(shapedcnt)
rc.update_forever()

