import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import subprocess


url = 'https://www.google.com/search?q='

valid_websites = [
    'reddit.com',
    'stackoverflow.com',
    'medium.com',
    'geeksforgeeks.org',
    'stackexchange.com',
    'quora.com'
]

# The %s placeholder in chrome_path will be replaced by the URL when calling .open(final_url). The most basic usage is to insert values into a string with the %s placeholder.
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'


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
        print('Error! Please enter a valid search query.')
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
root_icon = tk.PhotoImage(file='doc/images/icon.png')
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
