#!/usr/bin/env python3
"""
Lookup NS IP addresses for a list of domain names and/or single domain name as necessary.
"""

__author__ = "Thomas Freeman"
__copyright__ = "Copyright 2022, Thomas Freeman"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Thomas Freeman"
__email__ = "thomas.freeman@sikich.com"
__status__ = "Production"

import argparse
import dns.resolver
import socket 


def parse_cli():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser(
    description='This script will lookup NS IP addresses for a list of domain names.')
    parser.add_argument('-d', '--domain',
                        help='A domain name to perform lookup on', required=False)
    parser.add_argument('-D', '--domainsfile',
                        help='List of domains file name to perform lookup on', required=False)
    parser.add_argument('-t', '--type',
                        help='Type of record to lookup (default = "A")', required=False, default="A")
    parser.add_argument('-v', '--verbose',
                        help='How much information to return', action=argparse.BooleanOptionalAction, default=False)
    return(parser.parse_args())
    
def main():
    """ Main entry point of the app """

    #Parse Command Line Arguments
    args=parse_cli()
    
    #Declare Variables
    verbose = args.verbose
    recordtype = args.type
    line = ""
    domain_records = {}
    dns_records = {}
    resolver=dns.resolver.Resolver()
    i = 0

    #Check for domains file and perform lookup on each one.
    if args.domainsfile:
        domainsfile=args.domainsfile
        with open(domainsfile) as f:
            domain_list = [line.strip() for line in f.readlines()]
        for domain in domain_list:
            try:
                a_record = dns.resolver.resolve(domain, recordtype)
                for ipval in a_record:
                    i=i+1
                    domain_records[i] = domain
                    dns_records[i] = ipval.to_text()
            except dns.resolver.NoAnswer:
                print (f'{domain}: No answer:')
        
    
    if args.domain:
        domain=args.domain
        try:
            a_record=dns.resolver.resolve(domain, recordtype)
            for ipval in a_record:
                i=i+1
                domain_records[i] = domain
                dns_records[i] = ipval.to_text()
        except dns.resolver.NoAnswer:
            print (f'{domain}: No answer:')
    
    #Print results
    i = 0
    for value in dns_records.items():
        i=i+1
        if verbose is False:
            print (f"{dns_records[i]}")
        else:
            print (f"{domain_records[i]}: {dns_records[i]}")
        
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
