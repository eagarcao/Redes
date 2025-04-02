import socket

direccion_http = "ec2-3-148-137-181.us-east-2.compute.amazonaws.com"
puerto_http = 8080

texto = open("rescatados.txt", "r")
pokemons = []

for e in texto:
    e = e.strip()
    pokemons.append(e)

texto.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((direccion_http, puerto_http))

    for pokemon in pokemons:
        peticion = f"GET /{pokemon} HTTP/1.1\r\nHost: {direccion_http}\r\n\r\n"
        s.send(peticion.encode())

        response = s.recv(4096).decode()
        print(f'SERVIDOR: {response}')
finally:
    s.close()