#importacion de librerias
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#importacion de paquetes
from db_cc import conexion, class_databases
#creacion de variables para el llamado de las librerias y pàquetes
db = conexion.db_conect()
app = FastAPI()
user_and_password = {}
id_user = {}
person = class_databases.person()
templates = Jinja2Templates(directory="frontend") # ruta del directorio
# montando todos los archivos estaticos de la app 
app.mount("/fronted", StaticFiles(directory="frontend"), name="static_index")
app.mount("/frontend/inicio y registro", StaticFiles(directory="frontend/inicio y registro"), name="static_inicio_registro")
app.mount("/fronted/menu_user", StaticFiles(directory="frontend/menu_user"), name="static_menu_user")
#rutas get para visualizacion de archivos y extacion de datos para la visualcion
@app.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de la a paginsa

@app.get("/registro/")
async def registro(request: Request):
    return templates.TemplateResponse("/inicio y registro/registro.html", {"request": request})#retorno de la a paginsa

@app.get("/index/comentarios/")
async def comentarios(request: Request):
    return templates.TemplateResponse("/menu_user/comment.html", {"request": request})#retorno de la a paginsa

@app.get("/index/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})#retorno de la a paginsa

@app.get("/index/config/")
async def configuracion(request: Request): #extracion de los detos hacia la base de datos para la visulacion dependiendo de cliente
    resultado = person.log_in(user_and_password['user'], user_and_password['password'])

    id, fullname, email, number, password, city, number_document, laboratorios, historal, type_document = resultado[0]
    id_user['id'] = id
    return templates.TemplateResponse("/menu_user/dates.html", {"request": request,
                                                               "id": id, "fullname": fullname, "email": email,
                                                               "number": number, "password": password, "city": city,
                                                               "number_document": number_document,
                                                               "type_document": type_document})
@app.get("/update_dates/")
async def update_pg (request: Request):
    return templates.TemplateResponse("/menu_user/update.html", {"request": request})#retorno de la a paginsa
# creacion de los metodos post
@app.post("/sesion_r/")
async def consulta_usuario(request: Request, user: str = Form(...), password: str = Form(...)): #extracion de datos escritos pòr el usuario
    resultado = person.log_in(user, password) # se utiliza el metedo creado en la clase persona ppara verificar
    id_user['id'] = id # se guarda el id en una varible externa
    if not resultado:  # creacion de condicion para dejar entrar al usuario  a la pagina principal si el usuaario se encuentra en la base de datos
        return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})
    else:
        user_and_password['user'] = user # se guarda el usuario y contraseña en una variable externa
        user_and_password['password'] = password
        return templates.TemplateResponse("index.html", {"request": request})#retorno de la a paginsa

@app.post("/submit/")
async def submit_form(request: Request, nombre: str = Form(...), tipo_documento: str = Form(...),
                      numero_documento: int = Form(...), email: str = Form(...), ciudad: str = Form(...),
                      celular: int = Form(...), password: str = Form(...)): #extracion de datos escritos pòr el usuario
    user_and_password['user'] = nombre
    user_and_password['password'] = password
    user_and_password['tipo_docomuento'] = tipo_documento
    user_and_password['numero_documento'] = numero_documento# se guardan los datos en una varible externa
    user_and_password['email'] = email
    user_and_password['ciudad'] = ciudad
    user_and_password['celular'] = celular
    person.date(nombre, tipo_documento, numero_documento, email, ciudad, celular, password) # se guardan los datos en el metodo date
    person.create_user() # se utiliza el metedo para la creacion de usuarios
    return templates.TemplateResponse("index.html", {"request": request}) #retorno de la a paginsa
@app.post("/update/")
async def update(request: Request, fullname: str = Form(...), email: str = Form(...),
                 number_document: str = Form(...), number: str = Form(...),
                 city: str = Form(...), password: str = Form(...)):  #extracion de datos escritos pòr el usuario
    id = id_user["id"] #se utiliza una variable externa para treaer el id 
    id = int(id) #pasa la varible a entero para un mejor tipado
    person.update_user(id, fullname, number_document, email, city, number, password)
    return templates.TemplateResponse("index.html", {"request": request}) #retorno de la a paginsa
@app.post("/delete/")
async def delete(request: Request):
    id = id_user["id"] #se utiliza una variable externa para treaer el id 
    id = int(id) #pasa la varible a entero para un mejor tipado
    person.delete_user(id)
    return templates.TemplateResponse("/inicio y registro/inicio.html", {"request": request})#retorno de la a paginsa
