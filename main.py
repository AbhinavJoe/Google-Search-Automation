import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from urllib.parse import quote_plus
import webbrowser
import subprocess
import os


# ── Paths ──────────────────────────────────────────────────────────────────────
_DIR          = os.path.dirname(os.path.abspath(__file__))
ICON_PATH     = os.path.join(_DIR, 'assets', 'icon.png')
WEBSITES_PATH = os.path.join(_DIR, 'data', 'valid websites.txt')

# ── Base search URLs ───────────────────────────────────────────────────────────
GOOGLE_URL        = 'https://www.google.com/search?q='
GOOGLE_AI_URL     = 'https://www.google.com/search?q={query}&udm=50'   # Google AI Mode (Chrome)
BING_COPILOT_URL  = 'https://www.bing.com/search?q={query}&showconv=1' # Copilot (Edge)
PERPLEXITY_URL    = 'https://www.perplexity.ai/search?q={query}'        # Perplexity (Firefox / default)


# ── Browser detection ──────────────────────────────────────────────────────────
def _find_exe(*names):
    """Return the first resolvable executable path from the given names."""
    for name in names:
        try:
            out = subprocess.run(
                ['where', name], capture_output=True, text=True, check=True
            ).stdout.strip()
            first = out.split('\n')[0].strip()
            if first:
                return first
        except subprocess.CalledProcessError:
            pass
    return None


def detect_browser():
    """Return (browser_id, exe_path) for the best available browser."""
    candidates = [
        ('chrome',  ['chrome.exe']),
        ('brave',   ['brave.exe']),
        ('edge',    ['msedge.exe']),
        ('firefox', ['firefox.exe']),
    ]
    for bid, names in candidates:
        path = _find_exe(*names)
        if path:
            return bid, path
    return 'default', None


# ── Website list ───────────────────────────────────────────────────────────────
def load_websites():
    """Load site-filter list from data file; fall back to built-in defaults."""
    defaults = [
        'reddit.com', 'stackoverflow.com', 'medium.com',
        'geeksforgeeks.org', 'stackexchange.com', 'quora.com',
    ]
    try:
        with open(WEBSITES_PATH, 'r') as f:
            sites = [
                line.strip().strip("'").rstrip(',').strip()
                for line in f
                if line.strip() and not line.startswith('#')
            ]
        return [s for s in sites if s] or defaults
    except FileNotFoundError:
        return defaults


# ── Initialise app state ───────────────────────────────────────────────────────
BROWSER_ID, BROWSER_PATH = detect_browser()
WEBSITES       = load_websites()
ai_mode_active = True

# Precompute the site-filter string used in normal (non-AI) searches
SITE_FILTER = '+(' + '+OR+'.join('site:' + s for s in WEBSITES) + ')'

AI_LABELS = {
    'chrome':  'Google AI',
    'brave':   'Google AI',
    'edge':    'Copilot',
    'firefox': 'Google AI',
    'default': 'Google AI',
}
AI_URLS = {
    'chrome':  GOOGLE_AI_URL,
    'brave':   GOOGLE_AI_URL,
    'edge':    BING_COPILOT_URL,
    'firefox': GOOGLE_AI_URL,
    'default': GOOGLE_AI_URL,
}


# ── Core helpers ───────────────────────────────────────────────────────────────
def open_in_browser(url):
    """Open *url* in the detected browser, falling back to the system default."""
    if BROWSER_PATH:
        try:
            subprocess.Popen([BROWSER_PATH, url])
            return
        except Exception:
            pass
    webbrowser.open(url)


def do_search(_event=None):
    query = search_var.get().strip()
    if not query:
        messagebox.showwarning('Error', 'Please enter a search query.')
        return

    encoded = quote_plus(query)
    if ai_mode_active:
        url = AI_URLS[BROWSER_ID].format(query=encoded)
    else:
        url = GOOGLE_URL + encoded + SITE_FILTER

    open_in_browser(url)
    search_var.set('')
    search_entry.focus_set()


def toggle_ai():
    global ai_mode_active
    ai_mode_active = not ai_mode_active
    if ai_mode_active:
        label = AI_LABELS[BROWSER_ID]
        ai_btn.configure(text=f'AI ON  [{label}]', bootstyle='success-outline')
    else:
        ai_btn.configure(text='AI OFF', bootstyle='secondary-outline')


# ── GUI ────────────────────────────────────────────────────────────────────────
root = ttk.Window(themename='cosmo')
root.title('Search Google')
root.resizable(False, False)
root.attributes('-topmost', True)

WIN_W, WIN_H = 460, 100
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f'{WIN_W}x{WIN_H}+{sw - WIN_W - 20}+40')

try:
    _icon = tk.PhotoImage(file=ICON_PATH)
    root.iconphoto(True, _icon)
except Exception:
    pass

# Row 1 ── search bar
row1 = ttk.Frame(root)
row1.pack(fill='x', padx=10, pady=(10, 3))

search_var = tk.StringVar()
search_entry = ttk.Entry(row1, textvariable=search_var)
search_entry.pack(side='left', fill='x', expand=True, padx=(0, 6))
search_entry.bind('<Return>', do_search)
search_entry.focus_set()

search_btn = ttk.Button(row1, text='Search', command=do_search, bootstyle='primary')
search_btn.pack(side='left')

# Row 2 ── AI mode toggle
row2 = ttk.Frame(root)
row2.pack(fill='x', padx=10, pady=(3, 10))

ai_btn = ttk.Button(
    row2, text=f'AI ON  [{AI_LABELS[BROWSER_ID]}]', command=toggle_ai,
    bootstyle='success-outline', width=20,
)
ai_btn.pack(side='right')

root.mainloop()
