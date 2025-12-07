from src import *
from src.utils.logging import Logger

class Console:
    def __init__(self, module: str = 'Console'):
        self.module = module
        self._ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def title(self, title: str):
        if os.name == 'nt':
            os.system(f'title {title}')
        else:
            sys.stdout.write(f"\033]0;{title}\007")
            sys.stdout.flush()

    def _get_width() -> int:
        return shutil.get_terminal_size(fallback=(120, 30)).columns

    def center(self, text: str) -> str:
        text = str(text)
        lines = text.split('\n')
        centered_lines = []
        width = Console._get_width()

        for line in lines:
            visible_line = self._ansi_escape.sub('', line)
            visible_length = len(visible_line)
            
            if visible_length >= width:
                centered_lines.append(line)
            else:
                padding = (width - visible_length) // 2
                centered_lines.append(' ' * padding + line)
        
        return '\n'.join(centered_lines)

    def center_block(self, text: str) -> str:
        text = str(text)
        lines = text.split('\n')
        
        max_content_width = 0
        for line in lines:
            visible_line = self._ansi_escape.sub('', line)
            max_content_width = max(max_content_width, len(visible_line))
            
        term_width = Console._get_width()
        padding = (term_width - max_content_width) // 2
        padding = max(0, padding)
        
        centered_lines = []
        for line in lines:
            centered_lines.append((' ' * padding) + line)
        
        return '\n'.join(centered_lines)
    
    def gradient(self, text: str, color1: list, color2: list) -> str:
        if not text:
            return ''
        
        result = []
        length = len(text)
        
        div = length - 1 if length > 1 else 1

        for i, char in enumerate(text):
            factor = (i / div) ** 0.7
            r = int(color1[0] + (color2[0] - color1[0]) * factor)
            g = int(color1[1] + (color2[1] - color1[1]) * factor)
            b = int(color1[2] + (color2[2] - color1[2]) * factor)
            result.append(f'\033[38;2;{r};{g};{b}m{char}')
        
        result.append('\033[0m')
        return ''.join(result)

    def printbar(self, tokens: int, proxies: Union[int, str]):
        bar_text = f'{co.main}«{tokens}» Tokens                   «{proxies}» Proxies'
        
        centered_bar = self.center(bar_text)
        
        formatted_bar = centered_bar.replace('»', f'{co.main}»{co.reset}') \
                                    .replace('«', f'{co.main}«{co.reset}')

        print(formatted_bar)

    def printbanner(self):
        raw_banner = fr'''{co.main}
   ________ __  ____        _     __      ___ __     
  / ____/ // / / __ \____ _(_)___/ /     / (_) /____ 
 / / __/ // /_/ /_/ / __ `/ / __  /_____/ / / __/ _ \
/ /_/ /__  __/ _, _/ /_/ / / /_/ /_____/ / / /_/  __/
\____/  /_/ /_/ |_|\__,_/_/\__,_/     /_/_/\__/\___/ '''.strip('\n')
        print(self.center_block(raw_banner))

    def printmenu(self):
        header_text = fr'''{co.reset}
«Using the lite version, buy paid to get all features (all payments supported & 15usd lifetime)»
«https://g4tools.cc»'''.strip()

        options_text = fr'''{co.reset}
«SU» Token/Proxy Suppliers                                                  «SC» Scraping/Dumping
«01» Server Joiner $     «06» Channel Spammer      «11» Checker             «16» NickName Changer
«02» Server Leaver       «07» MultChanel Spammer $ «12» Bio Changer         «17» Profile Reporter $
«03» Server Checker      «08» Reply spammer $      «13» Avatar Changer $    «18» Message Reporter $
«04» Channel Checker     «09» Chat Crasher $       «14» ClanTag Changer $   «19» Tutorials       
«05» AuditLog Fucker  $  «10» Reaction Speller $   «15» Displayname Changer «20» Verify Bypasses'''.strip()

        c_header = self.center(header_text)
        c_options = self.center_block(options_text)
        
        full_menu = f"{c_header}\n{c_options}"

        final_output = full_menu.replace('»', f'{co.main}»{co.reset}') \
                                .replace('«', f'{co.main}«{co.reset}')

        print(final_output + '\n')

    def input(self, text: str, expected: type = str) -> Any:
        module_tag = f'{co.main}[{co.reset}{self.module}{co.main}] ' if self.module else ''
        text_tag = f'{co.main}[{co.reset}{text}{co.main}]'
        
        bool_hint = f'{co.main}({co.reset}{co.lime}y{co.reset}/{co.red}n{co.reset}{co.main})' if expected == bool else ''
        
        prompt = f'{module_tag}{text_tag} {bool_hint} {co.reset}» {co.reset}'
        
        while True:
            try:
                result = input(prompt).strip()
            except KeyboardInterrupt:
                print()
                sys.exit(0)

            if not result:
                if expected == str:
                    return result
                Logger.info('Input required, please enter a value')
                continue

            if expected == bool:
                lower_res = result.lower()
                if lower_res in ('y', 'yes', 'true', '1'):
                    return True
                elif lower_res in ('n', 'no', 'false', '0'):
                    return False
                else:
                    Logger.info('Invalid input. Use y/yes or n/no')
                    continue
            
            if expected == str:
                return result
            
            try:
                return expected(result)
            except ValueError:
                if expected == int:
                    Logger.info('Please enter a whole number (e.g. 1, 42)')
                elif expected == float:
                    Logger.info('Please enter a decimal number (e.g. 1.5, 3.14)')
                else:
                    Logger.info(f'Invalid format expected {expected.__name__}')

    def prep(self):
        self.cls()
        self.printbanner()
        if self.module:
            self.title(f'G4Raid-lite - {self.module} - g4tools.cc - discord.gg/spamming - Made by r3ci')

    def createmenu(self, options: list):
        lines = []
        for i, option in enumerate(options, 1):
            num = str(i).zfill(2)
            lines.append(f'{co.main}[{co.reset}{num}{co.main}] » {co.main}[{co.reset}{option}{co.main}]')
        
        print('\n'.join(lines))

    def printcustommenu(self, options: dict):
        self.prep()
        menu_items = list(options.keys()) + ['Back']
        self.createmenu(menu_items)