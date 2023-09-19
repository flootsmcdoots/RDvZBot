import random
from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse


#  https://github.com/py-mine/mcstatus


def handle_response(message: str) -> str:
    processed_message = message.lower()

    if processed_message == 'hello':
        return "Hello World!"

    if processed_message == 'roll':
        return str(random.randint(1, 6))

    if processed_message == 'info':
        return "Code: https://github.com/GreatWyrm/NightfallBot"

    if processed_message == 'status':
        nf_server = JavaServer.lookup("play.mcnightfall.com:25565")
        return parse_server_status(nf_server.status())

    if processed_message == 'players':
        nf_server = JavaServer.lookup("play.mcnightfall.com:25565")
        return parse_server_players(nf_server.status())

    if processed_message == 'top 500':
        return "The only top 500 NF player is Hatsune Miku (and maybe LadyLunch)"

    return ""


def parse_server_status(status: JavaStatusResponse) -> str:
    latency = status.latency
    server_version = status.version.name
    player_list = status.players
    motd = status.motd.to_plain()

    return (f'Version: {server_version}\n'
            f'Latency: {round(latency)} ms\n'
            f'Players Online: {player_list.online}/{player_list.max}\n'
            f'{motd}')


def parse_server_players(status: JavaStatusResponse) -> str:
    player_list = status.players
    ret_val = f'Players Online: {player_list.online}/{player_list.max}\n'

    if player_list.sample:  # Is not None
        for player in player_list.sample:
            sample_str = "Username: {name}, UUID: {uuid}\n".format(name=player.name, uuid=player.uuid)
            ret_val = ret_val + sample_str

    return ret_val
