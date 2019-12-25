# This is an example of code to use to send monitored GTP-C traffic as UDP
# packets.
#
# This is useful for sending monitored traffic to a PSM. Modify the DESTINATION
# variable to suit the local deployment.
#
# To use this, upload the script as a file named custom.py to the folder Custom
# Snooper files, and use the Custom Snooper as a monitor interface in a
# filtering rule (under Advanced Options in the Filtering rule editor).

import struct
import socket
import sys
import packethandler

# Set the DESTINATION to the address of the PSM and the port to the listen port
# under GTPv2-C source in PSM config (default 2123)
DESTINATION_V2 = ("161.1.150.249", 2123)
DESTINATION_V1 = ("161.1.150.249", 2124)

# Only packets with the destination port below will be forwarded to the PSM
# Set to None to forward all packets
MONITOR_DESTINATION_PORT = None

# Do not change these
GTPC_APPENDED_HEADER_VERSION = 1
IP_PROTO_UDP = 17
IP_VERSION_4 = 4
IP_VERSION_6 = 6


def build_appended_header(props):
    appended_hdr = struct.pack("!B", GTPC_APPENDED_HEADER_VERSION)
    appended_hdr += struct.pack("!B", props['ip-version'])
    if props['ip-version'] == IP_VERSION_4:
        appended_hdr += socket.inet_aton(props['ip-src'])
        appended_hdr += socket.inet_aton(props['ip-dst'])
    elif props['ip-version'] == IP_VERSION_6:
        appended_hdr += socket.inet_pton(socket.AF_INET6, props['ip-src'])
        appended_hdr += socket.inet_pton(socket.AF_INET6, props['ip-dst'])
    else:
        return None
    appended_hdr += struct.pack("!H", props['udp-src'])
    appended_hdr += struct.pack("!H", props['udp-dst'])
    return appended_hdr


class UDPTransporterGTPCPacketHandler(packethandler.UDPPacketHandler):

    def __init__(self, path):
        packethandler.PacketHandler.__init__(self, path)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle_ip6(self, data, props):
        if len(data) < 40:
            raise ValueError("Packet too short for IPv6 header")

        _vcfl, dlen, proto, hl, src, dst = struct.unpack(
            '!IHBB16s16s', data[:40])

        props['ip-src'] = socket.inet_ntop(socket.AF_INET6, src)
        props['ip-dst'] = socket.inet_ntop(socket.AF_INET6, dst)
        props['ip-version'] = IP_VERSION_6

        if proto == IP_PROTO_UDP:
            self.handle_udp(data[40:40 + dlen], props)

    def handle_ip(self, data, props):
        if len(data) < 20:
            raise ValueError("Packet too short for IP header")

        ver = ord(data[0]) >> 4

        if ver == IP_VERSION_6:
            self.handle_ip6(data, props)
            return

        if ver != IP_VERSION_4:
            raise ValueError("Packet with unknown IP version")

        proto = ord(data[9])
        hl = 4 * (ord(data[0]) & 0x0f)

        if hl < 20:
            raise ValueError("Header length too short for IP header")
        if hl > len(data):
            raise ValueError("Packet too short for IP header")

        (totlen,) = struct.unpack("!H", data[2:4])

        if totlen > len(data):
            raise ValueError("Packet too short for IP data")

        props['ip-src'] = socket.inet_ntop(socket.AF_INET, data[12:16])
        props['ip-dst'] = socket.inet_ntop(socket.AF_INET, data[16:20])
        props['ip-version'] = IP_VERSION_4

        if proto == IP_PROTO_UDP:
            self.handle_udp(data[hl:totlen], props)

    def handle_udp(self, data, props):
        if len(data) < 8:
            raise ValueError("Packet too short for UDP header")

        (src, dst, length, chksum) = struct.unpack("!HHHH", data[:8])

        if (MONITOR_DESTINATION_PORT is None) or (dst == MONITOR_DESTINATION_PORT):
            props['udp-src'] = src
            props['udp-dst'] = dst

            if length > len(data):
                raise ValueError(
                    "Packet too short for UDP data (%d %d)" % (length, len(data)))

            msg = data[8:length]
            version = struct.unpack('B',msg[0])[0] >> 5
            appended_header = build_appended_header(props)
            if appended_header is not None:
                msg += appended_header
            if version == 1:
                self.socket.sendto(msg, DESTINATION_V1)
            elif version == 2:
                self.socket.sendto(msg, DESTINATION_V2)
#            self.socket.sendto(msg, DESTINATION_V2)
 

ph = UDPTransporterGTPCPacketHandler(sys.argv[1])
ph.run()
