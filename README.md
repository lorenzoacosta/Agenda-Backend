# API de Turnos Médicos

API REST desarrollada con FastAPI para gestionar turnos médicos.

## Tecnologías
- Python
- FastAPI
- SQLite

## Funcionalidades
- Crear turnos
- Consultar turnos
- Consultar turnos por fecha
- Ver horarios disponibles
- Editar turnos
- Eliminar turnos

## Ejecutar el proyecto

pip install -r requirements.txt
uvicorn main:app --reload

## Endpoints principales

GET /turnos  
POST /turnos  
GET /turnos/fecha/{fecha}  
GET /turnos/disponibles/{fecha}  
PUT /turnos/{id}  
DELETE /turnos/{id}
