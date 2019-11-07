#Author: Bryan Bijonowski
#Date Created: 20191106
#Date Modified: 20191106
#Purpose: Ingest a file containing IP's with a newline delimiter, and
#sort them numerically, returning the output to stdout.

###Imports###

import sys
from ipaddress import ip_address

###Main Body###

def main():
    """Takes in a file of IP addresses as an argument, reads it, and sorts them numerically, returning the output to stdout"""
    
    try:
   
        if len(sys.argv) < 2 or len(sys.argv) > 2:
            """"Checks that at least and no more than one argument is passed."""
            
            print("Please provide ONE argument of a file containing IP Addresses!: ip_sorter.py <file_containing_ips>")
            sys.exit()
            
            
        with open(sys.argv[1], "r") as ip_file:
            """Opens ingested file containing presumably IP Addresses, reading each line, validating against known requirements of what constitutes a valid IP Address, 
            and then sorts the IP Addresses numerically."""
            
            if len(ip_file.readlines()) <= 1:
                """Checks to ensure the file being read in has at least two items to sort"""
                
                print("Please provide a list of IP's containing at least two IP Addresses to sort!")
                sys.exit()  
            
            ip_file.seek(0,0) #Returns pointer back to the beginning of the file.
            
            valid_ips = [ip.strip() for ip in ip_file.readlines() if ip_address(ip.strip())] #Ensures each element provided is a valid IP.
                                         
            ip_list_sorted = sorted(valid_ips, key = lambda ip: tuple(map(int, ip.split('.'))))
            
            print(ip_list_sorted, file=sys.stdout)
     
    except ValueError as E:
        """Validates the contents of the file as a catchall"""
        
        print("Please provide a file containing IP Addresses ONLY.", E)
        

###Protection###

if __name__ == "__main__":
    main()