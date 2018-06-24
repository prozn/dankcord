import discord
from discord.ext import commands
import asyncio
import configparser
from .lib.database import *
from .lib.utils import *

config = configparser.SafeConfigParser()

def startbot(configpath="."):
    config.read("%s/config.ini" % configpath)

    command_prefix='!'
    bot = commands.Bot(command_prefix)

    async def check_for_messages():
        await bot.wait_until_ready()
        while not bot.is_closed():
            message = pop_message()
            if message is not False:
                await process_message(message)
            await asyncio.sleep(1)

    async def process_message(message):
        guild = discord.utils.get(bot.guilds, name='BBW.')
        channel = discord.utils.get(guild.text_channels, name='test')
        text = "@everyone"
        e = discord.Embed()
        e.add_field(name="From", value=get_location_system_name(message['contract']['start_location_id']), inline=True)
        e.add_field(name="To", value=get_location_system_name(message['contract']['end_location_id']), inline=True)
        e.add_field(name="Volume", value=format_number(message['contract']['volume']), inline=True)
        e.add_field(name="Collateral", value=format_money(message['contract']['collateral']), inline=True)
        e.add_field(name="Reward", value=format_money(message['contract']['reward']), inline=True)
        e.add_field(name="isk/m3", value=format_number(round(message['contract']['reward']/message['contract']['volume'],2)), inline=True)
        e.add_field(name="Issued By", value=get_charcorp_name(message['contract']['issuer_id']), inline=True)
        if message['reason'] == 'NEW':
            e.title = "New contract received!"
        elif message['reason'] == 'IN_PROGRESS':
            e.title = "Contract has been accepted by %s" % get_charcorp_name(message['contract']['acceptor_id'])
        elif message['reason'] == 'EXPIRING_SOON':
            e.title = "The following contact is expiring soon!"
        elif message['reason'] == 'COMPLETED':
            e.title = "The following contract has been completed by %s" % get_charcorp_name(message['contract']['acceptor_id'])
        elif message['reason'] == 'EXPIRED':
            e.title = "The following contract has expired!"
        elif message['reason'] == 'DELETED':
            e.title = "The following contract has been deleted!"
        else:
            print('message type unknown')
            return False

        await channel.send(text, embed=e)

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @bot.command()
    async def askdrake(ctx):
        from random import randint
        emojis = bot.emojis
        print(emojis)
        if randint(1,2) == 1:
            await ctx.send(discord.utils.get(emojis, name='drakeyes'))
        else:
            await ctx.send(discord.utils.get(emojis, name='drakeno'))

    bot.loop.create_task(check_for_messages())
    bot.run(config.get('discord','bot_token'))