from src import *
from src.utils.logging import logger

class console:
    def __init__(self, module='Console'):
        self.module = module

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def title(self, title):
        if os.name == 'nt':
            os.system(f'title {title}')
        else:
            sys.stdout.write(f"]2;{title}")

    def center(self, text, size):
        text = str(text)
        lines = text.split('\n')
        centeredlines = []
        for line in lines:
            visibleline = re.sub(r'\033\[[0-9;]*m', '', line)
            visiblelength = len(visibleline)
            
            if visiblelength >= size:
                centeredlines.append(line)
            else:
                padding = (size - visiblelength) // 2
                centeredlines.append(' ' * padding + line)
        
        return '\n'.join(centeredlines)
    
    def gradient(self, text, color1, color2):
        if not text:
            return ''
        
        result = ''
        text_length = len(text)
        
        for i, char in enumerate(text):
            factor = (i / text_length) ** 0.7 if text_length > 1 else 0
            r = int(color1[0] + (color2[0] - color1[0]) * factor)
            g = int(color1[1] + (color2[1] - color1[1]) * factor)
            b = int(color1[2] + (color2[2] - color1[2]) * factor)
            result += f'\033[38;2;{r};{g};{b}m{char}'
        
        result += '\033[0m'
        return result

    def printbar(self, tokens, proxies):
        bar = fr'{co.main}«{tokens}» Tokens                   «{proxies}» Proxies'

        bar = self.center(text=bar, size=os.get_terminal_size().columns)
        bar = str(bar)

        for char in ['»', '«']:
            bar = bar.replace(char, f'{co.main}{char}{co.reset}')

        print(bar)

    def printbanner(self):
        banner = fr'''{co.main}
   ________ __  ____        _     __      ___ __     
  / ____/ // / / __ \____ _(_)___/ /     / (_) /____ 
 / / __/ // /_/ /_/ / __ `/ / __  /_____/ / / __/ _ \
/ /_/ /__  __/ _, _/ /_/ / / /_/ /_____/ / / /_/  __/
\____/  /_/ /_/ |_|\__,_/_/\__,_/     /_/_/\__/\___/ ''' 
        banner = self.center(banner, os.get_terminal_size().columns)

        print(banner)

    def printmenu(self):
        page1 = fr'''{co.reset}
«Using the lite version, buy paid to get all features (all payments supported & 15usd lifetime)»
«https://g4tools.cc»

«SU» Token/Proxy Suppliers                                                  «SC» Scraping/Dumping
«01» Server Joiner $     «06» Channel Spammer      «11» Checker             «16» NickName Changer
«02» Server Leaver       «07» MultChanel Spammer $ «12» Bio Changer         «17» Profile Reporter $
«03» Server Checker      «08» Reply spammer $      «13» Avatar Changer $    «18» Message Reporter $
«04» Channel Checker     «09» Chat Crasher $       «14» ClanTag Changer $   «19» Tutorials       
«05» AuditLog Fucker  $  «10» Reaction Speller $   «15» Displayname Changer «20» Verify Bypasses 
'''     
        page1: str = self.center(text=page1, size=os.get_terminal_size().columns)
        
        for char in ['»', '«']:
            page1 = page1.replace(char, f'{co.main}{char}{co.reset}')

        print(page1)

    def input(self, text, expected=str):
        module = f'{co.main}[{co.reset}{self.module}{co.main}] ' if self.module else ''
        
        promptparts = [f'{co.main}[{co.reset}{text}{co.main}]']
        
        if expected == bool:
            promptparts.append(f'{co.main}({co.reset}{co.lime}y{co.reset}/{co.red}n{co.reset}{co.main})')
        
        prompt = ' '.join(promptparts) + f' {co.reset}» {co.reset}'
        
        while True:
            result = input(prompt).strip()
        
            if not result:
                if expected == str:
                    return result
                else:
                    logger.info('Input required please enter a value')
                    continue

            if expected == bool:
                if result.lower() in ['y', 'yes', 'true', '1']:
                    return True
                
                elif result.lower() in ['n', 'no', 'false', '0']:
                    return False
                
                else:
                    logger.info('Invalid input please enter y/yes/true or n/no/false')
                    continue
            
            if expected == str:
                return result
            
            try:
                converted = expected(result)
                return converted
                
            except ValueError:
                if expected == int:
                    logger.info('Please enter a whole number (eg 1 42 100)')

                elif expected == float:
                    logger.info('Please enter a decimal number (eg 1.5 3.14 10.0)')

                else:
                    logger.info(f'Invalid format expected {expected.__name__}')
                continue

    def prep(self):
        self.cls()
        self.printbanner()
        if self.module != None:
            self.title(f'G4Raid-lite - {self.module} - g4tools.cc - discord.gg/spamming - Made by r3ci')

    def createmenu(self, options):
        toprint = []
        for i, option in enumerate(options, 1):
            number = str(i).zfill(2)
            toprint.append(f'{co.main}[{co.reset}{number}{co.main}] » {co.main}[{co.reset}{option}{co.main}]')
        
        print('\n'.join(toprint))

    def printcustommenu(self, options):
        options = dict(options)
        self.prep()
        self.createmenu(list(options.keys()) + ['Back'])
