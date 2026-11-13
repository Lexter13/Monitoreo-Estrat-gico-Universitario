"""
Script de Inicialización de la Base de Datos del Observatorio de Educación Superior (OES).
Crea el esquema relacional normalizado, inserta el catálogo maestro y los registros demostrativos.
"""

import sqlite3
import sys
from pathlib import Path

# Agregar directorio raíz al PYTHONPATH si es necesario
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.conexion import obtener_conexion, obtener_ruta_db
from data.datos_demostrativos import (
    INSTITUCIONES_BASE,
    FUENTES_BASE,
    NOTICIAS_DEMOSTRATIVAS,
    NOTICIAS_REALES_VERIFICADAS
)


def inicializar_base_datos(cargar_verificadas: bool = True, verbose: bool = True) -> Path:
    """
    Inicializa el esquema de SQLite y carga los datos maestros y demostrativos.
    Retorna la ruta hacia la base de datos inicializada.
    """
    ruta_db = obtener_ruta_db()
    ruta_schema = BASE_DIR / "database" / "schema.sql"

    if verbose:
        print(f"[OES DB] Inicializando base de datos en: {ruta_db}")

    # 1. Ejecutar esquema DDL
    with obtener_conexion() as con:
        with open(ruta_schema, "r", encoding="utf-8") as f:
            con.executescript(f.read())

    # 2. Cargar Instituciones Maestras
    with obtener_conexion() as con:
        for inst in INSTITUCIONES_BASE:
            con.execute("""
                INSERT OR IGNORE INTO instituciones (nombre, tipo, siglas, region, estado_licenciamiento, sitio_web)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                inst["nombre"],
                inst["tipo"],
                inst.get("siglas"),
                inst.get("region", "Lima"),
                inst.get("estado_licenciamiento", "Licenciada"),
                inst.get("sitio_web")
            ))

    # 3. Cargar Fuentes Oficiales Maestras
    with obtener_conexion() as con:
        for fte in FUENTES_BASE:
            con.execute("""
                INSERT OR IGNORE INTO fuentes (nombre, tipo_fuente, url_base, confiabilidad)
                VALUES (?, ?, ?, ?)
            """, (
                fte["nombre"],
                fte["tipo_fuente"],
                fte["url_base"],
                fte.get("confiabilidad", "Alta")
            ))

    # 4. Cargar los 3 Registros Demostrativos Obligatorios de la Práctica 08
    with obtener_conexion() as con:
        for noti in NOTICIAS_DEMOSTRATIVAS:
            # Obtener IDs foráneos correspondientes
            cur_inst = con.execute("SELECT id FROM instituciones WHERE nombre = ?", (noti["institucion"],))
            row_inst = cur_inst.fetchone()
            inst_id = row_inst["id"] if row_inst else None

            cur_fuente = con.execute("SELECT id FROM fuentes WHERE nombre = ?", (noti["fuente"],))
            row_fuente = cur_fuente.fetchone()
            fuente_id = row_fuente["id"] if row_fuente else None

            con.execute("""
                INSERT OR IGNORE INTO noticias (
                    titulo, institucion, categoria, fuente, fecha, url, resumen,
                    institucion_id, fuente_id, estado_verificacion, es_demostrativo,
                    prioridad, impacto_regulatorio, palabras_clave
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                noti["titulo"],
                noti["institucion"],
                noti["categoria"],
                noti["fuente"],
                noti["fecha"],
                noti["url"],
                noti["resumen"],
                inst_id,
                fuente_id,
                noti.get("estado_verificacion", "Pendiente"),
                noti.get("es_demostrativo", 1),
                noti.get("prioridad", "Media"),
                noti.get("impacto_regulatorio", "Informativo"),
                noti.get("palabras_clave", "")
            ))

    # 5. Opcional: Cargar registros reales verificados con trazabilidad
    if cargar_verificadas:
        with obtener_conexion() as con:
            for noti in NOTICIAS_REALES_VERIFICADAS:
                cur_inst = con.execute("SELECT id FROM instituciones WHERE nombre = ?", (noti["institucion"],))
                row_inst = cur_inst.fetchone()
                inst_id = row_inst["id"] if row_inst else None

                cur_fuente = con.execute("SELECT id FROM fuentes WHERE nombre = ?", (noti["fuente"],))
                row_fuente = cur_fuente.fetchone()
                fuente_id = row_fuente["id"] if row_fuente else None

                cursor = con.execute("""
                    INSERT OR IGNORE INTO noticias (
                        titulo, institucion, categoria, fuente, fecha, url, resumen,
                        institucion_id, fuente_id, estado_verificacion, es_demostrativo,
                        prioridad, impacto_regulatorio, palabras_clave
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    noti["titulo"],
                    noti["institucion"],
                    noti["categoria"],
                    noti["fuente"],
                    noti["fecha"],
                    noti["url"],
                    noti["resumen"],
                    inst_id,
                    fuente_id,
                    noti.get("estado_verificacion", "Pendiente"),
                    noti.get("es_demostrativo", 0),
                    noti.get("prioridad", "Media"),
                    noti.get("impacto_regulatorio", "Informativo"),
                    noti.get("palabras_clave", "")
                ))

                # Si tiene verificación asociada
                if "verificacion" in noti:
                    # Buscar el id de la noticia insertada o existente
                    cur_not_id = con.execute("SELECT id FROM noticias WHERE url = ?", (noti["url"],))
                    row_not_id = cur_not_id.fetchone()
                    if row_not_id:
                        ver = noti["verificacion"]
                        con.execute("""
                            INSERT OR IGNORE INTO verificaciones (
                                noticia_id, estado, responsable, fecha_verificacion, observaciones, criterio_evaluado
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            row_not_id["id"],
                            noti["estado_verificacion"],
                            ver["responsable"],
                            ver["fecha"],
                            ver["observaciones"],
                            ver.get("criterio", "Auditoría OES")
                        ))

    # Registrar evento en auditoría
    with obtener_conexion() as con:
        con.execute("""
            INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
            VALUES ('sistema', 'INSERT', 0, 'Base de datos inicializada satisfactoriamente con esquema normalizado', 'sistema_init')
        """)

    if verbose:
        with obtener_conexion() as con:
            total_noticias = con.execute("SELECT COUNT(*) AS c FROM noticias").fetchone()["c"]
            total_inst = con.execute("SELECT COUNT(*) AS c FROM instituciones").fetchone()["c"]
            total_fuentes = con.execute("SELECT COUNT(*) AS c FROM fuentes").fetchone()["c"]
            print(f"[OES DB] Inicialización completada exitosamente:")
            print(f"         - Noticias registradas: {total_noticias}")
            print(f"         - Instituciones en catálogo: {total_inst}")
            print(f"         - Fuentes monitoreadas: {total_fuentes}")

    return ruta_db


if __name__ == "__main__":
    inicializar_base_datos(cargar_verificadas=True, verbose=True)

