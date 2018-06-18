from pony.orm import *
from decimal import Decimal
from datetime import datetime


db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Contract(db.Entity):
	contract_id = PrimaryKey(int, 20)
	acceptor_id = Optional(int, 20) # monitor for changes
	assignee_id = Optional(int, 20) 
	availability = Required(str,50) # filter = "personal" only
	collateral = Optional(Decimal, 20, 2)
	date_accepted = Optional(datetime)
	date_completed = Optional(datetime)
	date_expired = Optional(datetime)
	date_issued = Required(datetime)
	days_to_complete = Optional(int, 3)
	end_location_id = Optional(int, 20)
	for_corporation = Optional(bool)
	issuer_corporation_id = Optional(int, 20)
	issuer_id = Optional(int, 20)
	price = Optional(Decimal, 20, 2)
	reward = Optional(Decimal, 20, 2)
	start_location_id = Optional(int, 20)
	status = Optional(str,50) # monitor for changes
	title = Optional(str,255)
	contract_type = Required(str, 50) # filter = "courier" only
	volume = Optional(Decimal, 20, 2)
	messages = Set('Messages')

class Messages(db.Entity):
	id = PrimaryKey(int, auto=True)
	contract_id = Required(Contract)
	reason = Required(str, 50)  # NEW, ACCEPTED, EXPIRING_SOON, COMPLETED, EXPIRED

db.generate_mapping(create_tables=True)

@db_session
async def contract_exists(contract_id):
	try:
		contract = Contract[contract_id]
		return true
	except ObjectNotFound:
		return false

@db_session
async def update_contract(c):
	if contract_exists(c.contract_id):
		Contract[c.contract_id].set(**c)
	else:
		Contract(**c)