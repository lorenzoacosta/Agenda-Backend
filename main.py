from fastapi import FastAPI
from routes.turnos import router as turnos_router
from database import crear_tabla

app = FastAPI()

crear_tabla()

@app.get("/")
def inicio():
    return {"mensaje": "Servidor funcionando"}

app.include_router(turnos_router)