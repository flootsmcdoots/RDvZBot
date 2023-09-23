import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot

import command_handler


#  With thanks to https://github.com/kkrypt0nn/Python-Discord-Bot-Template/ for code guidance

def run_bot_core(bot_config):
    bot_token = bot_config['token']

    bot_intents = discord.Intents.none()
    bot_intents.message_content = True
    bot_intents.messages = True
    bot_intents.dm_messages = True
    bot_intents.guilds = True

    bot_updates_channel_id = bot_config['update_channel_id']
    update_frequency = float(bot_config['update_frequency'])
    if update_frequency < 0.1:
        print("Update Frequency is too low (below 0.1)! Setting to 0.1...")
        update_frequency = 0.1

    bot = Bot(
        command_prefix="!",
        intents=bot_intents,
        help_command=commands.DefaultHelpCommand(),
    )
    # TODO: Input validation on config (like embed colors should be in the form of color/keyword objects)
    bot_response_handler = command_handler.ServerUpdateChecker(bot_config['host'], bot_config['port'],
                                                               update_frequency=update_frequency,
                                                               embed_color_list=bot_config['embed-colors'])

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is active!')
        update_channel = bot.get_channel(int(bot_updates_channel_id))
        list_server_status.start(update_channel=update_channel)
        print(f"Started periodic update with frequency of {update_frequency} minutes!")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author == bot.user or message.author.bot:
            return  # Don't respond to self or other bots

        await bot.process_commands(message)

    @tasks.loop(minutes=update_frequency)
    async def list_server_status(update_channel: discord.TextChannel) -> None:
        if update_channel:  # If not none, run other code
            # Retrieve last message, if it's written by this bot, and it's an embed, let's edit it
            last_message_id = update_channel.last_message_id
            last_message: discord.Message = await update_channel.fetch_message(last_message_id)
            if last_message.author == bot.user and last_message.embeds:
                await last_message.edit(embed=bot_response_handler.get_periodic_update(update_channel))
            else:
                # Otherwise send a new message
                await update_channel.send(embed=bot_response_handler.get_periodic_update(channel=update_channel))
                pass
        else:
            print("Failed to find update channel! (Wrong or missing id?)")

    @bot.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def info(ctx):
        await ctx.send(command_handler.handle_info())

    bot.run(token=bot_token)


async def handle_message(bot_response_handler: command_handler.ServerUpdateChecker, message, user_message,
                         private_message):
    try:
        response = bot_response_handler.handle_response(user_message)
        if response:
            #  If the message is not empty
            await message.author.send(response) if private_message else await message.channel.send(response)
    except Exception as e:
        print(e)
