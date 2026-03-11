from pydantic import BaseModel
from datetime import date, time

class Turno(BaseModel):
    nombre: str
    fecha: date #formato YYYY-MM-DD
    hora: time #formato HH:MM
    motivo: str