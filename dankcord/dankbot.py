import discord
from discord.ext import commands
import asyncio
import configparser
from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.cache import FileCache

config = configparser.SafeConfigParser()

def launchesi(configpath="."):
    global app, security, esi
    config.read("%s/config.ini" % configpath)
    cache = FileCache(path=config.get('esi','cache'))
    esi_app = EsiApp(cache=cache)
    app = esi_app.get_latest_swagger
    security = EsiSecurity(
        app=app,
        redirect_uri='http://localhost/oauth-callback', # This doesnt matter
        client_id=config.get('esi','client_id'),
        secret_key=config.get('esi','secret_key'),
    )
    esi = EsiClient(
        retry_requests=True,  # set to retry on http 5xx error (default False)
        header={'User-Agent': 'Discord bot by Prozn: https://github.com/prozn/dankcord'},
        security=security
    )
    security.update_token({
        'access_token': '',  # leave this empty
        'expires_in': -1,  # seconds until expiry, so we force refresh anyway
        'refresh_token': config.get('esi','refresh_token')
    })
    security.refresh()

def startbot():
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

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @bot.command()
    async def contracts(ctx):
        op = app.op['get_corporations_corporation_id_contracts'](
            corporation_id=config.get('corporation','corporation_id')
        )
        contracts = esi.request(op)
        print(contracts.data)
        #await ctx.send('Printed contracts data to console...')

    @bot.command()
    async def askdrake(ctx):
        from random import randint
        emojis = bot.emojis()
        print(emojis)
        if randint(1,2) == 1:
            await ctx.send(':drakeyes:')
        else:
            await ctx.send(':drakeno:')


    bot.loop.create_task(get_contracts())
    bot.run(config.get('discord','bot_token'))