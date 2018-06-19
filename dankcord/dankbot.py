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

    async def get_contracts():
        print("I'm in the get contracts function")
        await bot.wait_until_ready()
        print("Bot is ready")
        guild = discord.utils.get(bot.guilds, name='BBW.')
        if guild is not None:
            channel = discord.utils.get(guild.text_channels, name='test')
            while not bot.is_closed():
                print("Sending message...")
                #await channel.send('This would be a new contract alert')
                await asyncio.sleep(300) # task runs every 60 seconds
        else:
            print("Couldn't find server, not starting contracts task. You should probably fix this.")

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
        text = ""
        e = discord.Embed()
        if message['reason'] == 'NEW':
            #e = discord.Embed(title='New contract received!')
            e.title = "New contract received!"
            e.add_field(name="From", value=get_location_system_name(message['contract']['start_location_id']), inline=True)
            e.add_field(name="To", value=get_location_system_name(message['contract']['end_location_id']), inline=True)
            e.add_field(name="Volume", value=format_number(message['contract']['volume']), inline=True)
            e.add_field(name="Collateral", value=format_money(message['contract']['collateral']), inline=True)
            e.add_field(name="Reward", value=format_money(message['contract']['reward']), inline=True)
            e.add_field(name="isk/m3", value=format_number(round(message['contract']['reward']/message['contract']['volume'],2)), inline=True)
            e.add_field(name="Issued By", value=get_charcorp_name(message['contract']['issuer_id']), inline=True)
        elif message['reason'] == 'IN_PROGRESS':
            e = discord.Embed(title='Contract has been accepted by %s' % get_charcorp_name(message['contract']['acceptor_id']))
            e.add_field(name="From", value=get_location_system_name(message['contract']['start_location_id']), inline=True)
            e.add_field(name="To", value=get_location_system_name(message['contract']['end_location_id']), inline=True)
            e.add_field(name="Volume", value=format_number(message['contract']['volume']), inline=True)
            e.add_field(name="Collateral", value=format_money(message['contract']['collateral']), inline=True)
            e.add_field(name="Reward", value=format_money(message['contract']['reward']), inline=True)
            e.add_field(name="isk/m3", value=format_number(round(message['contract']['reward']/message['contract']['volume'],2)), inline=True)
            e.add_field(name="Issued By", value=get_charcorp_name(message['contract']['issuer_id']), inline=True)
        elif message['reason'] == 'EXPIRING_SOON':
            return True
        elif message['reason'] == 'COMPLETED':
            return True
        elif message['reason'] == 'EXPIRED':
            return True
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