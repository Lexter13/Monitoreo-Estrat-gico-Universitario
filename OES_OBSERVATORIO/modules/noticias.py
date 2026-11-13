"""
Módulo de Gestión de Noticias del Observatorio de Educación Superior (OES).
Implementa CRUD, validaciones estrictas, prevención de duplicados, filtros avanzados y exportación.
"""

import re
import sqlite3
from typing import Tuple, List, Optional, Dict, Any
import pandas as pd
from database.conexion import obtener_conexion


def validar_url(url: str) -> bool:
    """Valida formato básico de URL http/https."""
    if not url or not isinstance(url, str):
        return False
    patron = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    return bool(patron.match(url.strip()))


def registrar_noticia(
    titulo: str,
    institucion: str,
    categoria: str,
    fuente: str,
    fecha: str,
    url: str,
    resumen: str,
    prioridad: str = "Media",
    impacto_regulatorio: str = "Informativo",
    palabras_clave: str = "",
    es_demostrativo: int = 0,
    usuario: str = "admin"
) -> Tuple[bool, str, Optional[int]]:
    """
    Registra una nueva noticia validando campos obligatorios y duplicados por URL.
    Retorna (éxito, mensaje, nuevo_id).
    """
    # 1. Validación de obligatoriedad
    campos_obligatorios = {
        "Título": titulo,
        "Institución": institucion,
        "Categoría": categoria,
        "Fuente": fuente,
        "Fecha": fecha,
        "URL": url,
        "Resumen": resumen
    }
    for campo, valor in campos_obligatorios.items():
        if not valor or not str(valor).strip():
            return False, f"El campo '{campo}' es obligatorio y no puede estar vacío.", None

    titulo_clean = titulo.strip()
    url_clean = url.strip()
    institucion_clean = institucion.strip()
    categoria_clean = categoria.strip()
    fuente_clean = fuente.strip()
    fecha_clean = fecha.strip()
    resumen_clean = resumen.strip()

    # 2. Validación de URL
    if not validar_url(url_clean):
        return False, "La URL ingresada no tiene un formato válido (debe iniciar con http:// o https://).", None

    try:
        with obtener_conexion() as con:
            # 3. Comprobar duplicado por URL
            cur = con.execute("SELECT id FROM noticias WHERE url = ?", (url_clean,))
            if cur.fetchone():
                return False, f"Ya existe una noticia registrada con la URL especificada: {url_clean}", None

            # 4. Vincular o registrar institución automáticamente si no existe
            cur_inst = con.execute("SELECT id FROM instituciones WHERE nombre = ?", (institucion_clean,))
            row_inst = cur_inst.fetchone()
            if row_inst:
                inst_id = row_inst["id"]
            else:
                c_new = con.execute(
                    "INSERT INTO instituciones (nombre, tipo) VALUES (?, ?)",
                    (institucion_clean, categoria_clean if categoria_clean in ['Universidad pública', 'Universidad privada', 'Ente rector'] else 'Universidad pública')
                )
                inst_id = c_new.lastrowid

            # 5. Vincular o registrar fuente automáticamente si no existe
            cur_fuente = con.execute("SELECT id FROM fuentes WHERE nombre = ?", (fuente_clean,))
            row_fuente = cur_fuente.fetchone()
            if row_fuente:
                fuente_id = row_fuente["id"]
            else:
                c_new_f = con.execute(
                    "INSERT INTO fuentes (nombre, tipo_fuente, url_base) VALUES (?, ?, ?)",
                    (fuente_clean, "Portal institucional", url_clean)
                )
                fuente_id = c_new_f.lastrowid

            # 6. Inserción parametrizada segura
            cursor = con.execute("""
                INSERT INTO noticias (
                    titulo, institucion, categoria, fuente, fecha, url, resumen,
                    institucion_id, fuente_id, estado_verificacion, es_demostrativo,
                    prioridad, impacto_regulatorio, palabras_clave
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                titulo_clean,
                institucion_clean,
                categoria_clean,
                fuente_clean,
                fecha_clean,
                url_clean,
                resumen_clean,
                inst_id,
                fuente_id,
                "Pendiente",
                es_demostrativo,
                prioridad,
                impacto_regulatorio,
                palabras_clave.strip()
            ))
            nuevo_id = cursor.lastrowid

            # Registrar en auditoría
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('noticias', 'INSERT', ?, ?, ?)
            """, (nuevo_id, f"Noticia creada: '{titulo_clean[:60]}' por {usuario}", usuario))

            return True, "Noticia registrada exitosamente en el observatorio.", nuevo_id

    except sqlite3.IntegrityError as ie:
        return False, f"Error de integridad en base de datos: {str(ie)}", None
    except Exception as e:
        return False, f"Ocurrió un error inesperado al registrar la noticia: {str(e)}", None


