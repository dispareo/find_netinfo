#!/usr/bin/env
import sys

with open(sys.argv[1], 'r') as my_file:
    for line in my_file
        if line.startswith("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"):
            print(line)
