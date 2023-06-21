import struct
import socket

class IPv6Packet:
    def __init__(self, version, traffic_class, flow_label, payload_length, next_header, hop_limit, source_ip, destination_ip, data):
        self.version = version
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.payload_length = payload_length
        self.next_header = next_header
        self.hop_limit = hop_limit
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.data = data

    def pack(self):
        version_tc_fl = (self.version << 28) + (self.traffic_class << 20) + self.flow_label

        ip_header = struct.pack(">IHBB", version_tc_fl, self.payload_length, self.next_header,
                                self.hop_limit) + socket.inet_pton(socket.AF_INET6, self.source_ip) + \
                    socket.inet_pton(socket.AF_INET6, self.destination_ip)

        return ip_header + self.data

    def unpack(self, data):
        ipv6_first_word, payload_length, next_header, hop_limit = struct.unpack(">IHBB", data[0:8])
        self.version = ipv6_first_word >> 28
        self.traffic_class = (ipv6_first_word >> 20) & 0xFF
        self.flow_label = ipv6_first_word & 0xFFFFF
        self.payload_length = payload_length
        self.next_header = next_header
        self.hop_limit = hop_limit
        self.source_ip = socket.inet_ntop(socket.AF_INET6, data[8:24])
        self.destination_ip = socket.inet_ntop(socket.AF_INET6, data[24:40])
        self.data = data[40:]

    def __str__(self):
        return f"Version: {self.version}, Traffic Class: {self.traffic_class}, Flow Label: {self.flow_label}, Payload Length: {self.payload_length}, Next Header: {self.next_header}, Hop Limit: {self.hop_limit}, Source IP: {self.source_ip}, Destination IP: {self.destination_ip}, Data: {self.data}"

# Example usage
version = 6
traffic_class = 0
flow_label = 12345
payload_length = 40
next_header = 6  # TCP
hop_limit = 64
source_ip = "2001:db8::1"
destination_ip = "2001:db8::2"
data = b"This is the payload data"

# Create an IPv6 packet object
ipv6_packet = IPv6Packet(version, traffic_class, flow_label, payload_length, next_header, hop_limit,
                         source_ip, destination_ip, data)

# Pack the IPv6 packet
packed_data = ipv6_packet.pack()

# Unpack the IPv6 packet
unpacked_data = IPv6Packet(version, traffic_class, flow_label, payload_length, next_header, hop_limit,
                           source_ip, destination_ip, data)
unpacked_data.unpack(packed_data)

# Print the IPv6 packet details
print(ipv6_packet)
print(unpacked_data)
