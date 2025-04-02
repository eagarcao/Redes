import socket
import re
import asyncio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion = "ec2-3-148-137-181.us-east-2.compute.amazonaws.com"
puerto_tcp = 12345

grupo = "Grupo5"
clave_grupo = "D3e4F" #cambiar si es que responden que es por teclado

try:
    s.connect((direccion, puerto_tcp))
    s.send(grupo.encode())

    response = s.recv(1024).decode().strip()
    print(f'SERVIDOR:{response}')

    s.send(clave_grupo.encode())
    response = s.recv(1024).decode().strip()
    print(f'SERVIDOR:{response}')

    encontrarTag = re.search(r'Etiqueta: (TAG\d+)', response)
    encontrarPuerto = re.search(r'Puerto UDP: (\d+)', response)

    if encontrarTag and encontrarPuerto:
        tag = encontrarTag.group(1)
        puerto = int(encontrarPuerto.group(1))
finally:
    s.close()

async def pasar_datos():
    from ClienteUDP import main
    await main(tag, puerto)

asyncio.run(pasar_datos())