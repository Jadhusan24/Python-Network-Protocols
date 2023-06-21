import struct

class HTTPPacket:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def pack(self):
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        headers = ""
        for header, value in self.headers.items():
            headers += f"{header}: {value}\r\n"
        http_packet = f"{request_line}{headers}\r\n{self.body}"
        return http_packet.encode('utf-8')

    def unpack(self, data):
        http_lines = data.decode('utf-8').split('\r\n')
        request_line = http_lines[0]
        self.method, self.path, _ = request_line.split(' ')
        self.headers = {}
        header_lines = http_lines[1:-2]
        for line in header_lines:
            header, value = line.split(': ')
            self.headers[header] = value
        self.body = http_lines[-1]

    def __str__(self):
        return f"Method: {self.method}, Path: {self.path}, Headers: {self.headers}, Body: {self.body}"

method = "GET"
path = "/index.html"
headers = {"Host": "www.example.com", "User-Agent": "Mozilla/5.0"}
body = ""

http_packet = HTTPPacket(method, path, headers, body)

packed_data = http_packet.pack()

unpacked_data = HTTPPacket(method, path, headers, body)
unpacked_data.unpack(packed_data)

print(http_packet)
print(unpacked_data)
