from src import *
from src.utils.logging import logger
from src.utils.errorhandler import errorhandler

class SafeThread(threadinglib.Thread):
    def run(self):
        try:
            if self._target:
                super().run()
        except Exception:
            errorhandler(*sys.exc_info())

class threading:
    def __init__(self, func: Callable, tokens: List[str], args: list = None, delay: float = 0):
        self.func = func
        self.tokens = tokens
        self.args = args if args is not None else []
        self.delay = delay
        self.threads: List[SafeThread] = []

    def start(self):
        if not self.tokens:
            logger.warning("No tokens have been passed.")
            return

        try:
            for token in self.tokens:
                t = SafeThread(
                    target=self.func, 
                    args=(token, *self.args)
                )
                self.threads.append(t)
                t.start()

                if self.delay > 0:
                    time.sleep(self.delay)

            for thread in self.threads:
                thread.join()

        except KeyboardInterrupt:
            logger.info("Interrupted. Waiting for pending threads...")
