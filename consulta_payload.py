import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	print("Conectado a la bd" + db_file)
	consulta_de_payload(conexion)
	conexion.commit()
	conexion.close()

def consulta_de_payload(conexion):
	consulta = conexion.cursor()
	so = "Linux"
	server = "Apache"
	Ver_server = "2.4"
	Ver_PHP = "5.0"
	sql = "SELECT id_dato FROM datos WHERE SO LIKE (?) AND Server LIKE (?) AND Version_server LIKE (?) AND Version_PHP LIKE (?)"
	
	if(consulta.execute(sql,(so,server,Ver_server,Ver_PHP))):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0])
			payload = "SELECT Payload FROM Payload INNER JOIN datosXpayload WHERE id_dato LIKE (?)"
			if (consulta.execute(payload, (columna[0],))):
				res = consulta.fetchall()
				for valor in res:
					print(valor[0])

	consulta.close()

crear_conexion("base_nueva.db")