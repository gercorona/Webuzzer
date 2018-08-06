import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	payload = '../../../../../../..'
	print("Conectado a la bd" + db_file)
	insertar_payload(conexion, payload)
	consulta_de_payload(conexion)
	conexion.commit()
	conexion.close()

def insertar_payload(conexion,payload):
	consulta = conexion.cursor()
	campo = payload
	sql_datos = """INSERT INTO Payload(Payload)
	VALUES (?)"""
	if(consulta.execute(sql_datos, (payload,))):
		print ("Datos ingresados a la tabla")
	else:
		print ("No se ingresaron datos a la tabla")
	consulta.close()

def consulta_de_payload(conexion):
	consulta = conexion.cursor()

	sql = "SELECT * FROM Payload"

	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0], columna[1])
	consulta.close()

crear_conexion("base_nueva.db")