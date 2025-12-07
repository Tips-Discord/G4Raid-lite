from src import *
from src.utils.files import files
from src.utils.console import Console
from src.utils.threading import threading
from src.utils.discord import discord
from src.utils.stats import StatsManager
from src.utils.config import get
from src.utils.logging import Logger
from src.utils.sessionmanager import client as Client

class nicknamechanger:
    def __init__(self):
        self.console = Console('Nickname Changer')
        self.stats = StatsManager('Nickname_Changer', [StatsManager.SUCCEEDED, StatsManager.CAPTCHA, StatsManager.FAILED])
        self.nickname = None
        self.serverid = None
    
    def change(self, client: Client):
        try:
            client.cleanxcontent()
            if not client.cookiejar:
                Logger.infolog(f'{client.maskedtoken} » Getting cookies')
                client.refreshcookies()
                client.updatecookies(client.cookiejar, client.cookiestr)

            while True:
                r = client.sess.patch(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/members/@me',
                    headers=client.headers,
                    json={
                        'nick': f'g4tools.cc | {self.nickname}'
                    }

                )

                if r.status_code == 200:
                    Logger.success(f'{client.maskedtoken} » Changed')
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

                elif 'captcha_key' in r.text:
                    Logger.captcha(f'{client.maskedtoken} » Human verification (could have been avoided with paid version)')
                    self.stats.append(StatsManager.CAPTCHA, client.token)
                    break

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
        self.change(client)

    def menu(self):
        self.console.prep()
        self.nickname = self.console.input('Nickname', str)
        self.serverid = self.console.input('Server ID', str)
        self.delay = self.console.input('Delay', float)
        Logger.info(f'Stats will be saved to {self.stats.path}')
        Logger.info('Nickname with no watermark is anvaible in the paid version only')
        Logger.info('Nickname with no watermark is anvaible in the paid version only')
        Logger.info('Nickname with no watermark is anvaible in the paid version only')

        threading(
            func=self.run,
            tokens=[token.token for token in files.gettokens()],
            delay=self.delay
        )