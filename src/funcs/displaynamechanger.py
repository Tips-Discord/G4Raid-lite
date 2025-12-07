from src import *
from src.utils.files import files
from src.utils.console import Console
from src.utils.threading import threading
from src.utils.discord import discord
from src.utils.config import get
from src.utils.stats import StatsManager
from src.utils.logging import Logger
from src.utils.sessionmanager import client as Client

class displaynamechanger:
    def __init__(self):
        self.console = Console('Display Name Changer')
        self.stats = StatsManager('Disply_Name_Changer', [StatsManager.SUCCEEDED, StatsManager.CAPTCHA, StatsManager.FAILED])
        self.name = None
    
    def change(self, client: Client):
        try:
            client.cleanxcontent()
            if not client.cookiejar:
                Logger.infolog(f'{client.maskedtoken} » Getting cookies')
                client.refreshcookies()
                client.updatecookies(client.cookiejar, client.cookiestr)

            while True:
                r = client.sess.patch(
                    f'https://discord.com/api/v9/users/@me',
                    headers=client.headers,
                    json={
                        'global_name': f'g4tools.cc | {self.name}'
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
                    ratelimit = r.json().get('retry_after', 1.5)
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
        self.name = self.console.input('Name', str)
        self.delay = self.console.input('Delay', float)
        Logger.info(f'Stats will be saved to {self.stats.path}')
        Logger.info('Displayname with no watermark is anvaible in the paid version only')
        Logger.info('Displayname with no watermark is anvaible in the paid version only')
        Logger.info('Displayname with no watermark is anvaible in the paid version only')

        threading(
            func=self.run,
            tokens=[token.token for token in files.gettokens()],
            delay=self.delay
        )