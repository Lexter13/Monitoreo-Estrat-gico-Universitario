"""
Módulo de Gestión de Fuentes de Información del Observatorio de Educación Superior (OES).
Permite auditar la confiabilidad y procedencia de la vigilancia institucional.
"""

from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from database.conexion import obtener_conexion


def listar_fuentes() -> pd.DataFrame:
    """Retorna un DataFrame con todas las fuentes monitoreadas y el conteo de noticias emitidas."""
    query = """
        SELECT 
            f.id,
            f.nombre,
            f.tipo_fuente,
            f.url_base,
            f.confiabilidad,
            f.fecha_registro,
            COUNT(n.id) AS total_noticias
        FROM fuentes f
        LEFT JOIN noticias n ON n.fuente_id = f.id OR n.fuente = f.nombre
        GROUP BY f.id
        ORDER BY f.confiabilidad DESC, f.nombre ASC
    """
    with obtener_conexion() as con:
        return pd.read_sql_query(query, con)


def registrar_fuente(
    nombre: str,
    tipo_fuente: str,
    url_base: str,
    confiabilidad: str = "Alta",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """Registra una fuente institucional verificable."""
    if not nombre or not nombre.strip():
        return False, "El nombre de la fuente es obligatorio."
    if not url_base or not url_base.strip():
        return False, "La URL base de la fuente es obligatoria."

    nombre_c = nombre.strip()
    url_c = url_base.strip()

    try:
        with obtener_conexion() as con:
            cur = con.execute("SELECT id FROM fuentes WHERE nombre = ?", (nombre_c,))
            if cur.fetchone():
                return False, f"La fuente '{nombre_c}' ya existe en el registro."

            cursor = con.execute("""
                INSERT INTO fuentes (nombre, tipo_fuente, url_base, confiabilidad)
                VALUES (?, ?, ?, ?)
            """, (nombre_c, tipo_fuente.strip(), url_c, confiabilidad.strip()))
            new_id = cursor.lastrowid

            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('fuentes', 'INSERT', ?, ?, ?)
            """, (new_id, f"Fuente '{nombre_c}' registrada por {usuario}", usuario))

            return True, f"Fuente '{nombre_c}' registrada con éxito."
    except Exception as e:
        return False, f"Error al registrar la fuente: {str(e)}"


def actualizar_fuente(
    fuente_id: int,
    nombre: str,
    tipo_fuente: str,
    url_base: str,
    confiabilidad: str = "Alta",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """Actualiza los parámetros de una fuente existente."""
    try:
        with obtener_conexion() as con:
            con.execute("""
                UPDATE fuentes
                SET nombre = ?, tipo_fuente = ?, url_base = ?, confiabilidad = ?
                WHERE id = ?
            """, (nombre.strip(), tipo_fuente.strip(), url_base.strip(), confiabilidad.strip(), fuente_id))

            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('fuentes', 'UPDATE', ?, ?, ?)
            """, (fuente_id, f"Fuente #{fuente_id} actualizada por {usuario}", usuario))

            return True, "Fuente actualizada exitosamente."
    except Exception as e:
        return False, f"Error al actualizar la fuente: {str(e)}"


def eliminar_fuente(fuente_id: int, usuario: str = "admin") -> Tuple[bool, str]:
    """Elimina una fuente del observatorio."""
    try:
        with obtener_conexion() as con:
            cur = con.execute("SELECT nombre FROM fuentes WHERE id = ?", (fuente_id,))
            row = cur.fetchone()
            if not row:
                return False, "La fuente no existe."

            con.execute("DELETE FROM fuentes WHERE id = ?", (fuente_id,))
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('fuentes', 'DELETE', ?, ?, ?)
            """, (fuente_id, f"Fuente #{fuente_id} ('{row['nombre']}') eliminada por {usuario}", usuario))

            return True, "Fuente eliminada del registro."
    except Exception as e:
        return False, f"Error al eliminar la fuente: {str(e)}"

