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
        if get_contracts(corp):
            time.sleep(60)
        else:
            time.sleep(1)

def get_contracts(corp):
    contracts = corp.corp_contracts(config.get('corporation','corporation_id'))
    #print(contracts)
    for contract in contracts:
        if contract.type == 'courier': # we only care about courier contracts
            newcontract = {}
            for k,v in contract.items():
                if k == 'type':
                    newcontract['contract_type'] = v
                elif k[0:5] == 'date_':
                    newcontract[k] = v.v
                else:
                    newcontract[k] = v
            print(newcontract)
            check_contract(newcontract)
        else:
            print('Not courier contract (%s)' % contract.type)
    return True

def check_contract(contract):
    print('Checking contract...')
    new_contract = False
    if not contract_status(contract['contract_id']):
        print('Contract not found in database, inserting...')
        add_contract(contract) # contract does not exist in the database, insert it
        if contract['status'] not in ['finished_issuer','finished_contractor','finished','cancelled','deleted']:
            print('New unfinished contract, sending new message')
            new_contract = True
            add_message(contract['contract_id'],'NEW')
    
    if new_contract or contract_status(contract['contract_id']) != contract['status']:
        # status of the contract has changed - work out what!
        if contract['status'] == 'in_progress':
            print('Sending accepted message...')
            add_message(contract['contract_id'], 'ACCEPTED')
        elif contract['status'] in ['finished_issuer','finished_contractor','finished']:
            print('Sending completed message...')
            add_message(contract['contract_id'], 'COMPLETED')
        elif contract['status'] in ['cancelled','deleted']:
            print('Sending deleted message...')
            add_message(contract['contract_id'], 'DELETED')
        elif contract['status'] == 'rejected':
            print('Sending rejected message...')
            add_message(contract['contract_id'], 'REJECTED')
        elif contract['status'] == 'failed':
            print('Sending failed message...')
            add_message(contract['contract_id'], 'FAILED')

        print('Updating contract in database')
        update_contract(contract)


if __name__ == '__main__':
    start()
