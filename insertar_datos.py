import sqlite3


def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	SO = "Linux"
	Server = "Apache"
	url = "http://www.url3.com"
	Version_server = "4.4"
	Version_PHP = "7.0"
	print("Conectado a la bd" + db_file)
	insertar_datos(conexion, url, SO, Server, Version_server, Version_PHP)
	consulta_de_datos(conexion)
	conexion.commit()
	conexion.close()

def insertar_datos(conexion, url, SO, Server, Version_server, Version_PHP):
	consulta = conexion.cursor()
	campos = (url, SO, Server, Version_server, Version_PHP)
	sql_datos = """INSERT INTO datos(url, SO, Server, Version_server, Version_PHP)
	VALUES (?,?,?,?,?)"""
	if (consulta.execute(sql_datos, campos)):
		print ("Datos ingresados a la tabla")
	else:
		print ("No se ingresaron datos a la tabla")
	consulta.close()

def consulta_de_datos(conexion):
	consulta = conexion.cursor()

	sql = "SELECT * FROM datos"

	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0],columna[1],columna[2],columna[3],columna[4],columna[5])

	consulta.close()


crear_conexion("base_fuzzer.db")
