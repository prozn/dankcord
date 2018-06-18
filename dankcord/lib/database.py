from pony.orm import *
from decimal import Decimal
from datetime import datetime
import asyncio

DB = Database()
DB.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Contract(db.Entity):
	contract_id = PrimaryKey(int)
	acceptor_id = Optional(int) # monitor for changes
	assignee_id = Optional(int) 
	availability = Required(str,50) # filter = "personal" only
	collateral = Optional(Decimal, 20, 2)
	date_accepted = Optional(datetime)
	date_completed = Optional(datetime)
	date_expired = Optional(datetime)
	date_issued = Required(datetime)
	days_to_complete = Optional(int)
	end_location_id = Optional(int)
	for_corporation = Optional(bool)
	issuer_corporation_id = Optional(int)
	issuer_id = Optional(int)
	price = Optional(Decimal, 20, 2)
	reward = Optional(Decimal, 20, 2)
	start_location_id = Optional(int)
	status = Optional(str,50) # monitor for changes
	title = Optional(str,255)
	contract_type = Required(str, 50) # filter = "courier" only
	volume = Optional(Decimal, 20, 2)
	messages = Set('Messages')
	expiring_soon_sent = Required(bool,default=False)

class Messages(db.Entity):
	id = PrimaryKey(int, auto=True)
	contract_id = Required(Contract)
	reason = Required(str, 50)  # NEW, ACCEPTED, EXPIRING_SOON, COMPLETED, FAILED, REJECTED, DELETED

DB.generate_mapping(create_tables=True)

@db_session
async def contract_status(contract_id):
	try:
		contract = Contract[contract_id]
		return contract.status
	except ObjectNotFound:
		return false

@db_session
async def expiring_soon_sent(contract_id):
	try:
		contract = Contract[contract_id]
		return contract.expiring_soon_sent
	except ObjectNotFound:
		return false

@db_session
async def add_contract(contract):
	Contract(**contract)

@db_session
async def update_contract(contract):
	try:
		Contract[contract.contract_id].set(**contract)
		return true
	except ObjectNotFound:
		return false

@db_session
async def add_message(contract_id,reason):
	if reason in list('NEW','IN_PROGRESS','EXPIRING_SOON','COMPLETED','EXPIRED'):
		Messages(Contract[contract_id], reason)
	else:
		raise ValueError('Invalid reason code')