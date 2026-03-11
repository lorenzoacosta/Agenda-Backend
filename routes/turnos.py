from fastapi import APIRouter, HTTPException
from models import Turno
from database import get_connection

router = APIRouter()

HORARIOS_POSIBLES = [
    "08:00","09:00","10:00","11:00",
    "12:00","13:00","14:00","15:00",
    "16:00"
]


@router.get("/turnos")
def obtener_turnos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM turnos ORDER BY fecha, hora")
    turnos = cursor.fetchall()

    conn.close()

    return [dict(t) for t in turnos]

@router.post("/turnos")
def crear_turno(turno: Turno):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM turnos WHERE fecha = ? AND hora = ?",
        (str(turno.fecha), str(turno.hora))
    )

    existente = cursor.fetchone()

    if existente:
        conn.close()
        raise HTTPException(status_code=400, detail="Ya existe un turno en ese horario")

    cursor.execute(
        """
        INSERT INTO turnos (nombre, fecha, hora, motivo)
        VALUES (?, ?, ?, ?)
        """,
        (turno.nombre, str(turno.fecha), str(turno.hora), turno.motivo)
    )

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return {
        "id": nuevo_id,
        "nombre": turno.nombre,
        "fecha": turno.fecha,
        "hora": turno.hora,
        "motivo": turno.motivo
    }


@router.get("/turnos/fecha/{fecha}")
def obtener_turnos_por_fecha(fecha: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM turnos WHERE fecha = ? ORDER BY hora",
        (fecha,)
    )

    turnos = cursor.fetchall()
    conn.close()

    return [dict(t) for t in turnos]

@router.get("/turnos/disponibles/{fecha}")
def obtener_horarios_disponibles(fecha: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT hora FROM turnos WHERE fecha = ?",
        (fecha,)
    )

    turnos = cursor.fetchall()
    conn.close()

    horarios_ocupados = [t["hora"] for t in turnos]

    horarios_disponibles = [
        hora for hora in HORARIOS_POSIBLES
        if hora not in horarios_ocupados
    ]

    return horarios_disponibles


@router.get("/turnos/{id}")
def obtener_turno(id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM turnos WHERE id = ?",
        (id,)
    )

    turno = cursor.fetchone()
    conn.close()

    if turno:
        return dict(turno)

    raise HTTPException(status_code=404, detail="Turno no encontrado")

@router.put("/turnos/{id}")
def editar_turno(id: int, turno_actualizado: Turno):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE turnos
        SET nombre = ?, fecha = ?, hora = ?, motivo = ?
        WHERE id = ?
        """,
        (
            turno_actualizado.nombre,
            str(turno_actualizado.fecha),
            str(turno_actualizado.hora),
            turno_actualizado.motivo,
            id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    conn.close()

    return {"mensaje": "Turno actualizado"}

@router.delete("/turnos/{id}")
def eliminar_turno(id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM turnos WHERE id = ?",
        (id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    conn.close()

    return {"mensaje": "Turno eliminado"}

