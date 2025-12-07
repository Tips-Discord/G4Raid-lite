import sys, os
if os.name == 'nt':
    os.system('cls')
    os.system('title G4Raid-lite - launching...')
else:
    os.system('clear')
    sys.stdout.write(f"]2;G4Raid-lite - launching...")

import base64
import concurrent.futures
import copy
import json
import random
import re
import shutil
import socket
import string
import sys
import threading as threadinglib
import time
import traceback
import uuid
import webbrowser
from collections import defaultdict, namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from datetime import datetime as dt
from typing import Callable, Dict, List, Union, Any
from urllib.parse import quote, urlparse

import curl_cffi as curlcffi_
import pyperclip
import requests
import tkinter as tk
import urllib3
import websocket
from curl_cffi import exceptions as cfex
from curl_cffi import requests as curlcffi
from pypresence import Presence
from requests.cookies import RequestsCookieJar
from tkinter import Frame, Tk, filedialog, messagebox, ttk
from tkinter.filedialog import askdirectory, askopenfilename

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

class co:
    main = rgb(80, 5, 255)
    red = rgb(255, 69, 0)
    darkred = rgb(87, 2, 2)
    green = rgb(12, 250, 0)
    blue = rgb(30, 144, 255)
    yellow = rgb(255, 215, 0)
    orange = rgb(255, 140, 0)
    deeporange = rgb(201, 105, 6)
    pink = rgb(255, 105, 180)
    cyan = rgb(0, 255, 255)
    magenta = rgb(255, 0, 255)
    lime = rgb(12, 250, 0)
    indigo = rgb(138, 43, 226)
    grey = rgb(169, 169, 169)
    black = rgb(69, 69, 69)
    white = rgb(255, 255, 255)

    infolog = pink
    success = lime
    error = red
    locked = darkred
    debug = grey
    warning = yellow
    ratelimit = orange
    cloudflare = deeporange
    solver = indigo
    captcha = cyan
    
    reset = '\033[0m'

from src.utils.errorhandler import errorhandler
sys.excepthook = errorhandler

from src.utils.files import files
files.check()
