"""Rename files such that their dates follow ISO 8601."""

from os import rename
from sys import argv
from sys import exit as sys_exit

# Original name format syntax
# ....YYYY.MM.DD.X

if len(argv) < 3:
    print("sus")
    sys_exit()

ogfmt = argv[1].upper()

year_pos = -1
month_pos = -1
day_pos = -1
name_pos = -1
year_short = -1

if "YYYY" in ogfmt:
    year_pos = ogfmt.index("YYYY")
    year_short = False
elif "YY" in ogfmt:
    year_pos = ogfmt.index("YY")
    year_short = True

if "MM" in ogfmt:
    month_pos = ogfmt.index("MM")

if "DD" in ogfmt:
    day_pos = ogfmt.index("DD")

if "X" in ogfmt:
    name_pos = ogfmt.index("X")

if any(n == -1 for n in (year_pos, month_pos, day_pos, name_pos, year_short)):
    print("Original date format is incomplete!")
    sys_exit()

# print(year_pos, month_pos, day_pos, year_short)

for f in argv[2:]:
    if year_short:
        year_len = 2
    else:
        year_len = 4
    iso_date = "-".join(
        (
            f[year_pos : year_pos + year_len],
            f[month_pos : month_pos + 2],
            f[day_pos : day_pos + 2],
        )
    )
    new_name = iso_date + "_" + f[name_pos:]
    print(new_name)
    rename(f, new_name)
