import json
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (no recomendado para producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Definición del modelo de usuario
class Usuario(BaseModel):
    id: int
    username: str
    password: str

# Archivo JSON como "base de datos"
DATABASE_FILE = os.getenv("DATABASE_FILE")

def cargar_usuarios():
    try:
        with open(DATABASE_FILE, "r") as f:
            return [Usuario(**usuario) for usuario in json.load(f)]
    except FileNotFoundError:
        return []

def guardar_usuarios(usuarios: List[Usuario]):
    with open(DATABASE_FILE, "w") as f:
        json.dump([usuario.dict() for usuario in usuarios], f, indent=4)

usuarios = cargar_usuarios()

# Rutas de la API

@app.get("/usuarios", response_model=List[Usuario])
async def obtener_usuarios():
    return usuarios

@app.get("/usuarios/{id}", response_model=Usuario)
async def obtener_usuario(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: Usuario):
    if any(u.username == usuario.username for u in usuarios):
        raise HTTPException(status_code=400, detail="Nombre de usuario ya existe")
    usuarios.append(usuario)
    guardar_usuarios(usuarios)
    return usuario

@app.put("/usuarios/{id}", response_model=Usuario)
async def actualizar_usuario(id: int, usuario: Usuario):
    for i, u in enumerate(usuarios):
        if u.id == id:
            usuarios[i] = usuario
            guardar_usuarios(usuarios)
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id: int):
    for i, usuario in enumerate(usuarios):
        if usuario.id == id:
            del usuarios[i]
            guardar_usuarios(usuarios)
            return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")