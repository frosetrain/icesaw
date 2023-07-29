from hashlib import md5
from json import dumps as json_dumps
from os import listdir

from rich.progress import track

BUF_SIZE = 65536  # bytes to read for hashing, avoids large memory use

arctic = "/home/zixi/arctic/"  # the big Arctic Vualt
origin = "/home/zixi/archive/"  # the block that is being added

block = {"blockId": 0, "date": "2023-07-29", "count": len(listdir(origin)), "files": []}

for file in listdir(origin):
    if (
        int(file[0:4])
        and int(file[5:7])
        and int(file[8:10])
        and file[4] == "-"
        and file[7] == "-"
        and file[10] == "_"
    ):
        md5sum = md5()
        with open(origin + file, "rb") as f:
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
        raise ValueError

print(json_dumps(block, separators=(",", ":")))
