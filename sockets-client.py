import socket

HOST, PORT = '', 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

client_host, client_port = sock.getsockname()[:2]

print(client_host, client_port)

sock.sendall(b'test')
data = sock.recv(1024)

print(data.decode())
