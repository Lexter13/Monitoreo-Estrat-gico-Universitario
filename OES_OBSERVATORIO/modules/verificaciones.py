"""
Módulo de Verificación y Control de Calidad Informativa para el OES.
Implementa el flujo ético de verificación humana de noticias, estados y observaciones.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import pandas as pd
from database.conexion import obtener_conexion

ESTADOS_VALIDOS = ["Pendiente", "Verificada", "Observada"]


def registrar_verificacion(
    noticia_id: int,
    estado: str,
    responsable: str,
    observaciones: str = "",
    criterio_evaluado: str = "Trazabilidad de fuente primaria",
    evidencia_url: str = "",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """
    Registra una acción de verificación humana sobre una noticia y actualiza su estado.
    """
    if estado not in ESTADOS_VALIDOS:
        return False, f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"

    if not responsable or not responsable.strip():
        return False, "Debe especificar el nombre del responsable de la verificación."

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    try:
        with obtener_conexion() as con:
            # 1. Verificar existencia de la noticia
            cur = con.execute("SELECT id, titulo, estado_verificacion FROM noticias WHERE id = ?", (noticia_id,))
            noticia = cur.fetchone()
            if not noticia:
                return False, f"No se encontró la noticia con ID {noticia_id}."

            # 2. Insertar registro de verificación
            con.execute("""
                INSERT INTO verificaciones (
                    noticia_id, estado, responsable, fecha_verificacion,
                    observaciones, evidencia_url, criterio_evaluado
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                noticia_id,
                estado,
                responsable.strip(),
                fecha_hoy,
                observaciones.strip() or None,
                evidencia_url.strip() or None,
                criterio_evaluado.strip()
            ))

            # 3. Actualizar estado en la tabla noticias (sincronizado adicionalmente)
            con.execute("""
                UPDATE noticias
                SET estado_verificacion = ?
                WHERE id = ?
            """, (estado, noticia_id))

            # 4. Registrar en auditoría
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('verificaciones', 'VERIFICACION', ?, ?, ?)
            """, (
                noticia_id,
                f"Estado cambiado a '{estado}' por {responsable.strip()}. Criterio: {criterio_evaluado}",
                usuario
            ))

            return True, f"Noticia #{noticia_id} marcada exitosamente como '{estado}'."

    except Exception as e:
        return False, f"Error al procesar la verificación: {str(e)}"


def obtener_historial_verificaciones(noticia_id: int) -> List[Dict[str, Any]]:
    """Retorna el historial cronológico de revisiones de una noticia."""
    query = """
        SELECT id, estado, responsable, fecha_verificacion, observaciones, criterio_evaluado, fecha_registro
        FROM verificaciones
        WHERE noticia_id = ?
        ORDER BY id DESC
    """
    with obtener_conexion() as con:
        cur = con.execute(query, (noticia_id,))
        return [dict(row) for row in cur.fetchall()]


def resumen_metricas_verificacion() -> Dict[str, Any]:
    """Retorna conteos y ratios de control de calidad sobre las noticias."""
    with obtener_conexion() as con:
        total = con.execute("SELECT COUNT(*) AS c FROM noticias").fetchone()["c"]
        verificadas = con.execute("SELECT COUNT(*) AS c FROM noticias WHERE estado_verificacion = 'Verificada'").fetchone()["c"]
        pendientes = con.execute("SELECT COUNT(*) AS c FROM noticias WHERE estado_verificacion = 'Pendiente'").fetchone()["c"]
        observadas = con.execute("SELECT COUNT(*) AS c FROM noticias WHERE estado_verificacion = 'Observada'").fetchone()["c"]

        ratio_verificacion = round((verificadas / total * 100), 1) if total > 0 else 0.0

        return {
            "total": total,
            "verificadas": verificadas,
            "pendientes": pendientes,
            "observadas": observadas,
            "porcentaje_verificadas": ratio_verificacion
        }

