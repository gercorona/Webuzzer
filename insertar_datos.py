import sqlite3
from time import sleep

def crear_conexion(db_file,v):
	conexion = sqlite3.connect(db_file)
	print("{}".format("\n>> Connected to "+db_file+" database" if v else ""),end="")
	if v: sleep(0.8)
	#conexion.commit()
	#conexion.close()
	return conexion

def saludo(name):
	print("Hola {}".format(name))

def cerrar_conexion(connection):
	connection.close()

def insertar_datos(conexion, url, SO, Server, Version_server, Version_PHP,v):
	if v:
		print("\n >> Inserting data ....",end="") 
		sleep(0.6)
	id_inserted = None
	consulta = conexion.cursor()
	campos = (url, SO, Server, Version_server, Version_PHP)
	sql_datos = """INSERT INTO datos(url, SO, Server, Version_server, Version_PHP)
	VALUES (?,?,?,?,?)"""
	if (consulta.execute(sql_datos, campos)):
		id_inserted = consulta.lastrowid
	else:
		pass
	consulta.close()
	conexion.commit()
	return id_inserted

def consulta_de_datos(conexion,url):
	consulta = conexion.cursor()

	sql = "SELECT id_dato FROM datos WHERE url LIKE (?)"

	if(consulta.execute(sql,(url,))):
		reg = consulta.fetchall()
		if reg:
			#YA EXISTE!
			for columna in reg:
				return columna[0]
		else:
			#NO EXISTE!
			return None
		

			#print(columna[0],columna[1],columna[2],columna[3],columna[4],columna[5])
	else:
		print("\n -- URL not found\n")		

	consulta.close()
	return


#crear_conexion("base_fuzzer.db")
