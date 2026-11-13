"""
Módulo Experimental de Análisis Asistido por Inteligencia Artificial y Reglas de PLN.
Sección 6.8: Proporciona análisis automatizado local determinista sin depender de servicios de pago.
Identificado explícitamente como análisis basado en reglas y procesamiento de lenguaje natural simbólico.
"""

import os
import re
from typing import Dict, Any, List


# Léxico temático para análisis de tono institucional en educación superior
PALABRAS_POSITIVAS = {
    "inaugura", "premio", "financiamiento", "incremento", "moderno", "logro",
    "acuerdo", "convenio", "licenciada", "excelencia", "aprobado", "becas",
    "innovacion", "avance", "cooperacion", "equipamiento", "victoria"
}

PALABRAS_CRITICAS = {
    "denegada", "sancion", "observada", "irregularidad", "paro", "retraso",
    "denuncia", "conflicto", "reclamacion", "deficiencia", "vulneracion",
    "cierre", "clausura", "infraccion", "crisis", "disminucion"
}


def analizar_noticia_con_reglas(titulo: str, resumen: str, institucion: str = "") -> Dict[str, Any]:
    """
    Ejecuta un análisis automatizado local determinista basado en reglas y frecuencia léxica.
    Cumple con el requerimiento 6.8 de transparencia metodológica.
    """
    texto = f"{titulo}. {resumen}"
    palabras = re.findall(r"\b[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{4,}\b", texto.lower())

    # 1. Análisis de tono / orientación discursiva
    pos_count = sum(1 for p in palabras if p in PALABRAS_POSITIVAS)
    crit_count = sum(1 for p in palabras if p in PALABRAS_CRITICAS)

    if crit_count > pos_count:
        tono = "Crítico / Regulatorio"
        explicacion_tono = f"Contiene {crit_count} términos asociados a alertas, retrasos o sanciones."
    elif pos_count > crit_count:
        tono = "Favorable / Institucional"
        explicacion_tono = f"Contiene {pos_count} términos asociados a logros, inversión o avances."
    else:
        tono = "Informativo / Neutro"
        explicacion_tono = "Presenta lenguaje formal expositivo sin sesgo preponderante."

    # 2. Extracción de entidades y palabras clave sugeridas
    frecuencia: Dict[str, int] = {}
    stopwords = {
        "para", "como", "sobre", "este", "esta", "estos", "estas", "entre", "desde",
        "hacia", "hasta", "durante", "mediante", "donde", "quien", "cual", "cuyo",
        "pero", "sino", "porque", "aunque", "cuando", "mientras", "segun", "noticia",
        "ejemplo", "nota", "portal", "institucional", "verificar"
    }

    for p in palabras:
        if p not in stopwords and len(p) > 3:
            frecuencia[p] = frecuencia.get(p, 0) + 1

    top_terminos = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)[:5]
    tags_sugeridos = [f"#{term[0].capitalize()}" for term in top_terminos]

    # 3. Estimación del impacto institucional
    if any(k in texto.lower() for k in ["licenciamiento", "sancion", "millones", "reglamento", "denegada"]):
        impacto_estimado = "Alto"
        justificacion_impacto = "Involucra normativa obligatoria, supervisión o presupuestos de gran escala."
    elif any(k in texto.lower() for k in ["becas", "investigacion", "convenio", "acreditacion"]):
        impacto_estimado = "Medio"
        justificacion_impacto = "Afecta a la comunidad universitaria y oferta de programas."
    else:
        impacto_estimado = "Informativo"
        justificacion_impacto = "Comunicación de rutina o actividad académica regular."

    # 4. Síntesis ejecutiva estructurada
    oraciones = [s.strip() for s in re.split(r"[.!?]", texto) if len(s.strip()) > 15]
    oracion_principal = oraciones[0] if oraciones else titulo

    return {
        "motor": "Motor Simbólico Basado en Reglas Locales (Deterministic NLP)",
        "es_generativo": False,
        "advertencia_metodologica": "Análisis automatizado basado en reglas deterministas. Requiere revisión humana por el analista del OES antes de incorporarse a informes decisorios.",
        "tono_evaluado": tono,
        "explicacion_tono": explicacion_tono,
        "impacto_estimado": impacto_estimado,
        "justificacion_impacto": justificacion_impacto,
        "palabras_clave_detectadas": [t[0] for t in top_terminos],
        "tags_sugeridos": tags_sugeridos,
        "resumen_sintetizado": f"[{institucion or 'Institucional'}] {oracion_principal}."
    }


def consultar_analisis_ia(titulo: str, resumen: str, institucion: str = "") -> Dict[str, Any]:
    """
    Punto de entrada principal para el análisis.
    Si se detecta EXTERNAL_AI_API_KEY se podría conectar con un LLM, pero por defecto
    ejecuta el análisis determinista local garantizando funcionamiento offline.
    """
    api_key = os.getenv("EXTERNAL_AI_API_KEY", "").strip()
    provider = os.getenv("AI_PROVIDER", "local_rules").strip()

    if api_key and provider != "local_rules":
        # Placeholder seguro para extensión con LLM externo si el usuario la activa
        # Siempre con fallback al motor de reglas
        try:
            # Aquí iría el cliente opcional si se configuran credenciales
            pass
        except Exception:
            pass

    # Ejecución local obligatoria y determinista
    return analizar_noticia_con_reglas(titulo, resumen, institucion)

