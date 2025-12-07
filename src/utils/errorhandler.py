from src import *
from src.utils.logging import Logger

def errorhandler(exc_type, exc_value, exc_traceback):
    tracebk = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    Logger.error(f'Error » {tracebk}')
    Logger.error('If this keeps happening join the discord and report the error')
    input('')
    sys.exit()