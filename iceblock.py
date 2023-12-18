"""Check for duplicates using MD5 hashes, and print the block json."""

from datetime import date
from hashlib import md5
from json import dump, dumps, loads
from os import listdir, remove
from os.path import exists

from rich.progress import track

BUF_SIZE = 1048576  # read 1 MiB at a time when hashing


class DateFormatError(Exception):
    """Raised when a file does not conform to the ISO 8601 format."""

    def __init__(self, file="A file"):
        self.file = file
        super().__init__(f"{self.file} does not conform to ISO 8601")


hashes = {}


def hash_dir(dire: str, ignore_json: bool, out_file: str):
    """Generate MD5 hashes for all files in a directory, using hashlib.

    Args:
        dire (str): The directory to hash
        ignore_json (bool): Whether to skip JSON files.
        out_file (str): The output md5sums file.
    """
    if exists(out_file):
        remove(out_file)
    with open(out_file, "a", encoding="utf_8") as of:
        for f in track((listdir(dire)), description=f"hashing {dire}..."):
            if "json" in f and ignore_json:
                continue
            md5sum = md5()
            with open(dire + f, "rb") as binf:
                data = True
                while data:
                    data = binf.read(BUF_SIZE)
                    md5sum.update(data)
            of.write(md5sum.hexdigest() + "  " + f + "\n")


def load_json(json_file: str):
    """Load MD5 hashes from an iceblock JSON file.

    Args:
        json_file (str): The JSON file to load
    """
    with open(json_file, "r", encoding="utf_8") as json:
        for f in loads(json.read())["files"]:
            hashes[f["hash"]] = f["filename"]


def load_md5sums(md5_file: str):
    """Load MD5 hashes from an md5sums file.

    Args:
        md5_file (str): The md5sums file to load
    """
    with open(md5_file, "r", encoding="utf_8") as sums:
        for line in sums.readlines():
            md5sum = line[0:32].strip()
            filename = line[34:].strip()
            hashes[md5sum] = filename


def check_dir(d: str, delete=False):
    """Check for hash collisions between the new files and existing files.

    Args:
        d (str): Directory containing new files to be checked
        delete (bool): Whether to delete one copy of each duplicate file.
    """
    with open(f"{d[:-1]}.md5sums", encoding="utf_8") as sums:
        for f in sums.readlines():
            md5sum = f[0:32].strip()
            filename = f[34:-1].strip()
            g = hashes.get(md5sum)
            if g is not None:
                print("collision", g, filename)
                if delete:
                    remove(filename)
            else:
                hashes[md5sum] = filename


def make_block(new: str):
    """Create an iceblock dict.

    Args:
        new (str): Path to the new iceblock

    Raises:
        DateFormatError: A file does not conform to the ISO 8601 date format.
    """
    block = {
        "blockId": 1,
        "date": date.today().isoformat(),
        "count": len(listdir(new)),
        "files": [],
    }
    for file in track(listdir(new)):
        if (
            int(file[0:4])
            and int(file[5:7])
            and int(file[8:10])
            and file[4] == "-"
            and file[7] == "-"
            and file[10] == "_"
        ):
            md5sum = md5()
            with open(new + file, "rb") as f:
                data = True
                while data:
                    data = f.read(BUF_SIZE)
                    md5sum.update(data)
            file_dict = {
                "filename": file,
                "date": file[:10],
                "hash": md5sum.hexdigest(),
            }
            block["files"].append(file_dict)
        else:
            print(file)
            raise DateFormatError


def dump_block(block: dict, out_file: str = None) -> None:
    """Write an iceblock JSON to a file or stdout.

    Args:
        block (dict): The iceblock.
        out_file (str, optional): Path to the output file, or None for stdout.
    """
    if out_file:
        with open(out_file, "w", encoding="utf_8") as f:
            dump(block, f, separators=(",", ":"))
    else:
        print(dumps(block, indent=4))


# ARCTIC = "/home/zixi/arctic/"
GO_IN = "/home/zixi/b2/"
HAHA = "/home/zixi/Downloads/photos/"

load_json("/run/media/zixi/.arc0/b0.json")
load_json("/run/media/zixi/.arc0/b1.json")
hash_dir(GO_IN, False, GO_IN[0:-1] + ".md5sums")
hash_dir(HAHA, False, HAHA[0:-1]+".md5sums")
check_dir(GO_IN)
check_dir(HAHA)
