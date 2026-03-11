import sqlite3

DB_NAME = "agenda.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tabla():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        fecha TEXT,
        hora TEXT,
        motivo TEXT
    )
    """)

    conn.commit()
    conn.close()