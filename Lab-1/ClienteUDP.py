import asyncio

pokemon_buscando = {"Rattata", "Raticate", "Pidgeot", "Pidgeotto"}

class ClienteUDP(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.rescatados = []
        self.ultimo_recibido = asyncio._get_running_loop().time()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        mensaje = data.decode().strip()
        print(f'Servidor: {mensaje}')

        self.ultimo_recibido = asyncio.get_event_loop().time()
        palabras = mensaje.split(";")

        for e in palabras:
            if e  in pokemon_buscando and e not in self.rescatados:
                self.rescatados.append(e)

    def enviar_mensaje(self, mensaje):  # Eliminé host y port
        self.transport.sendto(mensaje.encode())  # Enviar directamente porque ya está configurado el remote_addr


async def main(etiqueta, puerto):
    HOST = 'ec2-3-148-137-181.us-east-2.compute.amazonaws.com'  # Dirección IP del servidor
    
    loop = asyncio.get_running_loop()
    transport, protocolo = await loop.create_datagram_endpoint(
        lambda: ClienteUDP(),
        remote_addr=(HOST, puerto)
    )

    try:
        tag = etiqueta
        mensaje_inicial = f'{tag}:Hola!'
        protocolo.enviar_mensaje(mensaje_inicial)

        while True:
            await asyncio.sleep(0.1) 
            tiempo_actual = loop.time()
            if tiempo_actual - protocolo.ultimo_recibido > 10:
                break

    except KeyboardInterrupt:
        print("Cerrando cliente.")
    finally:
        transport.close()

    texto = open("rescatados.txt", "w")

    for pokemon in protocolo.rescatados:
        texto.write(pokemon + "\n")
    
    texto.close()
