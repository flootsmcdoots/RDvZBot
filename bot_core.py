import discord
from discord.ext import tasks
from discord.ext.commands import Bot
import response_handler


#  With thanks to https://github.com/kkrypt0nn/Python-Discord-Bot-Template/ for code guidance

def run_bot_core(bot_config):
    bot_token = bot_config['token']

    bot_intents = discord.Intents.none()
    bot_intents.message_content = True
    bot_intents.messages = True
    bot_intents.dm_messages = True
    bot_intents.guilds = True

    bot_updates_channel_id = bot_config['update_channel_id']

    bot = Bot(
        command_prefix='/',
        intents=bot_intents,
        help_command=None,
    )

    bot_response_handler = response_handler.BotResponseHandler(bot_config['host'], bot_config['port'])

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is active!')
        update_channel = bot.get_channel(int(bot_updates_channel_id))
        list_server_status.start(update_channel=update_channel)
        print("Started periodic update!")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author == bot.user or message.author.bot:
            return  # Don't respond to self or other bots

        message_contents = str(message.content)
        print()

        #  private_message is currently unused
        await handle_message(bot_response_handler, message, message_contents, False)

    @tasks.loop(minutes=1.0)
    async def list_server_status(update_channel: discord.TextChannel) -> None:
        if update_channel:  # If not none, run other code
            await update_channel.send(embed=bot_response_handler.get_periodic_update(channel=update_channel))
        else:
            print("Failed to find update channel! (Wrong or missing id?)")

    bot.run(token=bot_token)


async def handle_message(bot_response_handler: response_handler.BotResponseHandler, message, user_message,
                         private_message):
    try:
        response = bot_response_handler.handle_response(user_message)
        if response:
            #  If the message is not empty
            await message.author.send(response) if private_message else await message.channel.send(response)
    except Exception as e:
        print(e)
