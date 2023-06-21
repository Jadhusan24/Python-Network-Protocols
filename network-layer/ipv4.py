import struct
import socket

class IPv4Packet:
    def __init__(self, version, header_length, service_type, total_length, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_ip, destination_ip, data):
        self.version = version
        self.header_length = header_length
        self.service_type = service_type
        self.total_length = total_length
        self.identification = identification
        self.flags = flags
        self.fragment_offset = fragment_offset
        self.time_to_live = time_to_live
        self.protocol = protocol
        self.header_checksum = header_checksum
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.data = data

    def pack(self):
        version_ihl = (self.version << 4) + self.header_length
        flags_fragment = (self.flags << 13) + self.fragment_offset

        ip_header = struct.pack("!BBHHHBBH4s4s", version_ihl, self.service_type, self.total_length,
                                self.identification, flags_fragment, self.time_to_live,
                                self.protocol, self.header_checksum,
                                socket.inet_aton(self.source_ip),
                                socket.inet_aton(self.destination_ip))

        return ip_header + self.data

    def unpack(self, data):
        ip_fields = struct.unpack("!BBHHHBBH4s4s", data[:20])
        self.version = ip_fields[0] >> 4
        self.header_length = ip_fields[0] & 0xF
        self.service_type = ip_fields[1]
        self.total_length = ip_fields[2]
        self.identification = ip_fields[3]
        self.flags = ip_fields[4] >> 13
        self.fragment_offset = ip_fields[4] & 0x1FFF
        self.time_to_live = ip_fields[5]
        self.protocol = ip_fields[6]
        self.header_checksum = ip_fields[7]
        self.source_ip = socket.inet_ntoa(ip_fields[8])
        self.destination_ip = socket.inet_ntoa(ip_fields[9])
        self.data = data[20:]

    def __str__(self):
        return f"Version: {self.version}, Header Length: {self.header_length}, Service Type: {self.service_type}, Total Length: {self.total_length}, Identification: {self.identification}, Flags: {self.flags}, Fragment Offset: {self.fragment_offset}, TTL: {self.time_to_live}, Protocol: {self.protocol}, Header Checksum: {self.header_checksum}, Source IP: {self.source_ip}, Destination IP: {self.destination_ip}, Data: {self.data}"

# Example usage
version = 4
header_length = 5
service_type = 0
total_length = 40
identification = 12345
flags = 0
fragment_offset = 0
time_to_live = 64
protocol = 6  # TCP
header_checksum = 0
source_ip = "192.168.1.1"
destination_ip = "192.168.1.2"
data = b"This is the payload data"

# Create an IPv4 packet object
ipv4_packet = IPv4Packet(version, header_length, service_type, total_length, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_ip, destination_ip, data)

# Pack the IPv4 packet
packed_data = ipv4_packet.pack()

# Unpack the IPv4 packet
unpacked_data = IPv4Packet(version, header_length, service_type, total_length, identification, flags, fragment_offset, time_to_live, protocol, header_checksum, source_ip, destination_ip, data)
unpacked_data.unpack(packed_data)

# Print the IPv4 packet details
print(ipv4_packet)
print(unpacked_data)
