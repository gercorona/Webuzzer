import sqlite3


def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	SO = "Windows"
	Server = "ISS"
	url = "http://www.url.com"
	Version_server = "2.3.4"
	Version_PHP = "7.0"
	print("Conectado a la bd" + db_file)
	insertar_datos(conexion, url, SO, Server, Version_server, Version_PHP)
	consulta_de_datos(conexion)
	conexion.commit()
	conexion.close()

def insertar_datos(conexion, url, SO, Server, Version_server, Version_PHP):
	consulta = conexion.cursor()
	campos = (url, SO, Server, Version_server, Version_PHP)
	sql = """INSERT INTO datos(url, SO, Server, Version_server, Version_PHP)
	VALUES (?,?,?,?,?)"""

	if (consulta.execute(sql,campos)):
		print ("Datos ingresados a la tabla")
	else:
		print ("No se ingresaron datos a la tabla")
	consulta.close()

def consulta_de_datos(conexion):
	consulta = conexion.cursor()

	sql = "SELECT * FROM datos"

	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for fila in filas:
			print(fila[0],fila[1],fila[2],fila[3],fila[4])

	consulta.close()


crear_conexion("base_fuzzer.db")