def obtener_noticias(
    categorias: Optional[List[str]] = None,
    instituciones: Optional[List[str]] = None,
    fuentes: Optional[List[str]] = None,
    estados_verificacion: Optional[List[str]] = None,
    busqueda_texto: str = "",
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    solo_demostrativas: Optional[bool] = None,
    orden_columna: str = "fecha",
    orden_direccion: str = "DESC"
) -> pd.DataFrame:
    """
    Consulta noticias aplicando filtros combinados, búsqueda textual y ordenamiento.
    Retorna un DataFrame de Pandas listo para visualización y análisis.
    """
    query = """
        SELECT 
            n.id,
            n.fecha,
            n.institucion,
            n.categoria,
            n.titulo,
            n.fuente,
            n.url,
            n.resumen,
            n.estado_verificacion,
            n.prioridad,
            n.impacto_regulatorio,
            n.palabras_clave,
            n.es_demostrativo,
            n.institucion_id,
            n.fuente_id,
            n.fecha_captura
        FROM noticias n
        WHERE 1=1
    """
    params = []

    if categorias:
        placeholders = ",".join(["?"] * len(categorias))
        query += f" AND n.categoria IN ({placeholders})"
        params.extend(categorias)

    if instituciones:
        placeholders = ",".join(["?"] * len(instituciones))
        query += f" AND n.institucion IN ({placeholders})"
        params.extend(instituciones)

    if fuentes:
        placeholders = ",".join(["?"] * len(fuentes))
        query += f" AND n.fuente IN ({placeholders})"
        params.extend(fuentes)

    if estados_verificacion:
        placeholders = ",".join(["?"] * len(estados_verificacion))
        query += f" AND n.estado_verificacion IN ({placeholders})"
        params.extend(estados_verificacion)

    if fecha_inicio:
        query += " AND n.fecha >= ?"
        params.append(fecha_inicio)

    if fecha_fin:
        query += " AND n.fecha <= ?"
        params.append(fecha_fin)

    if solo_demostrativas is not None:
        query += " AND n.es_demostrativo = ?"
        params.append(1 if solo_demostrativas else 0)

    if busqueda_texto and busqueda_texto.strip():
        patron = f"%{busqueda_texto.strip()}%"
        query += """ AND (
            n.titulo LIKE ? OR
            n.institucion LIKE ? OR
            n.resumen LIKE ? OR
            n.fuente LIKE ? OR
            n.palabras_clave LIKE ?
        )"""
        params.extend([patron, patron, patron, patron, patron])

    # Ordenamiento seguro
    columnas_validas = {
        "fecha": "n.fecha",
        "id": "n.id",
        "titulo": "n.titulo",
        "institucion": "n.institucion",
        "categoria": "n.categoria",
        "estado": "n.estado_verificacion"
    }
    col_orden = columnas_validas.get(orden_columna.lower(), "n.fecha")
    dir_orden = "ASC" if orden_direccion.upper() == "ASC" else "DESC"
    query += f" ORDER BY {col_orden} {dir_orden}, n.id DESC"

    with obtener_conexion() as con:
        df = pd.read_sql_query(query, con, params=params)

    return df


def obtener_noticia_por_id(noticia_id: int) -> Optional[Dict[str, Any]]:
    """Retorna los datos de una noticia específica o None."""
    with obtener_conexion() as con:
        cur = con.execute("SELECT * FROM noticias WHERE id = ?", (noticia_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def actualizar_noticia(
    noticia_id: int,
    titulo: str,
    institucion: str,
    categoria: str,
    fuente: str,
    fecha: str,
    url: str,
    resumen: str,
    prioridad: str = "Media",
    impacto_regulatorio: str = "Informativo",
    palabras_clave: str = "",
    usuario: str = "admin"
) -> Tuple[bool, str]:
    """Actualiza los datos de una noticia existente con validación."""
    if not noticia_id:
        return False, "Identificador de noticia inválido."

    if not validar_url(url.strip()):
        return False, "La URL ingresada no es válida."

    try:
        with obtener_conexion() as con:
            # Comprobar si existe otra noticia con esa misma URL
            cur = con.execute("SELECT id FROM noticias WHERE url = ? AND id != ?", (url.strip(), noticia_id))
            if cur.fetchone():
                return False, f"La URL '{url}' ya pertenece a otra noticia registrada."

            con.execute("""
                UPDATE noticias
                SET titulo = ?, institucion = ?, categoria = ?, fuente = ?, fecha = ?,
                    url = ?, resumen = ?, prioridad = ?, impacto_regulatorio = ?, palabras_clave = ?
                WHERE id = ?
            """, (
                titulo.strip(), institucion.strip(), categoria.strip(), fuente.strip(), fecha.strip(),
                url.strip(), resumen.strip(), prioridad, impacto_regulatorio, palabras_clave.strip(),
                noticia_id
            ))

            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('noticias', 'UPDATE', ?, ?, ?)
            """, (noticia_id, f"Noticia #{noticia_id} actualizada por {usuario}", usuario))

            return True, "Noticia actualizada con éxito."
    except Exception as e:
        return False, f"Error al actualizar la noticia: {str(e)}"


def eliminar_noticia(noticia_id: int, usuario: str = "admin") -> Tuple[bool, str]:
    """Elimina una noticia y sus verificaciones dependientes."""
    try:
        with obtener_conexion() as con:
            cur = con.execute("SELECT titulo FROM noticias WHERE id = ?", (noticia_id,))
            row = cur.fetchone()
            if not row:
                return False, "La noticia no existe o ya fue eliminada."

            titulo = row["titulo"]
            con.execute("DELETE FROM noticias WHERE id = ?", (noticia_id,))
            con.execute("""
                INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
                VALUES ('noticias', 'DELETE', ?, ?, ?)
            """, (noticia_id, f"Noticia #{noticia_id} ('{titulo[:50]}') eliminada por {usuario}", usuario))

            return True, "Noticia eliminada correctamente."
    except Exception as e:
        return False, f"Error al eliminar la noticia: {str(e)}"


def exportar_noticias_csv(df: pd.DataFrame) -> bytes:
    """
    Genera un archivo CSV codificado con UTF-8 y BOM (utf-8-sig)
    para apertura impecable en Microsoft Excel sin caracteres corruptos.
    """
    columnas_exportacion = [
        col for col in [
            "id", "fecha", "institucion", "categoria", "titulo", "fuente",
            "url", "resumen", "estado_verificacion", "prioridad", "impacto_regulatorio"
        ] if col in df.columns
    ]
    sub_df = df[columnas_exportacion] if columnas_exportacion else df
    return sub_df.to_csv(index=False).encode("utf-8-sig")

