#
# This simply sends monitored udp packets to specified destination
# (ipaddress, udp port)
#
# Supports Dual-Stack
#

import packethandler
import socket
import sys

DESTINATION_V4 = ("10.1.1.12", 5470)
DESTINATION_V6 = ("2001::1:12", 5460)

class PacketHandlerDS(packethandler.PacketHandler):
    def handle_packet(self, data, props):
        if data[self.prot_off] == 'PL':
            ip_off = struct.unpack(">H", data[self.iphdr_off:self.iphdr_off+2])[0]
            conn = struct.unpack(">L", data[self.iphdr_off+2:self.iphdr_off+6])[0]
            props['conn-id'] = conn
            self.handle_ip(data[ip_off:], props)
        elif data[self.prot_off] == '\x08\x00':
            self.handle_ip(data[self.iphdr_off:], props)
        elif data[self.prot_off] == '\x81\x00' and data[self.prot_off.start+4:self.prot_off.stop+4] == '\x08\x00':
            self.handle_ip(data[self.iphdr_off+4:], props)
        elif data[self.prot_off] == '\x86\xDD':
            self.handle_ipv6(data[self.iphdr_off:], props)
        else:
            self.handle_nonip(data[self.iphdr_off:], props)

    def handle_ipv6(self, data, props):
        pass

class IPPacketHandlerDS(PacketHandlerDS, packethandler.IPPacketHandler):
    def handle_ipv6(self, data, props):
        _vcfl, dlen, nh, hl = struct.unpack('>IHBB', data[0:8])

        if nh == 0x11: # UDPv6
            self.handle_udpv6(data[40:], props)

class UDPPacketHandlerDS(IPPacketHandlerDS, packethandler.UDPPacketHandler):
    def handle_udpv6(self, data, props):
        if len(data) < 8:
            raise ValueError("Packet too short for udp header")
            
        (src, dst, leng, chksum) = struct.unpack(">HHHH", data[:8])

        props['udp-src'] = src
        props['udp-dst'] = dst

        if leng > len(data):
            raise ValueError("Packet too short for udp data (%d %d)" % (leng, len(data)))

        self.handle_udpdata_v6(data[8:leng], props)

class UDPTransporterPacketHandlerDS(UDPPacketHandlerDS):
    def __init__(self, path):
        packethandler.PacketHandler.__init__(self, path)
        self.socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def handle_udpdata(self, data, props):
        #print "handle_udpdata src[%d] dst[%d]" % (props['udp-src'], props['udp-dst'])
        self.socket_v4.sendto(data, DESTINATION_V4)
    
    def handle_udpdata_v6(self, data, props):
        #print "handle_udpdata_v6 src[%d] dst[%d]" % (props['udp-src'], props['udp-dst'])
        self.socket_v6.sendto(data, DESTINATION_V6)

ph = UDPTransporterPacketHandlerDS(sys.argv[1])
ph.run()
