# Mi primer API
Desarrollare un API utilizando FastAPI utilizando un archivo JSON para almacenar información como si fuera una base de datos.

## Verificación de requerimientos
1. Tener python instalado
```
> python --version
```

## Entorno virtual
* Crear un entorno virtual
```
> python3 -m venv mi-entorno-virtual
```
* Activar el entorno virtual
```
> source mi-entorno-virtual/bin/activate
```
* Para desactivar el entorno virtual:
```
deactivate
```
## Instalar requerimientos
```
> pip install fastapi uvicorn pydantic python-dotenv
> pip install -r requirements.txt
```
Si se requiere alguna otra librería se utilizará
```
> pip install nombre_de_la_librería
```

## Ejecutar API
```
> uvicorn main:app --host 0.0.0.0 --port 8000
```