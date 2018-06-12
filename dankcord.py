import discord
import asyncio
import configparser
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
	client = discord.Client()

	@client.event
	async def on_ready():
	    print('Logged in as')
	    print(client.user.name)
	    print(client.user.id)
	    print('------')

	@client.event
	async def on_message(message):
	    if message.content.startswith('!contracts'):
	    	op = app.op['get_corporations_corporation_id_contracts'](
	    		corporation_id=config.get('corporation','corporation_id')
	    	)
	    	contracts = client.request(op)
	    	print(contracts.data)
	    	await client.send_message(message.channel, 'Printed contracts data to console...')

	client.run('NDU2MTg0NzQ1NTYzMzg5OTUz.DgG2qw.uo1GvEdehKFJ_2nLjDklkcOhu_0')

if __name__ == '__main__':
	launchesi()
	startbot()

