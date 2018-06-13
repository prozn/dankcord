import discord
from discord.ext import commands
import asyncio
import configparser
import logging
import logging.handlers
from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity

config = configparser.SafeConfigParser()

def launchesi(configpath="."):
    global app, security, esi
    config.read("%s/config.ini" % configpath)
    app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
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
        await ctx.send('Printed contracts data to console...')

    bot.run(config.get('discord','bot_token'))

if __name__ == '__main__':
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    launchesi()
    startbot()
