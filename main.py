# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

# This code is not the best as i honestly dont care much about it its made to work well and i do not need it to be good code overall as i dont update this often
# Only the paid version will get updates often this is a side thing nothing crazy
# Remember this is literary the only up to date FREE tool out on github all the other ones are old or skids from 2023
# If you wana get more features with the cost of flgging ur stuff do but you will make ur tokens flagged

from src import *
from src.utils.rpc import DiscordRPC
from src.utils.console import Console
from src.utils.files import files; files.check()
from src.utils.config import get
from src.utils.logging import Logger
from src.utils.discord import discord
from src.funcs import *
console = Console('Main')

discord.sleep(0.5)
console.cls()
console.title('G4Raid - g4tools.cc - discord.gg/spamming - Made by r3ci')
console.printbanner()

if get.debug.enabled():
    Logger.info('Debug mode enabled', 'Config')
while True:
    DiscordRPC().update()
    console.title('G4Raid-lite - g4tools.cc - discord.gg/spamming - Made by r3ci')
    console.cls()
    console.printbanner()
    console.printbar(len(files.gettokens()), 0)
    console.printmenu()
    Logger.info(f'G4Raid-lite made by r3ci <3')

    choice = console.input('Option', str)

    options = {
        'su': suppliers().menu,
        'sc': lambda: Logger.paidonly(),
        '1': lambda: Logger.paidonly(),
        '2': leaver().menu,
        '3': serverchecker().menu,
        '4': channelchecker().menu,
        '5': lambda: Logger.info('Will unpatch this soon', 'Menu'),
        '6': channelspammer().menu,
        '7': lambda: Logger.paidonly(),
        '8': lambda: Logger.paidonly(),
        '9': lambda: Logger.paidonly(),
        '10': lambda: Logger.paidonly(),
        '11': checker().menu,
        '12': biochanger().menu,
        '13': lambda: Logger.paidonly(),
        '14': lambda: Logger.paidonly(),
        '15': displaynamechanger().menu,
        '16': nicknamechanger().menu,
        '17': lambda: Logger.paidonly(),
        '18': lambda: Logger.paidonly(),
        '19': lambda: Logger.info('Not implemented yet', 'Menu'),
        '20': verifybypasses().menu,
    }

    choice = (str(int(choice)) if choice.startswith('0') and len(choice) == 2 else choice).lower()
    
    if choice in options:
        try:
            options[choice]()
            
        except Exception as e:
            Logger.error(f'Failed to run {str(choice)} » {str(e)}')
    else:
        Logger.error(f'Invalid option » {str(choice)}')

    Logger.info('Finished running option', 'Main')
    input('')