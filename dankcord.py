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

class Dankcord(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task_contracts = self.loop.create_task(self.get_contracts())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.ping_channel_id = discord.utils.get(client.get_all_channels(), guild__name='BBW.', name='test')
        print('Using ping channel id %s' % format(self.ping_channel_id))
        print('------')

    async def get_contracts(self):
        await self.wait_until_ready()
        channel = self.get_channel(self.ping_channel_id) # channel ID goes here
        while not self.is_closed():
            await channel.send("this would be a message if there were new contracts")
            await asyncio.sleep(60) # task runs every 60 seconds

    async def on_message(self, message):
        if message.content.startswith('!contracts'):
            await self.respond_contracts(message)

    async def respond_contracts(message):
        op = app.op['get_corporations_corporation_id_contracts'](
            corporation_id=config.get('corporation','corporation_id')
        )
        contracts = esi.request(op)
        print(contracts.data)
        await message.channel.send('Printed contracts data to console...')

def startbot():
    bot = Dankcord()
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
