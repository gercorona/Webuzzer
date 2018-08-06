import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	print("Conectado a la bd" + db_file)
	consulta_de_payload(conexion)
	conexion.commit()
	conexion.close()

def consulta_de_payload(conexion):
	consulta = conexion.cursor()
	sql = "SELECT * FROM datosXpayload"
	
	if(consulta.execute(sql)):
		filas = consulta.fetchall()
		for columna in filas:
			print(columna[0],columna[1])
	consulta.close()

crear_conexion("base_nueva.db")