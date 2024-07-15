#!/usr/bin/env python3
"""
# Copy or sync files locally:
rsync -zvh [Source-Files-Dir] [Destination]

# Copy or sync directory locally:
rsync -zavh [Source-Files-Dir] [Destination]

# Copy files and directories recursively locally:
rsync -zrvh [Source-Files-Dir] [Destination]

"""

# In order to use the rsync command in Python, use
# the subprocess module by calling call methods and
# passing a list as an argument:
import subprocess

src = "data/prod/" # replace <source-path> with the source directory
dest = "data/prod_backup/" # replace <destination-path> with the destination directory

subprocess.call(["rsync", "-arq", src, dest])

