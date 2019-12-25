import dhcppacket
import packethandler
import sys
import time
from ReliableRuleset import SimpleNetobjectRuleset

import os
import subprocess
import demjson

TIMEOUT = 30
PLHOST = "127.0.0.1"
PLUSER = "packetlogicd"
PLPASS = "secret2"
PSM_IP = "1.235.126.135"
PSM_PORT = 3996

class DHCPPacketHandler(packethandler.UDPPacketHandler):

    def __init__(self, iface):
        packethandler.PacketHandler.__init__(self, iface)

        while True:
            try:
                self.rs = SimpleNetobjectRuleset("/NetObjects/DHCP",
                                                 PLHOST, PLUSER, PLPASS,
                                                 "1.3.6.1.4.1.15397.2.10.1", "DHCP",
                                                 ["By MAC", "By option-82",
                                                  "By relay-agent"])
            except IOError:
                t,v,tb = sys.exc_info()
                print "Caught IOError, retrying in a minute (%s)" % v
                time.sleep(60)
                continue
            break

        self.rs.zone.value_definition_add (9, "Packets", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets"] = 0
        self.rs.zone.value_definition_add(10, "Unparsable packets", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Unparsable packets"] = 0
        self.rs.zone.value_definition_add(11, "Packets (DHCPREQUEST)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets (DHCPREQUEST)"] = 0
        self.rs.zone.value_definition_add(12, "Packets (DHCPACK)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Packets (DHCPACK)"] = 0
        self.rs.zone.value_definition_add(13, "Ignored packets", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["Ignored packets"] = 0
        
        self.rs.zone.value_definition_add(14, "ACK (FTTH)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["ACK (FTTH)"] = 0
        self.rs.zone.value_definition_add(15, "ACK (VDSL)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["ACK (VDSL)"] = 0
        self.rs.zone.value_definition_add(16, "ACK (HFC)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["ACK (HFC)"] = 0
        self.rs.zone.value_definition_add(17, "ACK (NoOpt)", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["ACK (NoOpt)"] = 0
        self.rs.zone.value_definition_add(18, "FTTH Mapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["FTTH Mapped"] = 0
        self.rs.zone.value_definition_add(19, "FTTH Unmapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["FTTH Unmapped"] = 0
        self.rs.zone.value_definition_add(20, "VDSL Mapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["VDSL Mapped"] = 0
        self.rs.zone.value_definition_add(21, "VDSL Unmapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["VDSL Unmapped"] = 0
        self.rs.zone.value_definition_add(22, "HFC Mapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["HFC Mapped"] = 0
        self.rs.zone.value_definition_add(23, "HFC Unmapped", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["HFC Unmapped"] = 0
        self.rs.zone.value_definition_add(24, "PSM Connects", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["PSM Connects"] = 0
        self.rs.zone.value_definition_add(25, "PSM Updates", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["PSM Updates"] = 0
        self.rs.zone.value_definition_add(26, "PSM Failed Updates", self.rs.zone.TYPE_MOMENT)
        self.rs.zone["PSM Failed Updates"] = 0
        self.rs.zone.register()
        
        self.requests = {}

        self.psmSock = None
        self.connectToPSM()

    def connectToPSM(self):
        self.psmSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.psmSock.connect((PSM_IP, PSM_PORT))
        self.rs.zone["PSM Connects"] += 1

    def sendToPSM(self, data):
        jsonStr = str(demjson.encode(data))

        try:
            if self.psmSock.send(jsonStr + "\n") > 0:
                self.rs.zone["PSM Updates"] += 1
            else:
                self.rs.zone["PSM Failed Updates"] += 1
                self.connectToPSM()
        except:
            self.rs.zone["PSM Failed Updates"] += 1
            self.connectToPSM()
            
    def extract_subscriber_key(self, req, pkt):
        data = {}
        if "option-224" in req.options:
            opt224 = req.options["option-224"]
            if "subOpt2" in opt224:
                data["TYPE"] = "FTTH"
                data["KEY"] = "ONT-" + opt224["subOpt2"]
        elif "option-82" in req.options:
            opt82 = req.options["option-82"]
            subOpt1 = opt82["subOpt1"]
            subOpt2 = opt82["subOpt2"]
            if len(subOpt1) == 6 and len(subOpt2) == 4:
                (rack, shelf, cardAndPort) = struct.unpack("!BBL", subOpt1)
                card = cardAndPort >> 20
                port = cardAndPort & 0xFFFFF
                ip = struct.unpack("BBBB", subOpt2)
                data["TYPE"] = "VDSL"
                ipStr = "%d.%d.%d.%d" % (ip[0], ip[1], ip[2], ip[3])
                portStr = "%02d" % port
                data["KEY"] = ipStr + "\%" + portStr
            elif len(subOpt2) == 6:
                mac = struct.unpack("BBBBBB", subOpt2)
                data["TYPE"] = "HFC"
                mac_addr = "%02X:%02X:%02X:%02X:%02X:%02X" % (mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])
                data["KEY"] = mac_addr.lower()

        if len(data) > 0:
            return data
        else:
            return None

    def handle_udpdata(self, data, props):
        self.rs.zone["Packets"] += 1

        try:
            pkt = dhcppacket.DHCPPacket(data)
        except:
            #import traceback
            #print "Bad dhcp packet:"
            #traceback.print_exc()
            self.rs.zone["Unparsable packets"] += 1
            return

        if pkt.type == 'DHCPREQUEST':
            self.rs.zone["Packets (DHCPREQUEST)"] += 1
            self.requests[(pkt.xid, pkt.hwaddr)] = (time.time(), pkt)
        elif pkt.type == 'DHCPACK':
            self.rs.zone["Packets (DHCPACK)"] += 1
            ip = dhcppacket.decodeip(pkt.yiaddr)

            if ip != '0.0.0.0':
                (t, req) = self.requests.get((pkt.xid, pkt.hwaddr), (None, None))

                if req:
                    data = self.extract_subscriber_key(req, pkt)
                    
                    if data is None:
                        self.rs.zone["ACK (NoOpt)"] += 1

                    elif data["TYPE"] == "FTTH":
                        self.rs.zone["ACK (FTTH)"] += 1
                        psqlQuery = "psql -A -t -U packetlogic -c \"SELECT subscriberid FROM subscriber_map WHERE subscriberkey=\'%s' LIMIT 1\" skbb_subscriber_map" % data["KEY"]
                        billingId = subprocess.check_output(psqlQuery, shell=True)
                        billingId = billingId.rstrip('\n')
                        
                        #print "FTTH: %s" % billingId

                        if len(billingId) == 10:
                            data["BILLINGID"] = billingId
                            self.rs.zone["FTTH Mapped"] += 1
                        else:
                            self.rs.zone["FTTH Unmapped"] += 1

                    elif data["TYPE"] == "VDSL":
                        self.rs.zone["ACK (VDSL)"] += 1
                        psqlQuery = "psql -A -t -U packetlogic -c \"SELECT subscriberid FROM subscriber_map WHERE subscriberkey LIKE \'%s' LIMIT 1\" skbb_subscriber_map" % data["KEY"]
                        billingId = subprocess.check_output(psqlQuery, shell=True)
                        billingId = billingId.rstrip('\n')
                        
                        #print "VDSL: %s" % billingId
                        
                        if len(billingId) == 10:
                            data["BILLINGID"] = billingId
                            self.rs.zone["VDSL Mapped"] += 1
                        else:
                            self.rs.zone["VDSL Unmapped"] += 1

                    elif data["TYPE"] == "HFC":
                        self.rs.zone["ACK (HFC)"] += 1
                        psqlQuery = "psql -A -t -U packetlogic -c \"SELECT subscriberid FROM subscriber_map WHERE subscriberkey=\'%s' LIMIT 1\" skbb_subscriber_map" % data["KEY"]
                        billingId = subprocess.check_output(psqlQuery, shell=True)
                        billingId = billingId.rstrip('\n')

                        #print "HFC KEY: %s ID: %s" % (data['KEY'], billingId)
                        
                        if len(billingId) == 10:
                            data["BILLINGID"] = billingId
                            self.rs.zone["HFC Mapped"] += 1
                        else:
                            #print "Unmapped HFC KEY[%s]" % data["KEY"]
                            self.rs.zone["HFC Unmapped"] += 1

                    if data and "BILLINGID" in data:
                        #print "MAP: %s,%s" % (data['BILLINGID'], ip)
                        data["IP"] = ip
                        
                        leaseTime = pkt.options["ip-address-lease-time"]

                        if leaseTime > 0:
                            data["LEASETIME"] = leaseTime
                        else:
                            data["LEASETIME"] = 3600
 
                        del data['TYPE']   
                        del data['KEY']
                        self.sendToPSM(data)

                    del self.requests[(pkt.xid, pkt.hwaddr)]
            else:
                self.rs.zone["Ignored packets"] += 1

        # timeout old requests..
        now = time.time()
        removes = []
        for k, v in self.requests.iteritems():
            if v[0] + TIMEOUT < now:
                removes.append(k)
        for k in removes:
            del self.requests[k]

    def run(self):
        try:
            packethandler.PacketHandler.run(self)
        except KeyboardInterrupt:
            pass
        self.rs.stop()
        print "done?"

ph = DHCPPacketHandler(sys.argv[1])
ph.run()
