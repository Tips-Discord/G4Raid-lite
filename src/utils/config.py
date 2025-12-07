from src import *

class TomlParser:
    @staticmethod
    def parse(content: str) -> dict:
        if not content or not content.strip():
            return {}

        data = {}
        current_section = None
        
        lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

        for line in lines:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue

            if line.startswith('[') and line.endswith(']'):
                raw_section = line[1:-1].strip()
                current_section = raw_section 
                if current_section not in data:
                    data[current_section] = {}
                continue

            if '=' in line and current_section is not None:
                parts = line.split('=', 1)
                key = parts[0].strip()
                value_part = parts[1].strip()

                if not re.match(r'^[a-zA-Z0-9_\-\s]+$', key):
                    continue

                value = TomlParser._extract_value_before_comment(value_part)
                parsed_value = TomlParser._parse_value(value)
                data[current_section][key] = parsed_value

        return data

    @staticmethod
    def _extract_value_before_comment(text: str) -> str:
        if not text: 
            return ""
        
        in_quote = False
        quote_char = None
        
        for i, char in enumerate(text):
            if char in ['"', "'"]:
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    if i > 0 and text[i-1] == '\\':
                        pass
                    else:
                        in_quote = False
                        quote_char = None
            
            if char == '#' and not in_quote:
                return text[:i].strip()
        
        return text.strip()

    @staticmethod
    def _parse_value(value: str):
        lower = value.lower()
        if lower in ('true', 'yes', 'on', '1'): return True
        if lower in ('false', 'no', 'off', '0'): return False

        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')

        try:
            if '.' in value or 'e' in lower:
                return float(value)
            return int(value, 0)
        except ValueError:
            pass

        return value

class ConfigManager:
    def __init__(self):
        self.filename = 'config.toml'
        self.defaults = {
            'rpc [TURNING OFF ANVAIBLE IN PAID ONLY]': {
                'enabled': (True, 'Make RPC visible'),
                'showdata': (True, 'Shows how many tokens and proxies you have loaded')
            },
            'proxies [ANVAIBLE IN PAID ONLY]': {
                'enabled': (False, 'Enable proxy support')
            },
            'tokenonlining [ANVAIBLE IN PAID ONLY]': {
                'enabled': (True, 'Onlines tokens on startup. DISABLING MAY LEAD TO CAPTCHAS'),
                'delay': (0.1, 'Delay between onlines. INCREASE FOR BAD INTERNET'),
                'status': ('random', 'Status: online, dnd, idle, invisible, random')
            },
            'solver [ANVAIBLE IN PAID ONLY]': {
                'README': ('For solvers to work you need GOOD PROXIES', 'readme'),
                'enabled': (False, 'Enable solver'),
                'apikey': ('your-api-key-here', 'Your solver api key'),
                'service': ('your-solver-service', 'Your solver service'),
            },
            'debug': {
                'enabled': (False, 'Enable debug mode'),
                'pause': (False, 'Pause execution for debugging')
            }
        }
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.data = TomlParser.parse(content)
                self.validate()
            except Exception:
                self.data = {}
                self.validate()
        else:
            self.validate()

    def validate(self):
        dirty = False
        
        for section, keys in self.defaults.items():
            if section not in self.data:
                self.data[section] = {}
                dirty = True
            
            for key, (def_val, _) in keys.items():
                if key not in self.data[section]:
                    self.data[section][key] = def_val
                    dirty = True
                else:
                    current = self.data[section][key]
                    casted = self._cast(current, def_val)
                    if current != casted:
                        self.data[section][key] = casted
                        dirty = True

        if dirty:
            self.save()

    def get(self, section_keyword: str, key: str, fallback=None):
        real_section = None
        for s in self.data.keys():
            if s.startswith(section_keyword):
                real_section = s
                break
        
        if not real_section:
            return fallback

        return self.data.get(real_section, {}).get(key, fallback)

    def set(self, section_keyword: str, key: str, value):
        real_section = None
        for s in self.data.keys():
            if s.startswith(section_keyword):
                real_section = s
                break
        
        if not real_section:
            for s in self.defaults.keys():
                if s.startswith(section_keyword):
                    real_section = s
                    break
            if not real_section: return False

        if real_section not in self.data:
            self.data[real_section] = {}

        self.data[real_section][key] = value
        self.save()
        return True

    def save(self):
        temp_file = self.filename + '.tmp'
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                for section, keys in self.defaults.items():
                    f.write(f'[{section}]\n')
                    for key, (def_val, comment) in keys.items():
                        val = self.data.get(section, {}).get(key, def_val)
                        
                        if isinstance(val, bool):
                            fmt_val = str(val).lower()
                        elif isinstance(val, (int, float)):
                            fmt_val = str(val)
                        else:
                            clean_str = str(val).replace('\\', '\\\\').replace('"', '\\"')
                            fmt_val = f'"{clean_str}"'
                        
                        f.write(f'{key} = {fmt_val} # {comment}\n')
                    f.write('\n') 
            
            if os.path.exists(self.filename):
                os.remove(self.filename)
            os.rename(temp_file, self.filename)
            return True
        except Exception:
            return False

    def _cast(self, value, default):
        try:
            target_type = type(default)
            if target_type == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            if target_type == int:
                return int(float(value))
            if target_type == float:
                return float(value)
            return str(value)
        except:
            return default

