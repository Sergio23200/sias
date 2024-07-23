import mysql.connector # imporatndo la libreria de mysql
def db_conect ():
    db = mysql.connector.connect( #creando la conexion con la base de datos
    host = "localhost",
    user="root",
    password = "Sergi@123",
    database = "sias",
    port= "3306"
    )
    return db
