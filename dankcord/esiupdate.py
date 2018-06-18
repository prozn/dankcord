#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pony
from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.cache import FileCache
import configparser

config = configparser.SafeConfigParser()

def start(configpath="."):
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
        headers={'User-Agent': 'Discord bot by Prozn: https://github.com/prozn/dankcord'},
        security=security
    )
    security.update_token({
        'access_token': '',  # leave this empty
        'expires_in': -1,  # seconds until expiry, so we force refresh anyway
        'refresh_token': config.get('esi','refresh_token')
    })
    security.refresh()

    while True:
        if get_contracts():
            time.sleep(60)
        else:
            time.sleep(1)

def get_contracts():
    op = app.op['get_corporations_corporation_id_contracts'](
        corporation_id=config.get('corporation','corporation_id')
    )
    contracts = esi.request(op,raise_on_error=True)
    for contract in contracts.data:
        contract['iskm3'] = contract.reward / contract.volume
        print(contract);
        #print("%s : %s -- %s -- %s -- %s (%s)" % (contract.type, contract.contract_id, contract.date_issued, contract.volume, contract.reward, contract.iskm3))
    return True

if __name__ == '__main__':
    start()
