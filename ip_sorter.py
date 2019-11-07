#Author: Bryan Bijonowski
#Date Created: 20191106
#Date Modified: 20191106
#Purpose: Ingest a file containing IP's with a newline delimiter, and
#sort them numerically, returning the output to stdout.

###Imports###

import sys


###Main Body###

def main():
    """Takes in a file of IP addresses as an argument, reads it, and sorts them numerically, returning the output to stdout"""

    with open(sys.argv[1], "r") as ip_file:
        
       ip_list = [ip.strip() for ip in ip_file.readlines()]
       ip_list_sorted = sorted(ip_list, key = lambda ip: tuple(map(int, ip.split('.'))))
       print(ip_list_sorted, file=sys.stdout)
     
        

###Protection###

if __name__ == "__main__":
    main()



