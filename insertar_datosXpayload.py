import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	#conexion.commit()
	#conexion.close()
	return conexion


def insertar_datosXpayload(conexion,url_id,pay_id):
	consulta = conexion.cursor()
	campos = (url_id,pay_id) # id_dato y id_payload
	sql_datos = """INSERT INTO datosXpayload(id_dato,id_Payload)
	VALUES (?,?)"""
	if(consulta.execute(sql_datos, (campos))):
		#print ("Datos ingresados a la tabla")
		consulta.close()
		conexion.commit()
	else:
		consulta.close()
	

def consulta_de_datosXpayload(conexion):
	consulta = conexion.cursor()

	sql = "SELECT * FROM datosXpayload"

	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0], columna[1])
	consulta.close()

#crear_conexion("base_nueva.db")