from src import *
from src.utils.console import Console
from src.utils.logging import Logger

class suppliers:
    def __init__(self):
        self.console = Console('Suppliers')

    def tokens(self):
        supp = requests.get('https://g4tools.cc/api/tokensupplier').text
        Logger.info('IMPORTANT > AFTER BUYING THEM WAIT 1-2 DAYS BEFORE USE YES EVEN WITH AGED ONES', 'Suppliers')
        Logger.info(f'Tokens are available at {supp}', 'Suppliers')
        webbrowser.open(supp)

    def proxies(self):
        supp = requests.get('https://g4tools.cc/api/proxysupplier').text
        Logger.info(f'Proxies are available at {supp}', 'Suppliers')
        webbrowser.open(supp)
    
    def menu(self):
        menu = {
            'Tokens': self.tokens,
            'Proxies (BUY RESIDENTIAL ONLY)': self.proxies
        }

        self.console.createmenu(menu)
        choice = self.console.input('Choice', int)

        if choice == 1:
            self.tokens()

        elif choice == 2:
            self.proxies()