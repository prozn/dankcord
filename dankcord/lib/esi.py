from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.cache import FileCache

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
            client_id=self.client_id,
            secret_key=self.secret_key,
        )
        self.esi = EsiClient(
            retry_requests=True,  # set to retry on http 5xx error (default False)
            headers={'User-Agent': 'Discord bot by Prozn: https://github.com/prozn/dankcord'},
            security=self.security
        )
        security.update_token({
            'access_token': '',  # leave this empty
            'expires_in': -1,  # seconds until expiry, so we force refresh anyway
            'refresh_token': self.refresh_token
        })
        security.refresh()

    def character_info(self, character_id):
        op = self.app.op['get_characters_character_id'](
            character_id=character_id
        )
        character = self.esi.request(op,raise_on_error=True)
        return character

    def character_name(self, character_id):
        character = self.character_info(character_id)
        return character.name

    def corp_contracts(self, corporation_id):
        op = self.app.op['get_corporations_corporation_id_contracts'](
            corporation_id=corporation_id
        )
        contracts = esi.request(op,raise_on_error=True)
        return contracts

    def personal_contracts(self):
        raise NotImplementedError
