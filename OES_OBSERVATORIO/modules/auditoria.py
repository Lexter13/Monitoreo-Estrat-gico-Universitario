"""
Módulo de Auditoría y Trazabilidad del Sistema OES.
Registra y permite auditar cada operación crítica (creación, edición, verificación, eliminación).
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd
from database.conexion import obtener_conexion


def registrar_auditoria(
    tabla: str,
    operacion: str,
    registro_id: Optional[int],
    detalles: str,
    usuario: str = "admin",
    ip_origen: str = "127.0.0.1"
) -> bool:
    """Registra manualmente un evento en la bitácora de auditoría inmutable."""
    try:
        with obtener_conexion() as con:
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario, ip_origen)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tabla, operacion, registro_id, detalles, usuario, ip_origen))
            return True
    except Exception as e:
        print(f"[ERROR AUDITORIA] {e}")
        return False


def consultar_auditoria(
    tabla: Optional[str] = None,
    operacion: Optional[str] = None,
    usuario: Optional[str] = None,
    limite: int = 150
) -> pd.DataFrame:
    """Consulta los registros de auditoría aplicando filtros opcionales."""
    query = """
        SELECT id, fecha_hora, tabla, operacion, registro_id, detalles, usuario, ip_origen
        FROM auditoria
        WHERE 1=1
    """
    params = []

    if tabla and tabla != "Todas":
        query += " AND tabla = ?"
        params.append(tabla)

    if operacion and operacion != "Todas":
        query += " AND operacion = ?"
        params.append(operacion)

    if usuario and usuario.strip():
        query += " AND usuario LIKE ?"
        params.append(f"%{usuario.strip()}%")

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limite)

    with obtener_conexion() as con:
        return pd.read_sql_query(query, con, params=params)


def obtener_estadisticas_auditoria() -> Dict[str, Any]:
    """Genera resumen cuantitativo de operaciones en el observatorio."""
    with obtener_conexion() as con:
        total_ops = con.execute("SELECT COUNT(*) AS c FROM auditoria").fetchone()["c"]
        por_operacion = dict(con.execute("SELECT operacion, COUNT(*) FROM auditoria GROUP BY operacion").fetchall())
        usuarios_activos = con.execute("SELECT COUNT(DISTINCT usuario) AS c FROM auditoria").fetchone()["c"]

        return {
            "total_operaciones": total_ops,
            "operaciones_por_tipo": por_operacion,
            "usuarios_activos": usuarios_activos
        }

