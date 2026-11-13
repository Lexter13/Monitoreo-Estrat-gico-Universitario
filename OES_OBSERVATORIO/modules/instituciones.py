"""
Módulo de Gestión de Instituciones del Observatorio de Educación Superior (OES).
Mantiene el directorio oficial de universidades, entes rectores e institutos superiores.
"""

from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from database.conexion import obtener_conexion


def listar_instituciones() -> pd.DataFrame:
    """Retorna un DataFrame con todas las instituciones registradas y su conteo de noticias."""
    query = """
        SELECT 
            i.id,
            i.nombre,
            i.tipo,
            i.siglas,
            i.region,
            i.estado_licenciamiento,
            i.sitio_web,
            i.fecha_registro,
            COUNT(n.id) AS total_noticias
        FROM instituciones i
        LEFT JOIN noticias n ON n.institucion_id = i.id OR n.institucion = i.nombre
        GROUP BY i.id
        ORDER BY i.nombre ASC
    """
    with obtener_conexion() as con:
        return pd.read_sql_query(query, con)


def registrar_institucion(
    nombre: str,
    tipo: str,
    siglas: str = "",
    region: str = "Lima",
    estado_licenciamiento: str = "Licenciada",
    sitio_web: str = "",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """Registra una nueva institución con validación de nombre único."""
    if not nombre or not nombre.strip():
        return False, "El nombre de la institución es obligatorio."
    if not tipo or not tipo.strip():
        return False, "El tipo de institución es obligatorio."

    nombre_c = nombre.strip()
    try:
        with obtener_conexion() as con:
            cur = con.execute("SELECT id FROM instituciones WHERE nombre = ?", (nombre_c,))
            if cur.fetchone():
                return False, f"La institución '{nombre_c}' ya se encuentra registrada."

            cursor = con.execute("""
                INSERT INTO instituciones (nombre, tipo, siglas, region, estado_licenciamiento, sitio_web)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nombre_c, tipo.strip(), siglas.strip() or None, region.strip() or "Lima",
                estado_licenciamiento.strip() or "Licenciada", sitio_web.strip() or None
            ))
            new_id = cursor.lastrowid

            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('instituciones', 'INSERT', ?, ?, ?)
            """, (new_id, f"Institución '{nombre_c}' registrada por {usuario}", usuario))

            return True, f"Institución '{nombre_c}' registrada exitosamente."
    except Exception as e:
        return False, f"Error al registrar la institución: {str(e)}"


def actualizar_institucion(
    institucion_id: int,
    nombre: str,
    tipo: str,
    siglas: str = "",
    region: str = "Lima",
    estado_licenciamiento: str = "Licenciada",
    sitio_web: str = "",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """Actualiza los datos de una institución existente."""
    if not nombre or not nombre.strip():
        return False, "El nombre de la institución es obligatorio."

    try:
        with obtener_conexion() as con:
            con.execute("""
                UPDATE instituciones
                SET nombre = ?, tipo = ?, siglas = ?, region = ?,
                    estado_licenciamiento = ?, sitio_web = ?
                WHERE id = ?
            """, (
                nombre.strip(), tipo.strip(), siglas.strip() or None, region.strip(),
                estado_licenciamiento.strip(), sitio_web.strip() or None, institucion_id
            ))

            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('instituciones', 'UPDATE', ?, ?, ?)
            """, (institucion_id, f"Institución #{institucion_id} actualizada por {usuario}", usuario))

            return True, "Institución actualizada correctamente."
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"


def eliminar_institucion(institucion_id: int, usuario: str = "admin") -> Tuple[bool, str]:
    """Elimina una institución del catálogo."""
    try:
        with obtener_conexion() as con:
            cur = con.execute("SELECT nombre FROM instituciones WHERE id = ?", (institucion_id,))
            row = cur.fetchone()
            if not row:
                return False, "La institución no existe."

            con.execute("DELETE FROM instituciones WHERE id = ?", (institucion_id,))
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('instituciones', 'DELETE', ?, ?, ?)
            """, (institucion_id, f"Institución #{institucion_id} ('{row['nombre']}') eliminada por {usuario}", usuario))

            return True, "Institución eliminada del catálogo."
    except Exception as e:
        return False, f"Error al eliminar institución: {str(e)}"

