from peewee import MySQLDatabase, AutoField, CharField, DateField, Model, IntegerField, IntegrityError #importacion de librerias 
import datetime # importacion para menjeo de fechas y hora
import bcrypt #importacion para el manejo del hash para la contraseñas

# Configuración de la base de datos
database = MySQLDatabase(
    'SIAS_sura',
    host='localhost',  
    port=3306,
    user='root',
    password='Sergi@123'
)


class affiliates(Model): # creacion de tablas
    id = AutoField() # llamado a llave primaria
    fullname = CharField(null=False)
    document_type = CharField(null=False)
    document_number = IntegerField(null=False)
    birthdate = DateField(null=False)
    email = CharField(index=True, unique=True, null=False)
    first_number = CharField(null=False)
    second_number = IntegerField()
    city = CharField(index=True, null=False)
    password = CharField(null=False)
    membership_type = CharField(null=False)
    created_date = DateField(default=datetime.date.today)
    
    class Meta:
        database = database
        db_table = 'affiliates' #confirmacion de elemento 

class admin(Model): # creacion de tablas 
    id = AutoField()
    fullname = CharField(null=False)
    document_type = CharField(null=False)
    document_number = IntegerField(null=False)
    birthdate = DateField(null=False)
    email = CharField(index=True, unique=True, null=False)
    first_number = CharField(null=False)
    second_number = IntegerField()
    city = CharField(index=True, null=False)
    password = CharField(null=False)
    job_title = CharField(null=False)
    created_date = DateField(default=datetime.date.today)
    
    class Meta:
        database = database
        db_table = 'admin' #confirmacion de elemento 

class create_appointment(Model):#confirmacion de elemento 
    id = AutoField() 
    create_by = CharField(null=False, index=True)
    create_date = DateField(default=datetime.date.today)
    appointment_type = CharField(null=False)
    hour = IntegerField(null=False)
    
    class Meta:
        database = database #confirmacion de elemento 
        db_table = 'create_appointment'

def create_affiliates(fullname, document_type, document_number, birthdate, email, first_number, second_number, city, password, membership_type):# cracion de metodo para la creacion de usuarios# cracion de metodo para la creacion de usuarios
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # pasar la contraseña a un hash para mayor seguridad
    new_user = affiliates(
        fullname=fullname,
        document_type=document_type,
        document_number=document_number, # definicinicion de datos 
        birthdate=birthdate,
        email=email,
        first_number=first_number,
        second_number=second_number,
        city=city,
        password=hashed_password.decode(),
        membership_type=membership_type
    )
    new_user.save()

def create_admin(fullname, document_type, document_number, birthdate, email, first_number, second_number, city, password, job_title):# creacion de funcion para la creacion de administradores
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) # pasar la contraseña a un hash para mayor seguridad
    new_user = admin(
        fullname=fullname,
        document_type=document_type,
        document_number=document_number,
        birthdate=birthdate,
        email=email, #datos a utilizar
        first_number=first_number,
        second_number=second_number,
        city=city,
        password=hashed_password.decode(),
        job_title=job_title,
    )
    new_user.save()

def authenticate_affiliate(email, password): # creacion de metodo para la autentificacion de usuarios
    try: # manejo de error
        affiliate = affiliates.get(affiliates.email == email) # verificacion de emeail
        if bcrypt.checkpw(password.encode(), affiliate.password.encode()): # verificacion de la contraseña por medio de hash
            return affiliate # retorno de el afiliado
        else: # si no se encontro el afiliado
            return None # se retorna nada
    except affiliates.DoesNotExist:
        return None  # se retorna nada
def delete_affiliate(email): # creacion de funcion para eliminar los afiliados
    query = affiliates.delete().where(affiliates.email == email) # sentencia sql que busca el usuario a eliminar por medio del email
    rows_deleted = query.execute() #ejecucion del query
    return rows_deleted
def update_affiliate(email_auto, **kwargs):
    try:
        # Buscar el afiliado en la base de datos usando el email proporcionado
        affiliate = affiliates.get(affiliates.email == email_auto)

        # Iterar sobre los argumentos proporcionados en kwargs
        for key, value in kwargs.items():
            # Verificar si el modelo tiene un atributo con el nombre de la clave
            if hasattr(affiliate, key):
                # Si la clave es 'password', hacer hash de la nueva contraseña
                if key == 'password':
                    affiliate.password = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
                else:
                    # Para otros campos, simplemente asignar el nuevo valor
                    setattr(affiliate, key, value)
        
        # Guardar los cambios en la base de datos
        affiliate.save()
        print("Afiliado actualizado exitosamente.")
    except affiliates.DoesNotExist:
        # Manejar el caso en que el afiliado con el email proporcionado no existe
        print(f"No se encontró un afiliado con el email {email_auto}.")
    except IntegrityError as e:
        # Manejar errores relacionados con restricciones de la base de datos, como duplicados
        print(f"Error al actualizar el afiliado: {e}")
    except Exception as e:
        # Capturar cualquier otro error y mostrar un mensaje
        print(f"Se produjo un error: {e}")


def get_affiliate_by_email(email):
    try:
        # Buscar el afiliado por su email
        affiliate = affiliates.get(affiliates.email == email)
        
        # Crear un diccionario con los datos del afiliado
        affiliate_data = {
            'id': affiliate.id,
            'fullname': affiliate.fullname,
            'document_type': affiliate.document_type,
            'document_number': affiliate.document_number,
            'birthdate': affiliate.birthdate,
            'email': affiliate.email,
            'first_number': affiliate.first_number,
            'second_number': affiliate.second_number,
            'city': affiliate.city,
            'password': affiliate.password,  # Nota: Nunca deberías exponer la contraseña real
            'membership_type': affiliate.membership_type,
            'created_date': affiliate.created_date,
        }
        
        return affiliate_data
    
    except affiliates.DoesNotExist:
        return None

if __name__ == '__main__':
        # Conectar a la base de datos
        database.connect()
        
        # Crear las tablas si no existen
        database.create_tables([affiliates, admin, create_appointment], safe=True)
