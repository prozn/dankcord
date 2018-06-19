from pony.orm import *
from decimal import Decimal
from datetime import datetime
import asyncio

DB = Database()
DB.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Contract(DB.Entity):
	contract_id = PrimaryKey(int)
	acceptor_id = Optional(int, size=64) # monitor for changes
	assignee_id = Optional(int, size=64)
	availability = Required(str,50) # filter = "personal" only
	collateral = Optional(Decimal, 20, 2)
	date_accepted = Optional(datetime)
	date_completed = Optional(datetime)
	date_expired = Optional(datetime)
	date_issued = Required(datetime)
	days_to_complete = Optional(int)
	end_location_id = Optional(int, size=64)
	for_corporation = Optional(bool)
	issuer_corporation_id = Optional(int, size=64)
	issuer_id = Optional(int, size=64)
	price = Optional(Decimal, 20, 2)
	reward = Optional(Decimal, 20, 2)
	start_location_id = Optional(int, size=64)
	status = Optional(str,50) # monitor for changes
	title = Optional(str,255)
	contract_type = Required(str, 50) # filter = "courier" only
	volume = Optional(Decimal, 20, 2)
	messages = Set('Message')
	expiring_soon_sent = Required(bool,default=False)

class Message(DB.Entity):
	id = PrimaryKey(int, auto=True)
	contract_id = Required(Contract)
	reason = Required(str, 50)  # NEW, ACCEPTED, EXPIRING_SOON, COMPLETED, FAILED, REJECTED, DELETED
	sent = Required(bool,default=False)

class CharCorp(DB.Entity):
	id = PrimaryKey(int)
	name = Required(str,255)

class Location(DB.Entity):
	location_id = PrimaryKey(int, size=64)
	name = Required(str,255)
	system_id = Required(int, size=64)

class System(DB.Entity):
	system_id = PrimaryKey(int)
	name = Required(str,255)

DB.generate_mapping(create_tables=True)

@db_session
def contract_status(contract_id):
	try:
		contract = Contract[contract_id]
		return contract.status
	except ObjectNotFound:
		return False

@db_session
def expiring_soon_sent(contract_id):
	try:
		contract = Contract[contract_id]
		return contract.expiring_soon_sent
	except ObjectNotFound:
		return False

def update_expiring_soon(contract_id):
	try:
		Contract[contract_id].set(expiring_soon_sent=True)
		return True
	except ObjectNotFound:
		return False

@db_session
def add_contract(contract):
	Contract(**contract)

@db_session
def update_contract(contract):
	try:
		Contract[contract['contract_id']].set(**contract)
		return True
	except ObjectNotFound:
		return False

@db_session
def add_message(contract_id,reason):
	if reason in ['NEW','IN_PROGRESS','EXPIRING_SOON','COMPLETED','EXPIRED']:
		Message(contract_id=Contract[contract_id], reason=reason)
	else:
		raise ValueError('Invalid reason code')

@db_session
def pop_message():
	mess = Message.select(lambda m: m.sent == False).order_by(lambda m: m.id)[:1]
	if len(mess) > 0:
		item = mess[0].to_dict(related_objects=True, with_collections=True)
		cont = mess[0].contract_id.to_dict()
		item['contract'] = cont
		del item['contract_id']
		Message[mess[0].id].set(sent=True)
		return item
	else:
		return False

@db_session
def get_charcorp_name(character_id):
	try:
		char = CharCorp[character_id]
		return char.name
	except ObjectNotFound:
		return 'Unknown Character or Corporation'

def get_location_name(location_id):
	try:
		loc = Location[location_id]
		return loc.name
	except ObjectNotFound:
		return 'Unknown Structure'

def get_system_name(system_id):
	try:
		system = System[system_id]
		return system.name
	except ObjectNotFound:
		return 'Unknown System'

@db_session
def get_or_create_charcorp(esi_instance,id):
	try:
		char = CharCorp[id]
		return char.to_dict()
	except ObjectNotFound:
		charname = esi_instance.id_name(id)
		CharCorp(id=id, name=charname)
		return CharCorp[id].to_dict()

@db_session
def get_or_create_location(esi_instance,location_id):
	try:
		loc = Location[location_id]
		return loc.to_dict()
	except ObjectNotFound:
		loc = esi_instance.location_details(location_id)
		Location(location_id=location_id, name=loc['name'], system_id=loc['system_id'])
		get_or_create_system(esi_instance,loc['system_id'])
		return Location[location_id].to_dict()

@db_session
def get_or_create_system(esi_instance,system_id):
	try:
		system = System[system_id]
		return system.to_dict()
	except ObjectNotFound:
		system = esi_instance.get_system_name(system_id)
		System(system_id=system_id, name=system)
		return System[system_id].to_dict()

@db_session
def update_contract_fluff(esi_instance,contract_id):
	try:
		contract = Contract[contract_id]
		get_or_create_location(esi_instance,contract.start_location_id)
		get_or_create_location(esi_instance,contract.end_location_id)
		if contract.acceptor_id != 0:
			get_or_create_charcorp(esi_instance,contract.acceptor_id)
		if contract.assignee_id != 0:
			get_or_create_charcorp(esi_instance,contract.assignee_id)
		if contract.issuer_id != 0:
			get_or_create_charcorp(esi_instance,contract.issuer_id)
	except ObjectNotFound:
		return False