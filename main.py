from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Response
from pydantic import BaseModel
import pymongo

client = pymongo.MongoClient("mongodb://havca1970:wIR3UCuOiYtAo9PL@ac-lywmls3-shard-00-00.z3iauxr.mongodb.net:27017,ac-lywmls3-shard-00-01.z3iauxr.mongodb.net:27017,ac-lywmls3-shard-00-02.z3iauxr.mongodb.net:27017/?ssl=true&replicaSet=atlas-d6ldgw-shard-0&authSource=admin&retryWrites=true&w=majority")

# Seleccionar la base de datos y la colección
db = client["bdescr"]
col = db["usuarios"]


app = FastAPI()

# Configurar CORS

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Usuario(BaseModel):
    nombre: str
    contra_correct: int
    token_correcto: int
    token1: str
    token2: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/usuarios")
async def agregar_usuario(usuario: Usuario):
    # Convertir el usuario en un diccionario
    user_dict = usuario.dict()

    # Buscar si ya existe un usuario con el mismo nombre
    existing_user = col.find_one({"nombre": user_dict["nombre"]})

    if existing_user:
        # Si ya existe un usuario con el mismo nombre, actualizarlo
        col.update_one({"nombre": user_dict["nombre"]}, {"$set": user_dict})
        mensaje = "Usuario actualizado exitosamente"
    else:
        # Si no existe un usuario con el mismo nombre, agregar el nuevo usuario
        col.insert_one(user_dict)
        mensaje = "Usuario agregado exitosamente"

    # Retornar una respuesta
    return {"mensaje": mensaje}


@app.get("/usuarios/{nombre}")
async def agregar_usuario(nombre: str):
    # Convertir el usuario en un diccionario
    usuario = col.find_one({"nombre": nombre})
    # Insertar el usuario en la colección
    if usuario:
        usuario["_id"] = str(usuario["_id"])
        return usuario
    # Retornar una respuesta
    return {"mensaje": "Usuario no encontrado"}


@app.put("/usuarios/{nombre}")
async def update_user_by_username(nombre: str, user_data: dict):
    
    result = col.update_one({"nombre": nombre}, {"$set": user_data})
    if result.modified_count == 1:
        return {"message": f"User with username {nombre} updated successfully."}
    else:
        return {"message": f"User with username {nombre} not found."}



@app.put("/ruta")
def ruta_put(response: Response):
    # tu lógica para procesar la solicitud PUT aquí

    # agregar los encabezados CORS necesarios en la respuesta
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "PUT"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    # retornar la respuesta adecuada
    return {"mensaje": "Solicitud PUT procesada correctamente"}
