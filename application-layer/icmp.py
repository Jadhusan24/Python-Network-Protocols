import struct

class ICMPPacket:
    def __init__(self, icmp_type, code, checksum, data):
        self.icmp_type = icmp_type
        self.code = code
        self.checksum = checksum
        self.data = data

    def pack(self):
        icmp_packet = struct.pack('!BBH', self.icmp_type, self.code, self.checksum)
        icmp_packet += self.data
        return icmp_packet

    def unpack(self, data):
        icmp_fields = struct.unpack('!BBH', data[:4])
        self.icmp_type = icmp_fields[0]
        self.code = icmp_fields[1]
        self.checksum = icmp_fields[2]
        self.data = data[4:]

    def __str__(self):
        return f"ICMP Type: {self.icmp_type}, Code: {self.code}, Checksum: {self.checksum}, Data: {self.data}"

icmp_type = 8  # ICMP Echo Request
code = 0
checksum = 12345
data = b'This is ICMP data'

icmp_packet = ICMPPacket(icmp_type, code, checksum, data)

packed_data = icmp_packet.pack()

unpacked_data = ICMPPacket(icmp_type, code, checksum, data)
unpacked_data.unpack(packed_data)

print(icmp_packet)
print(unpacked_data)
