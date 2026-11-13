"""
Pruebas de Filtros y Búsqueda del Documento Oficial:
- P2: Filtrar Universidad pública y comprobar que aparece UNMSM como dato demostrativo.
- P3: Buscar PUCP y comprobar que aparece una fila.
- P4: Buscar un término inexistente y comprobar que aparecen cero resultados sin errores.
"""

import pytest
from database.inicializar_db import inicializar_base_datos
from modules.noticias import obtener_noticias


@pytest.fixture(autouse=True)
def init_db():
    inicializar_base_datos(cargar_verificadas=True, verbose=False)


def test_prueba_p2_filtrar_universidad_publica():
    """
    PRUEBA P2 DEL DOCUMENTO:
    Filtrar 'Universidad pública' y comprobar que aparece UNMSM como dato demostrativo.
    """
    df = obtener_noticias(categorias=["Universidad pública"])
    
    assert not df.empty, "La consulta por 'Universidad pública' no debe estar vacía."
    
    # Comprobar que UNMSM está presente
    instituciones = df["institucion"].tolist()
    assert "UNMSM" in instituciones, "UNMSM debe aparecer entre los resultados de 'Universidad pública'."
    
    # Comprobar que el registro didáctico de UNMSM tiene es_demostrativo = 1
    unmsm_demo = df[(df["institucion"] == "UNMSM") & (df["url"] == "https://www.unmsm.edu.pe/")]
    assert len(unmsm_demo) == 1, "Debe existir el registro demostrativo original de UNMSM."
    assert unmsm_demo.iloc[0]["es_demostrativo"] == 1


def test_prueba_p3_buscar_pucp():
    """
    PRUEBA P3 DEL DOCUMENTO:
    Buscar PUCP y comprobar que aparece una fila en los registros demostrativos.
    """
    df = obtener_noticias(busqueda_texto="PUCP")
    
    # Debe aparecer al menos una fila correspondiente a PUCP
    assert len(df) >= 1, "La búsqueda de PUCP debe retornar al menos una fila."
    
    # Comprobar que el registro demostrativo de PUCP está presente
    pucp_demo = df[df["url"] == "https://www.pucp.edu.pe/"]
    assert len(pucp_demo) == 1, "El registro demostrativo de PUCP debe aparecer con su URL oficial."
    assert pucp_demo.iloc[0]["institucion"] == "PUCP"


def test_prueba_p4_buscar_termino_inexistente():
    """
    PRUEBA P4 DEL DOCUMENTO:
    Buscar un término inexistente y comprobar que aparecen cero resultados sin errores.
    """
    termino_fantasma = "TERMINO_COMPLETAMENTE_INEXISTENTE_XYZ_9999"
    
    df = obtener_noticias(busqueda_texto=termino_fantasma)
    
    # Comprobar que no lanza error y retorna un DataFrame vacío
    assert df is not None, "La función debe retornar un DataFrame válido, no None."
    assert len(df) == 0, f"La búsqueda del término inexistente debe dar 0 resultados, obtuvo {len(df)}."
    assert df.empty is True, "El DataFrame resultante debe estar vacío."

