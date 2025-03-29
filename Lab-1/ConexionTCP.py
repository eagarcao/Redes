import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion = "ec2-3-148-137-181.us-east-2.compute.amazonaws.com"
puerto_tcp = 12345

grupo = "Grupo5"
clave_grupo = "D3e4F"


s.connect((direccion, puerto_tcp))
s.send(grupo.encode())

response = s.recv(1024).decode()
print('SERVIDOR\n', response)

s.send(clave_grupo.encode())
response = s.recv(1024).decode()
print('SERVIDOR\n', response)

s.close()