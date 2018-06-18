from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.cache import FileCache
import asyncio

class ESI:
    def __init__(self,client_id,secret_key,refresh_token,cache_path,prefix='esipy'):
        self.client_id = client_id
        self.secret_key = secret_key
        self.refresh_token = refresh_token
        self.cache_path = cache_path
        self.prefix = prefix

        self._start()

    def _start(self):
        self.cache = FileCache(path=self.cache_path)
        self.esi_app = EsiApp(cache=self.cache, cache_prefix=self.prefix)
        self.app = self.esi_app.get_latest_swagger
        self.security = EsiSecurity(
            app=self.app,
            redirect_uri='http://localhost/oauth-callback', # This doesnt matter
            headers={'User-Agent': 'Discord bot by Prozn: https://github.com/prozn/dankcord'},
            client_id=self.client_id,
            secret_key=self.secret_key,
        )
        self.esi = EsiClient(
            retry_requests=True,  # set to retry on http 5xx error (default False)
            headers={'User-Agent': 'Discord bot by Prozn: https://github.com/prozn/dankcord'},
            security=self.security
        )
        self.security.update_token({
            'access_token': '',  # leave this empty
            'expires_in': -1,  # seconds until expiry, so we force refresh anyway
            'refresh_token': self.refresh_token
        })
        self.security.refresh()

    def character_info(self, character_id):
        op = self.app.op['get_characters_character_id'](
            character_id=character_id
        )
        character = self.esi.request(op,raise_on_error=True)
        return character

    def character_name(self, character_id):
        character = self.character_info(character_id)
        return character.name

    def corp_contracts(self, corporation_id, raw=False):
        op = self.app.op['get_corporations_corporation_id_contracts'](
            corporation_id=corporation_id
        )
        contracts = self.esi.request(op,raise_on_error=True, raw_body_only=raw)
        if raw:
            return contracts.raw
        else:
            return contracts.data

    def get_system_name(self, system_id):
        op = self.app.op['get_universe_systems_system_id'](
            system_id=system_id
        )
        system = self.esi.request(op,raise_on_error=True)
        return system.data.name

    def location_details(self, location_id):
        if location_id > 1000000000000: # it is a citadel
            location_type = 'citadel'
            op = self.app.op['get_universe_structures_structure_id'](
                structure_id=location_id
            )
        else: # it is a station
            location_type = 'station'
            op = self.app.op['get_universe_stations_station_id'](
                station_id=location_id
            )
        location = self.esi.request(op,raise_on_error=True)
        details = {
            location_id: location_id,
            location_type: location_type,
            system_id: location.data['system_id'],
            name: location.data.name
        }
        return details

    def personal_contracts(self):
        raise NotImplementedError
