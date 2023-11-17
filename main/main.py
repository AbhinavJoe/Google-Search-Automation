import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import webbrowser
import subprocess
import os


file_location = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(file_location, '..', 'assets', 'icon.png')
url = 'https://www.google.com/search?q='

# valid websites can be changed to get curated search results from desired websites
valid_websites = [
    'reddit.com',
    'stackoverflow.com',
    'medium.com',
    'geeksforgeeks.org',
    'stackexchange.com',
    'quora.com'
]


def find_chrome_exe():
    try:
        result = subprocess.run(["where", "chrome.exe"],
                                capture_output=True, text=True, check=True)
        chrome_path = result.stdout.strip()
        return chrome_path
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


chrome_exe_path = find_chrome_exe()
print(chrome_exe_path)


def create_filter():
    filter = '('
    for index, website in enumerate(valid_websites):
        filter += 'site:' + website
        if index == len(valid_websites)-1:
            filter += ')'
        else:
            filter += ' OR '
    return filter


def create_url(query):
    return url + query + create_filter()


def search_google():
    user_input = search_entry_var.get()
    if not user_input:
        messagebox.showwarning(title='Error',
                               message='Please enter a valid search query.')
    else:
        final_url = create_url(user_input)
        webbrowser.get(chrome_exe_path).open(final_url)


# GUI Code
# root
root = ttk.Window(themename='cosmo')
root.title('Search Google')

root_pos_width = root.winfo_screenwidth() - 445
root_pos_height = root.winfo_screenheight() - 1030
root.geometry(f"425x75+{root_pos_width}+{root_pos_height}")

root.resizable(False, False)
root_icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, root_icon)
root.iconphoto(False, root_icon)


# widgets
search_entry_var = tk.StringVar()
search_entry = ttk.Entry(
    root, width=30, textvariable=search_entry_var)
search_entry.pack(side='left', padx=15, expand=1)

search_button = ttk.Button(root, text='Search', command=search_google)
search_button.pack(side='left', padx=15, expand=1)


# run
root.attributes('-topmost', True)
root.mainloop()
