from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Contract(db.Entity):
	contract_id = PrimaryKey(int, 20)
	acceptor_id = Optional(int, 20)
	assignee_id = Optional(int, 20)
	availability = Required(str,50)
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
	status = Optional(str,50)
	title = Optional(str,255)
	contract_type = Required(str, 50)
	volume = Optional(Decimal, 20, 2)

	db.generate_mapping(create_tables=True)

@db_session
async def contract_exists(contract_id):
	try:
		contract = Customer[contract_id]
		return true
	except ObjectNotFound:
		return false