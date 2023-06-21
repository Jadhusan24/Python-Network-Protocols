import struct
import binascii

class EthernetFrame:
    def __init__(self, source_mac, destination_mac, ethertype, data):
        self.source_mac = source_mac
        self.destination_mac = destination_mac
        self.ethertype = ethertype
        self.data = data

    def pack(self):
        ethernet_frame = struct.pack('!6s6sH',
                                     binascii.unhexlify(self.destination_mac.replace(':', '')),
                                     binascii.unhexlify(self.source_mac.replace(':', '')),
                                     self.ethertype)
        ethernet_frame += self.data
        return ethernet_frame

    def unpack(self, data):
        eth_fields = struct.unpack('!6s6sH', data[:14])
        self.destination_mac = ':'.join(format(x, '02x') for x in eth_fields[0])
        self.source_mac = ':'.join(format(x, '02x') for x in eth_fields[1])
        self.ethertype = eth_fields[2]
        self.data = data[14:]

    def __str__(self):

        return f"Source MAC: {self.source_mac}, Destination MAC: {self.destination_mac}, EtherType: {self.ethertype}, Data: {self.data}"

source_mac = "AA:BB:CC:DD:EE:FF"
destination_mac = "11:22:33:44:55:66"
ethertype = 0x0800 
data = b'\x45\x00\x00\x1e\x00\x00\x40\x00\x40\x11\xb8\xea\xc0\xa8\x01\x01\xc0\xa8\x01\x02'

eth_frame = EthernetFrame(source_mac, destination_mac, ethertype, data)


packed_data = eth_frame.pack()

unpacked_data = EthernetFrame(source_mac, destination_mac, ethertype, data)
unpacked_data.unpack(packed_data)

print(eth_frame)
print(unpacked_data)
