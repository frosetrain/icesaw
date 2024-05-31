# icesaw

A way to back up files

An iceblock is a tar archive of files. Each file's name starts with an ISO 8601 date, then an underscore, then the rest of the name. For example, `2024-05-31_file.txt`.

Each iceblock is stored together with a json file, with a list of files including the MD5 hash of each file.

I put my iceblocks into a [Tomb](https://dyne.org/software/tomb/)

## Scripts

gphotos.py: Google Takeout gives you a json file with each photo. It contains some metadata, which this script uses to timestamp the photos.

iceblock.py: The main file. Checks the new file hashes with hashes in existing iceblocks, to prevent duplicate files. It can delete duplicate files, then make an iceblock JSON file.

mtimes.py: Uses filesystem modification times to timestamp files.

rename.py: Renames files from any date format to ISO 8601
