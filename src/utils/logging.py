from src import *
from src.utils.config import get

class Logger:
    @staticmethod
    def _timestamp():
        return datetime.now().strftime('%H:%M:%S ')

    @staticmethod
    def _format_arrow(text, color_code):
        return text.replace('»', f'{co.reset}»{color_code}') \
                   .replace('«', f'{co.reset}«{color_code}')

    @staticmethod
    def _log(label, color_code, text):
        ts = Logger._timestamp()
        
        # Base format
        # [TIMESTAMP] [LABEL] » [TEXT]
        log_msg = (
            f"{co.black}{ts}"
            f"{color_code}{label} {co.reset}»{co.reset} "
            f"{color_code}[{text}]{co.reset}"
        )

        log_msg = Logger._format_arrow(log_msg, color_code)
        
        print(log_msg)


    @staticmethod
    def info(text, subtext=None):
        prefix = ''
        if subtext:
            prefix = f'{co.main}[{co.reset}{subtext}{co.main}] {co.reset}»{co.reset} '
        
        log_msg = f'{prefix}{co.main}[{co.reset}{text}{co.main}]{co.reset}'
        log_msg = log_msg.replace('»', f'{co.main}»{co.reset}')
        log_msg = log_msg.replace('«', f'{co.main}«{co.reset}')
        
        print(log_msg)

    @staticmethod
    def infolog(text):
        Logger._log("INFO", co.infolog, text)

    @staticmethod
    def success(text):
        Logger._log("SUCCESS", co.success, text)

    @staticmethod
    def error(text):
        Logger._log("ERROR", co.error, text)

    @staticmethod
    def warning(text):
        Logger._log("WARNING", co.warning, text)

    @staticmethod
    def locked(text):
        Logger._log("LOCKED", co.locked, text)

    @staticmethod
    def ratelimit(text):
        Logger._log("RATELIMIT", co.ratelimit, text)

    @staticmethod
    def cloudflare(text):
        Logger._log("CLOUDFLARE", co.cloudflare, text)

    @staticmethod
    def solver(text):
        Logger._log("SOLVER", co.solver, text)

    @staticmethod
    def captcha(text):
        Logger._log("CAPTCHA", co.captcha, text)

    @staticmethod
    def debug(text):
        if get.debug.enabled():
            Logger._log("DEBUG", co.debug, text)


class InterfaceUtils:
    @staticmethod
    def show_paid_only_popup():
        def fade_in(window, alpha=0):
            alpha = min(alpha + 0.05, 1.0)
            window.attributes('-alpha', alpha)
            if alpha < 1:
                window.after(10, fade_in, window, alpha)

        def fade_out(window, alpha=1):
            alpha = max(alpha - 0.05, 0)
            window.attributes('-alpha', alpha)
            if alpha > 0:
                window.after(10, fade_out, window, alpha)
            else:
                window.destroy()

        def open_shop():
            webbrowser.open('https://g4tools.cc')
            fade_out(root)

        # UI Setup
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True, '-alpha', 0)
        root.configure(bg='#000000')

        # Calculate Center Position
        root.update_idletasks()
        width, height = 300, 150 #
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'+{x}+{y}')

        # Styling
        outer = tk.Frame(root, bg='#000000')
        outer.pack(padx=2, pady=2, fill='both', expand=True)
        
        inner = tk.Frame(outer, bg='#1e1e1e')
        inner.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 10), foreground='#ffffff', background='#2d2d30', borderwidth=0)
        style.map('TButton', background=[('active', '#3e3e42')])

        # Content
        ttk.Label(inner, text='This is a paid only feature', justify='center').pack(pady=(25, 15))

        btn_frame = tk.Frame(inner, bg='#1e1e1e')
        btn_frame.pack(pady=(0, 20))

        ttk.Button(btn_frame, text='OK', command=lambda: fade_out(root)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Get Paid Now', command=open_shop).pack(side='left', padx=5)

        fade_in(root)
        root.mainloop()

logger = Logger
