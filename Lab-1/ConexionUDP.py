import asyncio


class ClienteUDP(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f'Servidor: {data.decode()}')

    def enviar_mensaje(self, mensaje):  # Eliminé host y port
        self.transport.sendto(mensaje.encode())  # Enviar directamente porque ya está configurado el remote_addr


async def main():
    HOST = 'ec2-3-148-137-181.us-east-2.compute.amazonaws.com'  # Dirección IP del servidor
    PORT = 49968  # Puerto del servidor UDP

    loop = asyncio.get_running_loop()
    transport, protocolo = await loop.create_datagram_endpoint(
        lambda: ClienteUDP(),
        remote_addr=(HOST, PORT)
    )

    try:
        tag = "TAG4075"
        mensaje_inicial = f'{tag}:Hola!'
        protocolo.enviar_mensaje(mensaje_inicial)

        # Mantener el cliente escuchando permanentemente
        while True:
            await asyncio.sleep(0.1)  # Permitir que asyncio procese eventos

    finally:
        transport.close()



asyncio.run(main())
