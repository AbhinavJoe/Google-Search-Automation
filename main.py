# Have to make a floating tkinter application/window that will be on screen at all times until closed and will give google search return for the query typed in it.
# It will work in conjunction with the rest of the code.
import tkinter as tk
from tkinter import ttk
import webbrowser
import sys


url = 'https://www.google.com/search?q='

search = input('Search Google: ')

valid_websites = [
    'reddit.com',
    'stackoverflow.com',
    'medium.com',
    'geeksforgeeks.org',
    'stackexchange.com',
    'quora.com'
]

# The %s placeholder in chrome_path will be replaced by the URL when calling .open(final_url). The most basic usage is to insert values into a string with the %s placeholder.
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# https://www.google.com/search?q=what+does+a+google+query+look+like - This is what a google query looks like for a normal google search
# To get result from specific sites, we write the google search as shown below:
# python tutorial (site:geeksforgeeks.org OR site:medium.com) - This is what the create_filter() function does.


def create_filter():
    filter = '('
    for index, website in enumerate(valid_websites):
        filter += 'site:' + website
        if index == len(valid_websites)-1:
            filter += ')'
        else:
            filter += ' OR '
    return filter


def create_query():
    query = sys.argv[1:]
    # `' '.join()` pronounced space dot join is a nifty python function that joins all the strings of the sys.argv together.
    return ' '.join(query)


def create_url():
    if len(sys.argv[1:]) == 0:
        print('Error! Please enter a valid search query.')
    else:
        final_url = url + create_query() + create_filter()
        webbrowser.get(chrome_path).open(final_url)


create_url()
