import discord
from discord.ext.commands import Bot
import response_handler


async def handle_message(message, user_message, private_message):
    try:
        response = response_handler.handle_response(user_message)
        if response:
            #  If the message is not empty
            await message.author.send(response) if private_message else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_bot_core(bot_config):
    bot_token = bot_config['token']

    bot_intents = discord.Intents.none()
    bot_intents.message_content = True
    bot_intents.messages = True
    bot_intents.dm_messages = True

    bot = Bot(
        command_prefix='/',
        intents=bot_intents,
        help_command=None,
    )

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is active!')

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author == bot.user or message.author.bot:
            return  # Don't respond to self or other bots

        username = str(message.author)
        message_contents = str(message.content)
        channel = str(message.channel)

        print(f'{username} said \"{message_contents}\" in ({channel})')

        #  private_message is currently unused
        await handle_message(message, message_contents, False)

    bot.run(token=bot_token)

