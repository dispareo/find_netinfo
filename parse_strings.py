#!/usr/bin/env
import sys
import re

pattern = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

match = re.search(pattern, sys.argv[1])

if match != None: 
    
    # We reach here when the expression "([a-zA-Z]+) (\d+)" 
    # matches the date string. 
    
    # This will print [14, 21), since it matches at index 14 
    # and ends at 21.  
    print("Match at index % s, % s" % (match.start(), match.end()))
    
    # We us group() method to get all the matches and 
    # captured groups. The groups contain the matched values. 
    # In particular: 
    # match.group(0) always returns the fully matched string 
    # match.group(1) match.group(2), ... return the capture 
    # groups in order from left to right in the input string 
    # match.group() is equivalent to match.group(0) 
    
    # So this will print "June 24" 
    print("Full match: % s" % (match.group(0)))
    
    # So this will print "June" 
    print("Month: % s" % (match.group(1)))
    
    # So this will print "24" 
    print("Day: % s" % (match.group(2)))
    
else: 
    print("The regex pattern does not match.")