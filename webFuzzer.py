#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apt-get install python3-requests
apt-get install python3-nmap
pip3 install ipaddress

"""

import nmap, socket, argparse
from urllib.parse import urlparse
import ipaddress as ipa
from requests import head,get

nm = nmap.PortScanner()

def scanningHost(url):
    url_object = urlparse(url)
    host,protocol = getHost(url_object)
    print("\nHOST: {}".format(host))
    print(type(host))
    #Nmap library
    scann = nm.scan(host,'80,443','-O')
    print(scann)
    os = getOpSystem(scann,host)
    print("\nO.S.: {}".format(os))
    #Requests Library
    server = None
    php_v = None
    _url = None
    try:
        header=head(protocol+'://'+host)
        print("STATUS CODE: {}".format(header.status_code))
        if 'Server' in header.headers:
            server = header.headers['Server']
        if 'X-Powered-By' in header.headers:
            php_v = header.headers['X-Powered-By']
        if header.status_code > 400:
            print("URL: {}".format(header.url))
            print("STATUS CODE: {}".format(header.status_code))
        #print(header.headers)
        elif header.status_code in range(200,209,1):
            _url = url
        elif header.status_code in range(300,304,1):
            ##Redireccion
            _url = header.headers['Location']


    except Exception as e:
        print("NOOOOO!")
        print(e)
        print(type(e))
    if server is not None:
        server,srv_ver = parseServer(server)
    print("URL: {}".format(_url))
    print("SERVER: {}".format(server))
    print("PHP VERSION: {}".format(php_v))

def parseServer(srv):
    return srv,None

def getHost(URLobject):
    netloc = URLobject.netloc
    proto = URLobject.scheme
    print(netloc)
    try:
        ip_add = ipa.ip_address(netloc)
        print(ip_add)
        return str(ip_add),proto
    except ValueError:
        ##domain_name
        return socket.gethostbyname(netloc),proto
    
def getOpSystem(sc,ip):
    try:
        return sc['scan'][ip]['osmatch'][0]['name']
    except Exception as e:
        print("CHALE:\n")
        print(e)
        print(type(e))
    return

parser = argparse.ArgumentParser(description='Python Script that performs fuzzing targeting web servers')
parser.add_argument(
    'target', type=str, nargs=1, help='URL that\'ll be fuzzed'
    )
parser.add_argument(
    '-p','--payload',dest='a_payload', action='store_true',default=False,help='Set the payload to use'
    )
parser.add_argument(
    '-f','--pfile',dest='pay_file', type=str,help='Use the choosen PAY_FILE file from which payloads will be get'
    )
parser.add_argument(
    '-v','--verbose',dest='verbose',action='store_true',default=False,help='Enable verbosity mode'
    )

if __name__ == '__main__':
    try: 
        args = parser.parse_args()
        print(args.target[0])
        print(args.a_payload)
        print(args.pay_file)
        print(args.verbose)
        scanningHost(args.target[0])

    except Exception as e:
        print(e)
        print(type(e))