_cfg = ConfigManager()

class switch:
    class rpc:
        class enabled:
            @staticmethod
            def true(): _cfg.set('rpc', 'enabled', True)
            @staticmethod
            def false(): _cfg.set('rpc', 'enabled', False)
        
        class showdata:
            @staticmethod
            def true(): _cfg.set('rpc', 'showdata', True)
            @staticmethod
            def false(): _cfg.set('rpc', 'showdata', False)

    class proxies:
        class enabled:
            @staticmethod
            def true(): _cfg.set('proxies', 'enabled', True)
            @staticmethod
            def false(): _cfg.set('proxies', 'enabled', False)

    class tokenonlining:
        class enabled:
            @staticmethod
            def true(): _cfg.set('tokenonlining', 'enabled', True)
            @staticmethod
            def false(): _cfg.set('tokenonlining', 'enabled', False)
        
        class delay:
            @staticmethod
            def set(value): _cfg.set('tokenonlining', 'delay', float(value))

    class solver:
        class enabled:
            @staticmethod
            def true(): _cfg.set('solver', 'enabled', True)
            @staticmethod
            def false(): _cfg.set('solver', 'enabled', False)
        
        class apikey:
            @staticmethod
            def set(value): _cfg.set('solver', 'apikey', str(value))
            
        class service:
            @staticmethod
            def set(value): _cfg.set('solver', 'service', str(value))

    class debug:
        class enabled:
            @staticmethod
            def true(): _cfg.set('debug', 'enabled', True)
            @staticmethod
            def false(): _cfg.set('debug', 'enabled', False)
        
        class pause:
            @staticmethod
            def true(): _cfg.set('debug', 'pause', True)
            @staticmethod
            def false(): _cfg.set('debug', 'pause', False)

class get:
    class rpc:
        @staticmethod
        def enabled() -> bool: return _cfg.get('rpc', 'enabled', True)
        @staticmethod
        def showdata() -> bool: return _cfg.get('rpc', 'showdata', True)

    class proxies:
        @staticmethod
        def enabled() -> bool: return _cfg.get('proxies', 'enabled', False)

    class tokenonlining:
        @staticmethod
        def enabled() -> bool: return _cfg.get('tokenonlining', 'enabled', True)
        @staticmethod
        def delay() -> float: return _cfg.get('tokenonlining', 'delay', 0.1)
        @staticmethod
        def status() -> str: return _cfg.get('tokenonlining', 'status', 'random')

    class solver:
        @staticmethod
        def enabled() -> bool: return _cfg.get('solver', 'enabled', False)
        @staticmethod
        def apikey() -> str: return _cfg.get('solver', 'apikey', '')
        @staticmethod
        def service() -> str: return _cfg.get('solver', 'service', 'teamai')

    class debug:
        @staticmethod
        def enabled() -> bool: return _cfg.get('debug', 'enabled', False)
        @staticmethod
        def pause() -> bool: return _cfg.get('debug', 'pause', False)