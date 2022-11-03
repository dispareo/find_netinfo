import re
import sys
import whois
import socket
from urllib.parse import urlparse
from pprint import pprint
from ipwhois import IPWhois


  
# open and read file dynamically
with open(sys.argv[1]) as fh:
  string = fh.readlines()
    

# initializing the list objects
ip_candidates =[]
url_candidates =[]
  
# iterate over each line of the file (presumably strings.txt), extracting the potential IP addresses and URLS - this isn't foolproof but code rarely is
# There is definitely some stuff that's going to get caught in this that isn't an IP or URL - such as a SW version - but we can resolve and perform sanity checks later. 
for line in string:
    line = line.rstrip()
    prolly_an_IP = re.search(r"\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line)
    lookin_like_a_url = re.search(r"\b(https?://[^\s]+)", line)
    
    # put "what appears to be" valid IP addresses into the ip_candidates list
    if prolly_an_IP:
        ip_candidates.append(prolly_an_IP.group())
    
    #find what appears to be valid URLs/domains and put them into the url_candidates list
    if lookin_like_a_url:
        url_candidates.append(lookin_like_a_url.group())

#This explains a bit on the console, as I may actually use this for some IR stuff at ${day_job} and this could be a good start
#Its main value comes from not having to dig into the scripting code to figure this out :)

explanation = '''\n[!]The following are potential IPs.
[-]They could also be software versions or other numeric objects that matched the pattern.
[-] Be sure to investigate. \n\n[+] Potential IP : '''       

#Print all of the potential IPs
print(explanation + "\n[+] Potential IP : ".join(ip_candidates))



#Same explanation, except for URLs/domains
explanation_url = """\n\n[!]The following look like URLS or domains.
[-]Most were found using http/s, but some were using TLDs.
[-]Be sure to investigate. \n\n[+] Potential domain/URL : """       

#URLS - Print 'em all
print(explanation_url + "\n[+] Potential domain/URL : ".join(url_candidates))

#Resolving URL to IPS's - the end of the "print" function socket.gethostbyname(domain) is the "secret sauce" to resolving it.
#The rest just prints it nicely to console in case this makes its way into production for IR
for url in url_candidates:
    domain = urlparse(url).netloc
    print("\n[!] URL " + url + " is part of domain " + domain + " and maps to " + (socket.gethostbyname(domain)))




#Running through app IPs. First, check to see if they resolve to a FQDN. If not, perform WHOIS lookup to obtain more info. 
#Private IP's keep causing problems. Strain them out at the beginning and just pass. There's no reason to need a Private IP for whois anyway

for ip in ip_candidates:
    private_ip = re.search("^(10(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|((172\.(1[6-9]|2[0-9]|3[01]))|192\.168)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})$",ip)
    if private_ip:
        print("\n\n\n[!][!][!]IP {} is a Private IP and will cause issues. Investigate separately".format(ip))
    else:
        try:
            print("\n\n[-] Trying ip " +ip)
            host = socket.gethostbyaddr(ip)
            print("Host Name for the IP address {} is {}".format(ip, host))
        except:
            print("[-] The IP did not resolve to a PTR record. Running whois query to see if this provides better info: \n")
            who = IPWhois(ip)
            results = who.lookup_rdap(depth=1)
            print("[-] Whois information for {} is as follows: \n".format(ip))
            parsed_result = result['network']['name']
            pprint(parsed_result)
        else:
            print("IP timed out resolving. It still might be worth investigating manually")