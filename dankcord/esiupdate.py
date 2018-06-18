#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import configparser

from .lib.database import *
from .lib.esi import ESI

config = configparser.SafeConfigParser()

def start(configpath="."):
    config.read("%s/config.ini" % configpath)
    corp = ESI(
        config.get('esi','client_id'),
        config.get('esi','secret_key'),
        config.get('esi','refresh_token'),
        config.get('esi','cache'),
        'corp'
    )
    while True:
        if get_contracts():
            time.sleep(60)
        else:
            time.sleep(1)

def get_contracts(corp):
    contracts = corp.esi.corp_contracts(config.get('corporation','corporation_id'))
    for contract in contracts.data:
        print contract
        #check_contract(contract)

def get_contracts_old():
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
