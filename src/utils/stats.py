from src import *
from src.utils.logging import logger

class StatsManager:
    SUCCEEDED = 'succeeded'
    CAPTCHA = 'captcha'
    FAILED = 'failed'
    REASONS = 'reasons'

    def __init__(self, session_name: str):
        self.session_name = session_name
        self.path = os.path.join('data', 'stats', session_name)
        
        self.data = {
            self.SUCCEEDED: [],
            self.CAPTCHA: [],
            self.FAILED: [],
            self.REASONS: []
        }
        
        self._lock = threadinglib.Lock()
        self._initialize_storage()

    def _initialize_storage(self):
        try:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
            os.makedirs(self.path, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to initialize stats folder: {e}")

    def get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_count(self, category: str) -> int:
        with self._lock:
            return len(self.data.get(category, []))

    def append(self, category: str, token: str, error: str = None):
        with self._lock:
            if category not in self.data:
                self.data[category] = []

            self.data[category].append(token)

            self._write_to_file(category, token)

            if error:
                reason_entry = f'{token} » {error}'
                
                if self.REASONS not in self.data:
                    self.data[self.REASONS] = []
                self.data[self.REASONS].append(reason_entry)
                
                self._write_to_file(self.REASONS, reason_entry)

    def _write_to_file(self, category: str, content: str):
        filepath = os.path.join(self.path, f'{category}.txt')
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content + '\n')
        except Exception as e:
            print(f"[Stats Error] Could not write to {category}: {e}")

stats = StatsManager
