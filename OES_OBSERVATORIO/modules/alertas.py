"""
Módulo de Detección Temprana de Alertas Temáticas del Observatorio de Educación Superior (OES).
Monitorea palabras clave de alta sensibilidad regulatoria y política universitaria peruana.
"""

import re
from typing import Dict, List, Any, Set, Tuple
import pandas as pd

# Matriz de Palabras Clave Regulatorias Oficiales (Sección 6.7 de la Guía)
PALABRAS_CLAVE_ALERTAS = {
    "Licenciamiento": [
        "licenciamiento", "licencia institucional", "condiciones basicas de calidad",
        "cbc", "renovacion de licencia", "denegatoria", "sunedu"
    ],
    "Acreditación": [
        "acreditacion", "acreditada", "sineace", "estandares de calidad",
        "evaluacion externa", "comite de calidad", "certificacion"
    ],
    "Calidad educativa": [
        "calidad educativa", "aseguramiento de la calidad", "mejora continua",
        "evaluacion docente", "desempeno academico", "estandares"
    ],
    "Investigación": [
        "investigacion", "renacyt", "concytec", "prociencia", "i+d+i",
        "patente", "articulo cientifico", "laboratorio", "tesis", "fondo concursable"
    ],
    "Becas": [
        "beca", "becas", "beca 18", "pronabec", "beca continuidad",
        "credito educativo", "subvencion", "talento"
    ],
    "Presupuesto": [
        "presupuesto", "canon", "recursos ordinarios", "ejecucion presupuestal",
        "mef", "inversion publica", "gasto", "fondos publicos"
    ],
    "Infraestructura universitaria": [
        "infraestructura", "infraestructura universitaria", "pabellon", "campus",
        "obra", "laboratorios", "equipamiento", "modernizacion"
    ],
    "Educación superior": [
        "educacion superior", "ley universitaria", "universidades", "autonomia universitaria",
        "reforma universitaria", "asamblea universitaria"
    ]
}

NIVELES_CRITICIDAD = {
    "Licenciamiento": "CRÍTICO",
    "Presupuesto": "ALTO",
    "Calidad educativa": "ALTO",
    "Acreditación": "MEDIO",
    "Investigación": "INFORMATIVO",
    "Becas": "INFORMATIVO",
    "Infraestructura universitaria": "MEDIO",
    "Educación superior": "INFORMATIVO"
}


def _limpiar_texto(texto: str) -> str:
    """Normaliza texto removiendo acentos y pasando a minúsculas."""
    if not texto:
        return ""
    texto = texto.lower()
    reemplazos = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
        ("Á", "a"), ("É", "e"), ("Í", "i"), ("Ó", "o"), ("Ú", "u"),
        ("ñ", "n"), ("ü", "u")
    )
    for origen, destino in reemplazos:
        texto = texto.replace(origen, destino)
    return texto


def analizar_alertas_noticia(titulo: str, resumen: str, palabras_clave: str = "") -> List[Dict[str, Any]]:
    """
    Analiza una noticia individual y detecta coincidencias con las alertas normativas.
    Retorna lista de alertas encontradas con su criticidad y términos coincidentes.
    """
    texto_completo = f"{_limpiar_texto(titulo)} {_limpiar_texto(resumen)} {_limpiar_texto(palabras_clave)}"
    alertas_detectadas = []

    for categoria, terminos in PALABRAS_CLAVE_ALERTAS.items():
        coincidencias = []
        for termino in terminos:
            termino_limpio = _limpiar_texto(termino)
            # Buscar palabra completa o frase exacta
            patron = r"\b" + re.escape(termino_limpio) + r"\b"
            if re.search(patron, texto_completo):
                coincidencias.append(termino)

        if coincidencias:
            alertas_detectadas.append({
                "categoria": categoria,
                "criticidad": NIVELES_CRITICIDAD.get(categoria, "INFORMATIVO"),
                "terminos_encontrados": coincidencias,
                "coincidencias_total": len(coincidencias)
            })

    return alertas_detectadas


def generar_matriz_alertas(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Escanea todo el DataFrame de noticias y genera:
    1. Un DataFrame con cada coincidencia detallada para visualización.
    2. Un diccionario de conteo agregado por categoría de alerta.
    """
    if df.empty:
        return pd.DataFrame(), {cat: 0 for cat in PALABRAS_CLAVE_ALERTAS}

    registros_alertas = []
    conteo_global = {cat: 0 for cat in PALABRAS_CLAVE_ALERTAS}

    for _, row in df.iterrows():
        titulo = str(row.get("titulo", ""))
        resumen = str(row.get("resumen", ""))
        kw = str(row.get("palabras_clave", ""))
        noticia_id = row.get("id")
        institucion = row.get("institucion", "")
        fecha = row.get("fecha", "")

        alertas = analizar_alertas_noticia(titulo, resumen, kw)
        for al in alertas:
            cat = al["categoria"]
            conteo_global[cat] += 1
            registros_alertas.append({
                "noticia_id": noticia_id,
                "fecha": fecha,
                "institucion": institucion,
                "titulo": titulo,
                "categoria_alerta": cat,
                "criticidad": al["criticidad"],
                "terminos": ", ".join(al["terminos_encontrados"]),
                "url": row.get("url", "")
            })

    df_alertas = pd.DataFrame(registros_alertas)
    return df_alertas, conteo_global

