import discord
from discord.ext import commands
import asyncio
import configparser
from .lib.database import *

config = configparser.SafeConfigParser()
bot_is_ready = False

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
        if bot_is_ready == True:
            message = pop_message()
            print(message)
        else:
            print('Bot not ready, waiting...')
        await asyncio.sleep(1)

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        bot_is_ready = True

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