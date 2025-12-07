from src import *
from src.utils.files import files
from src.utils.console import Console
from src.utils.threading import threading
from src.utils.discord import discord
from src.utils.stats import StatsManager
from src.utils.logging import Logger
from src.utils.sessionmanager import client as Client

class leaver:
    def __init__(self):
        self.console = Console('Leaver')
        self.stats = StatsManager('Leaver', [StatsManager.SUCCEEDED, StatsManager.FAILED])
        self.serverid = None
    
    def leave(self, client: Client):
        try:
            client.cleanxcontent()
            if not client.cookiejar:
                Logger.infolog(f'{client.maskedtoken} » Getting cookies')
                client.refreshcookies()
                client.updatecookies(client.cookiejar, client.cookiestr)

            while True:
                r = client.sess.delete(
                    f'https://discord.com/api/v9/users/@me/guilds/{self.serverid}',
                    headers=client.headers,
                    json={
                        'lurking': False
                    }
                )

                if r.status_code == 204:
                    Logger.success(f'{client.maskedtoken} » Left')
                    self.stats.append(StatsManager.SUCCEEDED, client.token)
                    break

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    Logger.ratelimit(f'{client.maskedtoken} » {ratelimit}s')
                    discord.sleep(ratelimit)

                elif 'Try again later' in r.text:
                    Logger.ratelimit(f'{client.maskedtoken} » 5s')
                    discord.sleep(5)

                elif 'Cloudflare' in r.text:
                    Logger.cloudflare(f'{client.maskedtoken} » 10s')
                    discord.sleep(10)

                elif 'You need to verify' in r.text:
                    Logger.locked(f'{client.maskedtoken} Locked/Flagged')
                    self.stats.append(StatsManager.FAILED, client.token, 'Locked/Flagged')
                    break

                else:
                    e, etype = discord.errordatabase(r.text) 
                    Logger.error(f'{client.maskedtoken} » {e}')
                    self.stats.append(StatsManager.FAILED, client.token, e)
                    break
                
        except Exception as e:
            Logger.error(f'{client.maskedtoken} » {e}')
            self.stats.append(StatsManager.FAILED, client.token, e)

    def run(self, token):
        client = Client(token)
        self.leave(client)

    def menu(self):
        self.console.prep()
        self.serverid = self.console.input('Server ID', str)
        self.delay = self.console.input('Delay', float)
        Logger.info(f'Stats will be saved to {self.stats.path}')

        threading(
            func=self.run,
            tokens=[token.token for token in files.gettokens()],
            delay=self.delay
        )