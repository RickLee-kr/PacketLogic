import sippacket
import packethandler
import sys
import StringIO
import csv
import time
from ReliableRuleset import SimpleNetobjectRuleset

class SIPPacketHandler(packethandler.TCPPacketHandler, packethandler.UDPPacketHandler):
    def __init__(self, iface):
        packethandler.PacketHandler.__init__(self, iface)

        while True:
            try:
                self.rs = SimpleNetobjectRuleset("/NetObjects/SIP", "127.0.0.1", "packetlogicd", "secret2", "1.3.6.1.4.1.15397.2.10.2", "SIP", ["By register"])
            except IOError:
                t,v,tb = sys.exc_info()
                print "Caught IOError, retrying in a minute (%s)" % v
                time.sleep(60)
                continue
            break
                
        self.rs.zone = self.rs.zone
        self.rs.zone.value_definition_add(9, "Packets", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets"] = 0
        self.rs.zone.value_definition_add(10, "Unparsable packets", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Unparsable packets"] = 0
        self.rs.zone.value_definition_add(11, "Packets (REQUEST)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets (REQUEST)"] = 0
        self.rs.zone.value_definition_add(12, "Packets (RESPONSE)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets (RESPONSE)"] = 0
        self.rs.zone.value_definition_add(13, "Packets (UNKNOWN)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets (UNKNOWN)"] = 0

        self.rs.zone.register()

        self.stringio = StringIO.StringIO()
        self.csv = csv.writer(self.stringio, lineterminator='')

    def handle_udpdata(self, data, props):
        self.handle_data(data, props)

    def handle_tcpdata(self, data, props):
        self.handle_data(data, props)
    
    def handle_data(self, data, props):

        self.rs.zone["Packets"] += 1

        try:
            pkt = sippacket.SIPPacket(data)
        except:
            #import traceback
            #print "Bad SIP packet:"
            #traceback.print_exc()
            self.rs.zone["Unparsable packets"] += 1
            return

        data = []

        data.append(time.time())
        data.append(props.get('ip-src', "0.0.0.0"))
        data.append(props.get('udp-src', props.get('tcp-src', 0)))
        data.append(props.get('ip-dst', "0.0.0.0"))
        data.append(props.get('udp-dst', props.get('tcp-dst', 0)))
        data.append(",".join(pkt.header.get("from", ["<not specified>"])))
        data.append(",".join(pkt.header.get("to", ["<not specified>"])))
        data.append(pkt.method)
        data.append(pkt.requesturi)
        data.append(pkt.code)
        data.append(",".join(pkt.header.get("call-id", ["<not specified>"])))
        data.append(",".join(pkt.header.get("cseq", ["<not specified>"])))
        data.append(pkt.reason)

        self.stringio.truncate(0)
        self.csv.writerow(data)
        self.stringio.seek(0)
        print "sipdata:" + self.stringio.read()

        o = []

        if pkt.type == 'REQUEST':
            self.rs.zone["Packets (REQUEST)"] += 1

            if pkt.method == 'REGISTER':
                o.append("By register/%s" % pkt.requesturi)
                self.rs.enqueue(props['ip-src'], o)
        elif pkt.type == 'RESPONSE':
            self.rs.zone["Packets (RESPONSE)"] += 1
        else:
            self.rs.zone["Packets (UNKNOWN)"] += 1


ph = SIPPacketHandler(sys.argv[1])
ph.run()

