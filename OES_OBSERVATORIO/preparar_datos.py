"""
Script de Preparación de Datos - Práctica Guiada N.° 08
Observatorio de Educación Superior (OES)

Este script realiza la creación y carga inicial de la base de datos SQLite 'oes.db',
garantizando la restricción UNIQUE en la columna 'url' para evitar duplicados (Prueba P1),
e inicializando las estructuras completas requeridas por la aplicación.
"""

import sqlite3
import shutil
from pathlib import Path

# Rutas estándar del proyecto
BASE_DIR = Path(__file__).resolve().parent
DB_ROOT = BASE_DIR / "oes.db"
DB_DATABASE_DIR = BASE_DIR / "database" / "oes.db"

# Asegurar existencia del directorio database
(BASE_DIR / "database").mkdir(parents=True, exist_ok=True)

def preparar_datos(ruta_db: Path = DB_ROOT, inicializar_normalizada: bool = True):
    """
    Crea la tabla noticias e inserta los tres registros didácticos demostrativos.
    Utiliza INSERT OR IGNORE para no duplicar URLs en ejecuciones repetidas.
    """
    with sqlite3.connect(ruta_db) as con:
        # Activar soporte de claves foráneas
        con.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Crear tabla de noticias (Compatible con Práctica 08 y extensible)
        con.execute("""CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            institucion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            fuente TEXT NOT NULL,
            fecha TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            resumen TEXT NOT NULL,
            institucion_id INTEGER,
            fuente_id INTEGER,
            estado_verificacion TEXT DEFAULT 'Pendiente',
            es_demostrativo INTEGER DEFAULT 1,
            prioridad TEXT DEFAULT 'Media',
            impacto_regulatorio TEXT DEFAULT 'Informativo',
            palabras_clave TEXT,
            fecha_captura TEXT DEFAULT (datetime('now', 'localtime'))
        )""")
        
        # 2. Registros didácticos iniciales requeridos por el laboratorio
        datos = [
            ("Ejemplo: convocatoria de becas", "PRONABEC", "Ente rector",
             "Portal institucional (ejemplo)", "2026-11-06",
             "https://www.pronabec.gob.pe/", "Registro didáctico: verificar nota original."),
            ("Ejemplo: actividad de investigación", "UNMSM", "Universidad pública",
             "Portal institucional (ejemplo)", "2026-11-06",
             "https://www.unmsm.edu.pe/", "Registro didáctico: verificar noticia original."),
            ("Ejemplo: programa académico", "PUCP", "Universidad privada",
             "Portal institucional (ejemplo)", "2026-11-05",
             "https://www.pucp.edu.pe/", "Registro didáctico: verificar noticia original.")
        ]
        
        con.executemany("""INSERT OR IGNORE INTO noticias
            (titulo, institucion, categoria, fuente, fecha, url, resumen)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", datos)
        
    print("Base creada:", ruta_db)
    
    # Si se inicializa la arquitectura completa en database/
    if inicializar_normalizada:
        try:
            from database.inicializar_db import inicializar_base_datos
            inicializar_base_datos(cargar_verificadas=True, verbose=False)
            # Sincronizar hacia database/oes.db si se creó en la raíz o viceversa
            if DB_DATABASE_DIR.exists() and not DB_ROOT.exists():
                shutil.copy2(DB_DATABASE_DIR, DB_ROOT)
            elif DB_ROOT.exists() and not DB_DATABASE_DIR.exists():
                shutil.copy2(DB_ROOT, DB_DATABASE_DIR)
        except Exception as e:
            # Mantener ejecución resiliente
            pass


if __name__ == "__main__":
    preparar_datos(DB_ROOT)
    # Asegurar copia en database/oes.db
    if DB_ROOT.exists():
        shutil.copy2(DB_ROOT, DB_DATABASE_DIR)
        print("Base sincronizada:", DB_DATABASE_DIR)

