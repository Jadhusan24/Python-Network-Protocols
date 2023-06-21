import struct
import binascii

class macaddr:
    def __init__(self, source_mac, destination_mac):
        self.source_mac = source_mac
        self.destination_mac = destination_mac

    def pack(self):
        mac_header = struct.pack('!6s6s',
                                 binascii.unhexlify(self.destination_mac.replace(':', '')),
                                 binascii.unhexlify(self.source_mac.replace(':', '')))
        return mac_header

    def unpack(self, data):
        mac_fields = struct.unpack('!6s6s', data)
        self.destination_mac = ':'.join(format(x, '02x') for x in mac_fields[0])
        self.source_mac = ':'.join(format(x, '02x') for x in mac_fields[1])

    def __str__(self):
        return f"Source MAC: {self.source_mac}, Destination MAC: {self.destination_mac}"

source_mac = "AA:BB:CC:DD:EE:FF"
destination_mac = "11:22:33:44:55:66"

mac_header = macaddr(source_mac, destination_mac)

packed_data = mac_header.pack()

unpacked_data = macaddr(source_mac, destination_mac)
unpacked_data.unpack(packed_data)

print(mac_header)
print(unpacked_data)
