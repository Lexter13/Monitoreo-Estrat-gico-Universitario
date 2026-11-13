"""
Pruebas Automatizadas de Base de Datos — OES
Verifica la inicialización del esquema, integridad referencial (claves foráneas) y disparadores de auditoría.
"""

import sqlite3
import pytest
from pathlib import Path
from database.conexion import obtener_conexion, obtener_ruta_db
from database.inicializar_db import inicializar_base_datos


@pytest.fixture(scope="module")
def setup_db():
    """Inicializa la base de datos para la suite de pruebas."""
    ruta = inicializar_base_datos(cargar_verificadas=True, verbose=False)
    assert ruta.exists()
    yield ruta


def test_claves_foraneas_activadas(setup_db):
    """Comprueba que SQLite aplique restricciones de claves foráneas (PRAGMA foreign_keys = ON)."""
    with obtener_conexion() as con:
        cur = con.execute("PRAGMA foreign_keys;")
        row = cur.fetchone()
        assert row[0] == 1, "Las claves foráneas deben estar habilitadas en SQLite."


def test_tablas_principales_creadas(setup_db):
    """Verifica la existencia física de las 5 tablas obligatorias del sistema."""
    tablas_esperadas = {"instituciones", "fuentes", "noticias", "verificaciones", "auditoria"}
    with obtener_conexion() as con:
        cur = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_existentes = {row["name"] for row in cur.fetchall()}

    for t in tablas_esperadas:
        assert t in tablas_existentes, f"La tabla obligatoria '{t}' debe existir en la base de datos."


def test_disparador_auditoria_automatico(setup_db):
    """Comprueba que un INSERT en noticias dispare automáticamente un registro en auditoria."""
    with obtener_conexion() as con:
        # Registrar una noticia de prueba
        cur = con.execute("""
            INSERT INTO noticias (titulo, institucion, categoria, fuente, fecha, url, resumen)
            VALUES ('Test Trigger Noticia', 'UNMSM', 'Universidad pública', 'Portal Test', '2026-11-12', 'https://test-trigger.edu.pe', 'Resumen test')
        """)
        noticia_id = cur.lastrowid

        # Comprobar si el trigger insertó en la tabla de auditoría
        cur_aud = con.execute("SELECT * FROM auditoria WHERE registro_id = ? AND tabla = 'noticias'", (noticia_id,))
        row_aud = cur_aud.fetchone()
        assert row_aud is not None, "El trigger de inserción debió registrar un evento en auditoria."
        assert "Test Trigger Noticia" in row_aud["detalles"]

        # Limpiar registro de prueba
        con.execute("DELETE FROM noticias WHERE id = ?", (noticia_id,))

