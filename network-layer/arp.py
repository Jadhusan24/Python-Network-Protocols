import struct
import socket
import binascii

class ARPPacket:
    def __init__(self, hardware_type, protocol_type, hardware_size, protocol_size, opcode, sender_mac, sender_ip, target_mac, target_ip):
        self.hardware_type = hardware_type
        self.protocol_type = protocol_type
        self.hardware_size = hardware_size
        self.protocol_size = protocol_size
        self.opcode = opcode
        self.sender_mac = sender_mac
        self.sender_ip = sender_ip
        self.target_mac = target_mac
        self.target_ip = target_ip

    def pack(self):
        arp_packet = struct.pack("!HHBBH", self.hardware_type, self.protocol_type, self.hardware_size, self.protocol_size, self.opcode)
        arp_packet += binascii.unhexlify(self.sender_mac.replace(':', ''))
        arp_packet += socket.inet_aton(self.sender_ip)
        arp_packet += binascii.unhexlify(self.target_mac.replace(':', ''))
        arp_packet += socket.inet_aton(self.target_ip)
        return arp_packet

    def unpack(self, data):
        arp_fields = struct.unpack("!HHBBH", data[:8])
        self.hardware_type = arp_fields[0]
        self.protocol_type = arp_fields[1]
        self.hardware_size = arp_fields[2]
        self.protocol_size = arp_fields[3]
        self.opcode = arp_fields[4]
        self.sender_mac = ':'.join(format(x, '02x') for x in data[8:14])
        self.sender_ip = socket.inet_ntoa(data[14:18])
        self.target_mac = ':'.join(format(x, '02x') for x in data[18:24])
        self.target_ip = socket.inet_ntoa(data[24:28])

    def __str__(self):
        return f"Hardware Type: {self.hardware_type}, Protocol Type: {self.protocol_type}, Hardware Size: {self.hardware_size}, Protocol Size: {self.protocol_size}, Opcode: {self.opcode}, Sender MAC: {self.sender_mac}, Sender IP: {self.sender_ip}, Target MAC: {self.target_mac}, Target IP: {self.target_ip}"

# Example usage
hardware_type = 1  # Ethernet
protocol_type = 0x0800  # IPv4
hardware_size = 6  # MAC address size
protocol_size = 4  # IP address size
opcode = 1  # ARP request
sender_mac = "AA:BB:CC:DD:EE:FF"
sender_ip = "192.168.10.1"
target_mac = "11:22:33:44:55:66"
target_ip = "192.168.10.2"

# Create an ARP packet object
arp_packet = ARPPacket(hardware_type, protocol_type, hardware_size, protocol_size, opcode, sender_mac, sender_ip, target_mac, target_ip)

# Pack the ARP packet
packed_data = arp_packet.pack()

# Unpack the ARP packet
unpacked_data = ARPPacket(hardware_type, protocol_type, hardware_size, protocol_size, opcode, sender_mac, sender_ip, target_mac, target_ip)
unpacked_data.unpack(packed_data)

# Print the ARP packet details
print(arp_packet)
print(unpacked_data)
