# Google Search Automation — Instructions

A lightweight, always-on-top Python desktop utility that lets developers fire
filtered Google searches (or browser-native AI searches) without leaving their
current window.

---

## Table of Contents

1. [What This Project Does](#1-what-this-project-does)
2. [Project Structure](#2-project-structure)
3. [How the Code Works](#3-how-the-code-works)
4. [AI Search Mode](#4-ai-search-mode)
5. [Setup & Installation](#5-setup--installation)
6. [Running the App](#6-running-the-app)
7. [Customising the Site Filter List](#7-customising-the-site-filter-list)

---

## 1. What This Project Does

When you are deep in development and need a quick answer, you typically:

1. Alt-Tab to a browser
2. Open a new tab
3. Type your query
4. Manually add `site:stackoverflow.com OR site:reddit.com OR …` to narrow results

This tool collapses all of that into a single floating search bar that sits in the
**top-right corner of your screen, always on top of every other window**. You type
your query, press **Enter** (or click **Search**), and your browser opens the
pre-filtered Google result immediately. You never leave your editor.

There are two modes:

| Mode | What it does |
|------|-------------|
| **Normal** | Opens a Google search filtered to your curated list of developer sites |
| **AI** | Skips the filter and sends your query directly to the native AI of your detected browser |

---

## 2. Project Structure

```
Google Search Automation/
├── main.py                  # Entire application — one file
├── requirements.txt         # Third-party dependencies
├── Instructions.md          # This file
├── README.md                # Project overview
├── data/
│   └── valid websites.txt   # Editable list of sites used for filtering
└── assets/
    ├── icon.png             # Window title-bar icon (16 px)
    ├── logo.ico             # Windows taskbar icon
    └── logo.png             # Logo used in README / presentations
```

There is intentionally **no package structure, no build step, and no database**.
The entire runtime lives in `main.py`.

---

## 3. How the Code Works

`main.py` is divided into five clearly commented sections. Here is what each one does.

### 3.1 Paths (lines 10 – 13)

```python
_DIR          = os.path.dirname(os.path.abspath(__file__))
ICON_PATH     = os.path.join(_DIR, 'assets', 'icon.png')
WEBSITES_PATH = os.path.join(_DIR, 'data', 'valid websites.txt')
```

`_DIR` resolves to the folder that contains `main.py` regardless of where you
launch the script from. All other paths are built relative to it, so the app
works from any working directory.

### 3.2 Browser Detection (lines 22 – 49)

```python
def _find_exe(*names):
    ...

def detect_browser():
    candidates = [
        ('chrome',  ['chrome.exe']),
        ('edge',    ['msedge.exe']),
        ('firefox', ['firefox.exe']),
    ]
    ...
```

`_find_exe` calls the Windows `where` command to locate a browser executable.
`detect_browser` tries Chrome first, then Edge, then Firefox, and returns the
**first one found** as a `(browser_id, exe_path)` tuple.
If none are found it returns `('default', None)` and falls back to Python's
built-in `webbrowser.open()`.

The result is stored in two module-level constants:

```python
BROWSER_ID, BROWSER_PATH = detect_browser()
```

These are computed **once at startup** and reused for every search.

### 3.3 Website List (lines 52 – 77)

```python
def load_websites():
    ...

SITE_FILTER = '+(' + '+OR+'.join('site:' + s for s in WEBSITES) + ')'
```

`load_websites` reads `data/valid websites.txt` line by line, strips formatting
noise (quotes, trailing commas), and returns a clean Python list. If the file is
missing it silently falls back to a built-in default list of six developer sites.

`SITE_FILTER` is a pre-built URL fragment that looks like:

```
+(site:reddit.com+OR+site:stackoverflow.com+OR+site:medium.com+OR+...)
```

This fragment is appended to every normal-mode Google search URL.

### 3.4 Core Search Logic (lines 93 – 129)

#### `open_in_browser(url)`

Tries to launch the detected browser as a subprocess:

```python
subprocess.Popen([BROWSER_PATH, url])
```

Using `subprocess.Popen` directly (rather than the `webbrowser` module) handles
browser paths that contain spaces and avoids spawning an unnecessary shell
process. If this fails for any reason it falls back to `webbrowser.open(url)`.

#### `do_search(_event=None)`

The main event handler, bound to both the Search button and the `<Return>` key.

```python
encoded = quote_plus(query)          # URL-safe encoding of the user's input
if ai_mode_active:
    url = AI_URLS[BROWSER_ID].format(query=encoded)
else:
    url = GOOGLE_URL + encoded + SITE_FILTER
```

`quote_plus` converts spaces to `+` and encodes special characters so they
cannot corrupt the URL. After opening the URL, the entry field is cleared and
focus is returned to it so the next search can begin immediately.

#### `toggle_ai()`

Flips the `ai_mode_active` boolean and updates the button's text and colour to
reflect the new state.

### 3.5 GUI (lines 132 – 171)

Built with **ttkbootstrap** on top of Tkinter using the `cosmo` theme.

```
┌─────────────────────────────────────────────────┐
│  [  search entry field  ..................  ] [Search] │  ← row1
│                                      [AI OFF]   │  ← row2
└─────────────────────────────────────────────────┘
```

| Widget | Purpose |
|--------|---------|
| `row1` | Frame holding the entry field and Search button side by side |
| `search_entry` | Text input; `<Return>` is bound to `do_search` |
| `search_btn` | Triggers `do_search` on click |
| `row2` | Frame holding the AI toggle button |
| `ai_btn` | Calls `toggle_ai`; changes colour and label based on state |

Window positioning is calculated at runtime so it always appears in the
**top-right corner** regardless of screen resolution:

```python
root.geometry(f'{WIN_W}x{WIN_H}+{sw - WIN_W - 20}+40')
#                              ^^^^^^^^^^^^^^^^^^^^^^^^
#                              20 px from right edge, 40 px from top
```

`root.attributes('-topmost', True)` keeps the window above all other windows
at all times.

---

## 4. AI Search Mode

Clicking **AI OFF** toggles the app into AI mode. The button turns green and
shows the name of the AI engine that will be used.

| Detected browser | AI engine | URL pattern |
|-----------------|-----------|-------------|
| Chrome | Google AI Mode | `google.com/search?q=…&udm=50` |
| Edge | Bing Copilot | `bing.com/search?q=…&showconv=1` |
| Firefox / none | Perplexity | `perplexity.ai/search?q=…` |

In AI mode the site filter is **not** applied — the raw query goes straight to
the AI. This is intentional: AI assistants perform better with unrestricted
context than with `site:` constraints.

Toggle it off again at any time to return to filtered Google search.

---

## 5. Setup & Installation

### Prerequisites

- **Python 3.10 or newer** (developed on 3.12)
- A virtual environment is recommended but not required

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/AbhinavJoe/Google-Search-Automation.git
cd Google-Search-Automation

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install the only third-party dependency
pip install -r requirements.txt
```

`requirements.txt` contains:

```
ttkbootstrap>=1.10.1
```

Everything else (`tkinter`, `webbrowser`, `subprocess`, `os`, `urllib`) is part
of the Python standard library and requires no installation.

---

## 6. Running the App

```bash
python main.py
```

The window appears in the top-right corner of your screen. It stays on top of
all other windows.

| Action | Result |
|--------|--------|
| Type a query + press `Enter` | Fires the search |
| Click **Search** | Same as Enter |
| Click **AI OFF** | Switches to AI mode (button turns green) |
| Click **AI ON [engine]** | Switches back to normal filtered search |

---

## 7. Customising the Site Filter List

Open `data/valid websites.txt` and edit it. One domain per line:

```
reddit.com
stackoverflow.com
medium.com
geeksforgeeks.org
stackexchange.com
quora.com
```

Rules:
- Plain domain only — no `https://`, no `www.`, no `site:` prefix
- Lines starting with `#` are treated as comments and ignored
- Blank lines are ignored
- Changes take effect the next time you launch the app

If the file is deleted or missing the app falls back silently to the default
list of six sites shown above.
