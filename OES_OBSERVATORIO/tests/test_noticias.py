"""
Pruebas de Noticias y Cumplimiento de Pruebas Obligatorias del Documento:
- P1: Ejecutar la carga de datos dos veces y comprobar que no se dupliquen las tres URL.
- P6: Registrar una noticia real verificada y comprobar que aumenta el contador y se conserva su URL directa.
"""

import pytest
from database.conexion import obtener_conexion
from database.inicializar_db import inicializar_base_datos
from modules.noticias import registrar_noticia, obtener_noticias, eliminar_noticia


@pytest.fixture(autouse=True)
def init_db():
    inicializar_base_datos(cargar_verificadas=True, verbose=False)


def test_prueba_p1_evitar_duplicados_en_doble_carga():
    """
    PRUEBA P1 DEL DOCUMENTO:
    Ejecutar la carga de datos dos veces y comprobar que no se dupliquen las tres URL.
    """
    # 1. Primera carga ejecutada por el fixture
    urls_esperadas = [
        "https://www.pronabec.gob.pe/",
        "https://www.unmsm.edu.pe/",
        "https://www.pucp.edu.pe/"
    ]

    # 2. Ejecutar la inicialización por segunda vez
    inicializar_base_datos(cargar_verificadas=True, verbose=False)

    # 3. Comprobar que cada URL exista exactamente una vez en la base de datos
    with obtener_conexion() as con:
        for url in urls_esperadas:
            cur = con.execute("SELECT COUNT(*) AS c FROM noticias WHERE url = ?", (url,))
            conteo = cur.fetchone()["c"]
            assert conteo == 1, f"La URL {url} debe existir exactamente una sola vez, pero se encontró {conteo} veces."


def test_prueba_p6_registro_noticia_real_verificada():
    """
    PRUEBA P6 DEL DOCUMENTO:
    Registrar una noticia real verificada y comprobar que aumenta el contador y se conserva su URL directa.
    """
    df_inicial = obtener_noticias()
    conteo_inicial = len(df_inicial)

    url_real_prueba = "https://www.gob.pe/institucion/minedu/noticias/test-p6-prueba-verificada"

    # Asegurar que no exista previamente
    with obtener_conexion() as con:
        con.execute("DELETE FROM noticias WHERE url = ?", (url_real_prueba,))

    # Registrar noticia real
    exito, mensaje, nuevo_id = registrar_noticia(
        titulo="Noticia Real Verificada de Prueba P6",
        institucion="MINEDU",
        categoria="Ente rector",
        fuente="Portal MINEDU Prensa",
        fecha="2026-11-12",
        url=url_real_prueba,
        resumen="Registro de prueba verificada para validar el incremento de contador y preservación de URL.",
        prioridad="Alta",
        impacto_regulatorio="Alto",
        usuario="auditor_p6"
    )

    assert exito is True, f"El registro debe ser exitoso: {mensaje}"
    assert nuevo_id is not None

    # Comprobar que el contador aumentó en 1
    df_posterior = obtener_noticias()
    conteo_posterior = len(df_posterior)
    assert conteo_posterior == conteo_inicial + 1, "El contador total de noticias debe incrementarse exactamente en 1."

    # Comprobar que se conserva la URL directa íntegramente
    noticia_registrada = df_posterior[df_posterior["id"] == nuevo_id].iloc[0]
    assert noticia_registrada["url"] == url_real_prueba, "La URL directa debe conservarse exactamente idéntica a la ingresada."

    # Limpiar registro de prueba
    eliminar_noticia(nuevo_id, usuario="cleanup")

