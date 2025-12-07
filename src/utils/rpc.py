from src import *
from src.utils.config import get
from src.utils.files import files

class DiscordRPC:
    def __init__(self):
        self.client_id = '1430609793436876820'
        self.rpc = None
        self.connected = False
        self.start_time = int(time.time())

        if not get.rpc.enabled():
            return

        self._connect()

    def _connect(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True

            self.update(state="Idling...")
        except Exception:
            self.connected = False

    def _get_data_string(self):
        if get.rpc.showdata():
            token_count = len(files.gettokens())
            proxy_count = 0 
            return f'Tokens » {token_count} | Proxies » {proxy_count}'
        else:
            return 'Tokens » Private | Proxies » Private'

    def update(self, state="Idling..."):
        if not self.connected or not self.rpc:
            return

        try:
            self.rpc.update(
                state=state,
                details='Using G4Raid-lite',
                start=self.start_time,
                large_image='smalllogorounded',
                large_text='discord.gg/spamming',
                small_image='folder',
                small_text=self._get_data_string(),
                buttons=[
                    {'label': 'Join Discord', 'url': 'https://discord.gg/spamming'},
                    {'label': 'Get G4Raid for FREE', 'url': 'https://github.com/r3ci/G4Raid'}
                ]
            )
        except Exception:
            self.connected = False