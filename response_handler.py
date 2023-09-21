import random
from datetime import datetime

import discord
from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse


#  https://github.com/py-mine/mcstatus

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


class BotResponseHandler:
    def __init__(self, host, port, update_frequency):
        self.hostaddress = "{host}:{port}".format(host=host, port=port)
        self.update_frequency = update_frequency

    def handle_response(self, message: str) -> str:
        processed_message = message.lower()

        if processed_message == 'hello':
            return "Hello World!"

        if processed_message == 'roll':
            return str(random.randint(1, 6))

        if processed_message == 'info':
            return "Code: https://github.com/GreatWyrm/NightfallBot"

        if processed_message == 'status':
            nf_server = JavaServer.lookup(self.hostaddress)
            return parse_server_status(nf_server.status())

        if processed_message == 'players':
            nf_server = JavaServer.lookup(self.hostaddress)
            return parse_server_players(nf_server.status())

        if processed_message == 'top 500':
            return "The only top 500 NF player is Hatsune Miku (and maybe LadyLunch)"

        return ""

    def get_periodic_update(self, channel: discord.TextChannel) -> discord.Embed:
        nf_server = JavaServer.lookup(self.hostaddress)
        status = nf_server.status()
        server_version = status.version.name
        motd_lowercase = status.motd.to_plain().lower()
        player_list = status.players
        color = 0xFFFFFF
        if "starting soon" in motd_lowercase:
            color = 0x7a7979
        elif "fallen" in motd_lowercase:
            color = 0x0a0a0a
        elif "build phase" in motd_lowercase:
            color = 0x08c40e
        elif "shrine" in motd_lowercase:
            color = 0x920be0

        embed = discord.Embed(title=f"Nightfall - {server_version}", color=color, description=status.motd.to_plain())
        embed.set_author(name="Nightfall Bot")
        embed.set_thumbnail(url=channel.guild.icon.url)
        update_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        embed.set_footer(text=f"Updated on {update_time}. Updates {self.update_frequency} minute(s).")
        embed.add_field(name="Players Online", value=f"{player_list.online}/{player_list.max}")

        return embed
