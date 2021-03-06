import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	#conexion.commit()
	#conexion.close()
	return conexion

def cerrar_conexion(connection):
	connection.close()

def insertar_payload(conexion,payload):
	id_inserted = None
	consulta = conexion.cursor()
	campo = payload
	sql_datos = """INSERT INTO Payload(Payload)
	VALUES (?)"""
	if(consulta.execute(sql_datos, (campo,))):
		id_inserted=consulta.lastrowid
	else:
		print("\n"+"-"*10,end="")
	consulta.close()
	#conexion.commit()
	return id_inserted

def consulta_de_payload(conexion):
	consulta = conexion.cursor()

	sql = "SELECT * FROM Payload"

	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0], columna[1])
	consulta.close()

#crear_conexion("base_nueva.db")