#!/usr/bin/env
import sys
import re

pattern = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')

try:
    lines = open("C:\\users\\dispareo\\desktop\\strings.txt", "r").readlines()
    
    for line in lines:
        if re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line):
            print(line)
except:
    print("no dice")