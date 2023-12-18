"""
Prepend the date using Google Photos JSON files.

Supply the JSON files as command-line arguments.
"""

from datetime import date
from json import loads
from os import rename
from os.path import exists
from sys import argv

for j in argv[1:]:
    if exists(j[:-5]):
        with open(j, "r", encoding="utf_8") as f:
            img_date = date.fromtimestamp(
                int(loads(f.read())["photoTakenTime"]["timestamp"])
            )
            print(img_date)
            rename(j[:-5], "{img_date}_gphoto_{j[:-5]}")
