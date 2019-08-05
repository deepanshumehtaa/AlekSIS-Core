import requests
from django.utils.html import format_html

def parse():
    icons_raw = requests.get("https://raw.githubusercontent.com/google/material-design-icons/master/iconfont/codepoints").text

    icons_raw = icons_raw.splitlines()

    icons = [(i.split()[0], format_html('<i class="material-icons">{}</i>', i.split()[0])) for i in icons_raw]

    print(icons)
