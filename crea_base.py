import sqlite3

def crear_conexion(db_file):
	conexion = sqlite3.connect(db_file)
	print("Conexion exitosa a la bd")
	crear_tablas(conexion)
	conexion.commit()
	conexion.close()
	

def crear_tablas(conexion):
	consulta = conexion.cursor()
	sql="""CREATE TABLE IF NOT EXISTS datos (
	id_dato integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	url text NOT NULL,
	SO text NOT NULL,
	Server text NOT NULL,
	Version_server text NOT NULL,
	Version_PHP text
	)"""
	sql1="""
	CREATE TABLE IF NOT EXISTS Payload(
	id_Payload integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	Payload text NOT NULL
	)"""
	sql2="""
	CREATE TABLE IF NOT EXISTS datosXpayload(
	id_dato integer,
	id_Payload integer,
	PRIMARY KEY (id_dato,id_Payload),
	FOREIGN KEY (id_dato) REFERENCES datos (id_dato),
	FOREIGN KEY (id_Payload) REFERENCES Payload (id_Payload)
	)"""

	if (consulta.execute(sql)): 
		print ("Tabla datos creada! ")
	else: 
		print("No se creo la tabla datos") 
	if (consulta.execute(sql1)): 
		print ("Tabla Payload creada! ")
	else: 
		print("No se creo la tabla Payload")
	if (consulta.execute(sql2)): 
		print ("Tabla datosXpayload creada! ")
	else: 
		print("No se creo la tabla datosXpayload")
	consulta.close()

crear_conexion("fuzzer_db.db")
