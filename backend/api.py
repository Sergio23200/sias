#importacion de librerias
from datetime import date
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#importacion de paquetes
from db_cc import orm
#creacion de variables para el llamado de las librerias y pàquetes
app = FastAPI()
user_and_password_and_id = {}
templates = Jinja2Templates(directory="frontend") # ruta del directorio
# montando todos los archivos estaticos de la app 
app.mount("/fronted", StaticFiles(directory="frontend"), name="static_index")
app.mount("/frontend/inicio y registro", StaticFiles(directory="frontend/inicio y registro"), name="static_inicio_registro")
app.mount("/fronted/menu_user", StaticFiles(directory="frontend/menu_user"), name="static_menu_user")
#rutas get para visualizacion de archivos y extacion de datos para la visualcion
@app.get("/")
async def inicio(request: Request): # creacion de funcion para el llamado de las paginas  de inicio de sesion html
    email = user_and_password_and_id["email"] # verificacion si el usuario ya inicio sesion para redirigirlo a pagina princicpal
    if not email :#condicion para verifivar si no hay un email guardado en la variable email
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de la a pagina para el inicio de sesion
    else:#si hay un email se proces a enviar a la pagina principal
        return templates.TemplateResponse("index.html", {"request": request})#retorno a la pagina principal
@app.get("/registro/")#creacion de la funcion para el llamado de la pagina de registro html
async def registro(request: Request): # creacion de la funcion 
    return templates.TemplateResponse("/inicio y registro/registro.html", {"request": request})#retorno de a la pagina principal
@app.get("/comentarios/")# creacion de get para el retorno de la pagina de comentarios html
async def comentarios(request: Request):
    return templates.TemplateResponse("/menu_user/comment.html", {"request": request})#retorno de la pagina de la pagina de comentarios

@app.get("/index/")#creacion de metodo get para el retorno de la pagina principal 
async def index(request: Request):
    try:#manejo de error si el usuario no ha inicia sesion antes 
        id = user_and_password_and_id["email"]#verificacion de que hay un email en la variable usuarios
        return templates.TemplateResponse("index.html", {"request": request})#retorno a pagina principal si ha iniciado sesion
    except:
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de inicio de sesion si no ha iniciado

@app.get("/index/config/")#creacion de metodo get para  mostrar la pantalla de configuracion
async def configuracion(request: Request): #extracion de los detos hacia la base de datos para la visulacion dependiendo de cliente
    try:
        resultado = orm.get_affiliate_by_email(user_and_password_and_id['email']) #extracion de datos utilizando la funcion de busqueda 
        id = resultado['id']
        user_and_password_and_id
        fullname = resultado['fullname'] 
        email = resultado['email']
        document_type = resultado['document_type']  #extracion de datos en varibles 
        city = resultado['city']
        second_number = resultado['second_number']
        first_number = resultado['first_number']
        document_number = resultado['document_number']
        membership_type = resultado['membership_type']
        created_date = resultado['created_date']
        birthdate = resultado['birthdate']

        
        return templates.TemplateResponse("/menu_user/dates.html", {"request": request,
                                                                "id": id, "fullname": fullname, "email": email,
                                                                "number": first_number, "city": city,
                                                                "number_document": document_number,
                                                                "second_number": second_number,
                                                                "type_document": document_type,
                                                                "membership_type":membership_type,
                                                                "created_date":created_date, #retorno de variables para mostrarlas en el documento html
                                                                "birthdate":birthdate})
    except:
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno a la pagina de inicio de sesion si no ha iniciado
@app.get("/update_dates/")#metodo para el llamado a la pagina de actualizacion de datos
async def update_pg (request: Request):
    try:#verificacion de si el usuario inicio sesion
        user_and_password_and_id["email"]#
        return templates.TemplateResponse("/menu_user/update.html", {"request": request})#retorno de la a paginsa
    except:
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de la a paginsa
# creacion de los metodos post
@app.post("/sesion_r/")
async def consulta_usuario(request: Request, email: str = Form(...), password: str = Form(...)): #extracion de datos escritos pòr el usuario
    resultado = orm.authenticate_affiliate(email,password)
    if not resultado:  # creacion de condicion para dejar entrar al usuario  a la pagina principal si el usuaario se encuentra en la base de datos
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})
    else:
        user_and_password_and_id['email'] = email # se guarda el correo en una variable externa
        return templates.TemplateResponse("index.html", {"request": request})#retorno de la a

@app.post("/registro/")
async def submit_form(request: Request, fullname: str = Form(...), document_type: str = Form(...),
                      document_number: int = Form(...), email: str = Form(...),birthdate: date = Form(...),  city: str = Form(...),
                      first_number: int = Form(...), second_number: int = Form(...),password: str = Form(...), membership_type: str=Form(...)): #extracion de datos escritos pòr el usuario
    
    user_and_password_and_id["email"] = email # se guarda el correo en un variable externa

    orm.create_affiliates(fullname, document_type, document_number, birthdate, email, first_number, second_number, city, password, membership_type)
    return templates.TemplateResponse("index.html", {"request": request}) #retorno de la a paginsa
@app.post("/update/")
async def update(request: Request,  
                 email: str = Form(...),
                 second_number: str = Form(...),
                 first_number: str = Form(...),
                 city: str = Form(...), 
                 password: str = Form(...)):  # Extracción de datos escritos por el usuario

    email_auto = user_and_password_and_id["email"]

    # Llama a la función update_affiliate con los parámetros como un diccionario kwargs
    orm.update_affiliate(
        email_auto,  # El primer argumento posicional
        email=email,  # Argumentos de palabra clave
        second_number=second_number,
        first_number=first_number,
        city=city,
        password=password
    )

    return templates.TemplateResponse("index.html", {"request": request}) # Retorno de la página


@app.post("/delete/")
async def delete(request: Request):
    
     #se utiliza una variable externa para treaer el id 
    email = user_and_password_and_id["email"]
    orm.delete_affiliate(email)
    return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de la a paginsa
 