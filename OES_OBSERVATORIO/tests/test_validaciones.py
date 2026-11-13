"""
Pruebas de Validaciones de Integridad, Formato de URL y Seguridad — OES.
Garantiza el rechazo de entradas erróneas, datos faltantes y estados no permitidos.
"""

import pytest
from database.inicializar_db import inicializar_base_datos
from modules.noticias import registrar_noticia, validar_url
from modules.verificaciones import registrar_verificacion
from modules.alertas import analizar_alertas_noticia


@pytest.fixture(autouse=True)
def init_db():
    inicializar_base_datos(cargar_verificadas=True, verbose=False)


def test_validacion_campos_obligatorios():
    """Valida que no se permita registrar noticias con campos obligatorios vacíos."""
    # Título vacío
    ok, msg, nid = registrar_noticia(
        titulo="",
        institucion="UNMSM",
        categoria="Universidad pública",
        fuente="Portal",
        fecha="2026-11-12",
        url="https://valid-url.edu.pe",
        resumen="Resumen"
    )
    assert ok is False
    assert "obligatorio" in msg.lower()

    # URL vacía
    ok, msg, nid = registrar_noticia(
        titulo="Título válido",
        institucion="UNMSM",
        categoria="Universidad pública",
        fuente="Portal",
        fecha="2026-11-12",
        url="",
        resumen="Resumen"
    )
    assert ok is False


def test_validacion_formato_url():
    """Comprueba el validador regex de URLs http/https."""
    assert validar_url("https://www.sunedu.gob.pe/norma") is True
    assert validar_url("http://unmsm.edu.pe/noticia?id=123") is True
    assert validar_url("ftp://servidor.com/archivo") is False
    assert validar_url("htp:/invalido") is False
    assert validar_url("texto plano no url") is False
    assert validar_url("") is False


def test_rechazo_url_duplicada():
    """Verifica que el sistema rechace explícitamente el intento de ingresar una URL duplicada."""
    url_existente = "https://www.pronabec.gob.pe/"
    ok, msg, nid = registrar_noticia(
        titulo="Intento de noticia duplicada",
        institucion="PRONABEC",
        categoria="Ente rector",
        fuente="Portal",
        fecha="2026-11-12",
        url=url_existente,
        resumen="Debe ser rechazado por URL ya existente."
    )
    assert ok is False
    assert "ya existe" in msg.lower() or "duplic" in msg.lower()


def test_validacion_estado_verificacion_invalido():
    """Verifica que se rechacen estados de verificación fuera de la lista permitida."""
    ok, msg = registrar_verificacion(
        noticia_id=1,
        estado="ESTADO_INVENTADO_NO_VALIDO",
        responsable="Auditor Test"
    )
    assert ok is False
    assert "inválido" in msg.lower() or "invalido" in msg.lower()


def test_deteccion_alertas_normativas():
    """Comprueba que el detector de alertas reconozca palabras clave críticas en títulos o resúmenes."""
    alertas = analizar_alertas_noticia(
        titulo="SUNEDU anuncia nuevo proceso de licenciamiento institucional y condiciones basicas de calidad",
        resumen="Se evaluará la investigación universitaria y laboratorios."
    )
    categorias_detectadas = [a["categoria"] for a in alertas]
    assert "Licenciamiento" in categorias_detectadas
    assert "Investigación" in categorias_detectadas

