from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db_cc import conexion
db = conexion.db_conect()
app = FastAPI()
templates = Jinja2Templates(directory="../frontend")
@app.get("/")
async def inicio (request: Request):
    app.mount("/static", StaticFiles(directory="../frontend/inicio y registro"), name="static")
    return templates.TemplateResponse("/inicio y registro/inicio.html",{"request":request})

@app.get("/index/")
async def inicial(request: Request):
    app.mount("/static", StaticFiles(directory="../frontend"), name="static")
    return  templates.TemplateResponse("index.html",{"request":request}) 
@app.post("/submit/")
async def submit_form(request: Request, nombre: str = Form(...), correo: str = Form(...),
                    numero_documento: str = Form(...), contraseña: str = Form(...) ):
        cursor = db.cursor()
        sql = "INSERT INTO usuarios (username, email,cedula,password) VALUES (%s, %s,%s, %s)"
        val = (nombre, correo,numero_documento,contraseña)
        cursor.execute(sql, val)
        db.commit()
        cursor.close() 
        return templates.TemplateResponse("index.html", {"request": request, "nombre": nombre})
@app.get("/registro/")
async def registro(request: Request):
    app.mount("/static", StaticFiles(directory="../frontend/inicio y registro"), name="static")
    return templates.TemplateResponse("/inicio y registro/registro.html",{"request":request})
    
