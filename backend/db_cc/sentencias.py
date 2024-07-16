import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    password = "Sergi@123",
    database = "sias",
    port= "3306"
    )

def buscar_usuario(nombre_usuario):
    cursor = db.cursor()
    sentencia = "SELECT * FROM usuarios WHERE email = %s;"
    valores = (nombre_usuario,)
    cursor.execute(sentencia, valores)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados
def buscar_password(password):
    cursor = db.cursor()
    sentencia = "SELECT * FROM usuarios WHERE password = %s;"
    valores = (password,)
    cursor.execute(sentencia, valores)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados