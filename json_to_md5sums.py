"""Convert iceblock JSON to an md5sums file."""

from json import loads
from sys import argv

with open(argv[1], encoding="utf_8") as block:
    for entry in loads(block.read())["files"]:
        print(entry["hash"])
