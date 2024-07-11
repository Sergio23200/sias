import mysql.connector
def db_conect ():
    db = mysql.connector.connect(
    host = "localhost",
    user="root",
    password = "Sergi@123",
    database = "sias",
    port= "3306"
    )
    return db
