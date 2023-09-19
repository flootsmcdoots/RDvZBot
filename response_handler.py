import random
from mcstatus import JavaServer

#  https://github.com/py-mine/mcstatus


def handle_response(message: str) -> str:
    processed_message = message.lower()

    if processed_message == 'hello':
        return "Hello World!"

    if processed_message == 'roll':
        return str(random.randint(1, 6))

    if processed_message == 'info':
        return "Arcane Made This!"

    if processed_message == 'status':
        nf_server = JavaServer.lookup("play.mcnightfall.com:25565")
        status = nf_server.status()
        print(status)
        return ""

    return ""
