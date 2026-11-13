"""
Módulo de Conexión a la Base de Datos SQLite para OES.
Garantiza el uso de claves foráneas, paths absolutos consistentes y transacciones seguras.
"""

import sqlite3
import os
from pathlib import Path

# Resolver la ruta hacia database/oes.db respecto a este archivo
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "oes.db"

# También permitir variable de entorno OES_DB_PATH
ENV_DB = os.getenv("OES_DB_PATH")
if ENV_DB:
    CUSTOM_PATH = Path(ENV_DB)
    if CUSTOM_PATH.is_absolute():
        DB_PATH = CUSTOM_PATH
    else:
        DB_PATH = BASE_DIR / CUSTOM_PATH


def obtener_ruta_db() -> Path:
    """Retorna la ruta absoluta hacia el archivo SQLite oes.db."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return DB_PATH


def obtener_conexion() -> sqlite3.Connection:
    """
    Retorna una conexión activa a SQLite con:
    - PRAGMA foreign_keys = ON
    - row_factory = sqlite3.Row para acceso asociativo por nombre de columna
    - timeout configurable para evitar bloqueos
    """
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta, timeout=15.0)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


def ejecutar_script_sql(ruta_script: Path) -> None:
    """Ejecuta un script SQL completo dentro de una transacción segura."""
    with obtener_conexion() as con:
        with open(ruta_script, "r", encoding="utf-8") as f:
            con.executescript(f.read())

