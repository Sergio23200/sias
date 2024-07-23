#CREANDO CLASE DE USUARIO
import mysql.connector # imporatndo la libreria de mysql
db = mysql.connector.connect( #creando la conexion con la base de datos
    host = "localhost",
    user="root",
    password = "Sergi@123",
    database = "sias",
    port= "3306"
    )
#creacion de clase
class person :
    def date (self,fullname,document_type,document_number,email,city,phone,password): # creacion de metodo para guardar los datos
        self.__fullname = fullname
        self.__document_type = document_type
        self.__document_number = document_number
        self.__email = email
        self.__city = city
        self.__phone = phone
        self.__password = password
    def create_user(self): # creacion de metodo para la creacion de usurio
        cursor = db.cursor() #llamado a la conexion a la base de datos
        sql = "INSERT INTO usuarios (username, tipo_documento, cedula, email, ciudad, telefono, password ) VALUES (%s, %s, %s, %s, %s,%s,%s)" #sentencia
        val = (self.__fullname,self.__document_type,self.__document_number
               ,self.__email, self.__city, self.__phone, self.__password,) #variables a utilizar
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
    def log_in(self,email,password): #creacion de metodo para la vereficacion de usuario
        self.__email = email
        self.__password = password
        cursor = db.cursor()
        sentencia = "SELECT * FROM usuarios WHERE email = %s AND password = %s;"
        valores = (self.__email,self.__password,)
        cursor.execute(sentencia, valores,)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def update_user(self, id: int, fullname: str, document_number: str, email: str, city: str, phone: str, password: str): # creacion de metodo para la actualizacion de datos 
        cursor = db.cursor()
        sentencia = "UPDATE usuarios SET username = %s, email = %s, telefono = %s, password = %s, ciudad = %s, cedula = %s WHERE id = %s;"
        valores = (fullname, email, phone, password, city, document_number, id)
        cursor.execute(sentencia, valores)
        db.commit()
        cursor.close()
    def delete_user(self,id): # creacion de metodo para la elimicacion de usuario
        cursor = db.cursor()
        sentencia = "DELETE FROM usuarios WHERE id = %s;"
        valores = (id,)
        cursor.execute(sentencia, valores)
        db.commit()
        cursor.close()
