#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from esipy import EsiApp
from esipy import EsiClient
import configparser

def start():
	global app, security, esi
	config.read("%s/config.ini" % configpath)
	esi_app = EsiApp()
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

if __name__ == '__main__':
	start()