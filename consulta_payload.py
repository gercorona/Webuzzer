import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)	
	return conexion

def cerrar_conexion(connection):
	connection.close()

def consulta_de_payload(conexion,datos,_list):
	print("  ......")
	ret = False
	consulta = conexion.cursor()
	so = datos[1]
	server = datos[2]
	Ver_server = datos[3]
	Ver_PHP = datos[5]
	sql = "SELECT id_dato FROM datos WHERE SO LIKE (?) AND Server LIKE (?) AND Version_server LIKE (?) AND Version_PHP LIKE (?)	"
	
	if(consulta.execute(sql,(so,server,Ver_server,Ver_PHP))):
		filas = consulta.fetchall()
		for columna in filas:
			#payload = "SELECT Payload FROM Payload INNER JOIN datosXpayload WHERE id_dato LIKE (?)"
			payload = "SELECT d.id_dato,dp.id_Payload,p.Payload FROM datos d INNER JOIN datosXpayload dp ON d.id_dato=dp.id_dato INNER JOIN Payload p ON p.id_Payload=dp.id_Payload WHERE d.id_dato = (?)"
			if (consulta.execute(payload, (columna[0],))):
				res = consulta.fetchall()
				ret = True
				for valor in res:
					_list.append(valor[2])
	consulta.close()
	conexion.commit()
	return ret,_list

#crear_conexion("base_nueva.db")