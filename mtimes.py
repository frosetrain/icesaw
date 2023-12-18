"""Prepend the dates using file modification times."""

from datetime import date
from os import rename
from os.path import getmtime
from sys import argv

for f in argv[1:]:
    new_name = str(date.fromtimestamp(int(float(getmtime(f))))) + "_" + f
    print(new_name)
    rename(f, new_name)
