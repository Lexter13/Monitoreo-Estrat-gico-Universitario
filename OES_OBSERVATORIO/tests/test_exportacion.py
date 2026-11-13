"""
Pruebas de Exportación y Generación de Reportes del Documento:
- P5: Exportar CSV y comprobar que el archivo contiene encabezados y filas filtradas.
- Verificación de compilación de informes oficiales en PDF con ReportLab.
"""

import io
import pytest
import pandas as pd
from database.inicializar_db import inicializar_base_datos
from modules.noticias import obtener_noticias, exportar_noticias_csv
from modules.reportes import generar_informe_pdf


@pytest.fixture(autouse=True)
def init_db():
    inicializar_base_datos(cargar_verificadas=True, verbose=False)


def test_prueba_p5_exportacion_csv():
    """
    PRUEBA P5 DEL DOCUMENTO:
    Exportar CSV y comprobar que el archivo contiene encabezados y filas filtradas con codificación UTF-8 BOM.
    """
    df_filtrado = obtener_noticias(categorias=["Universidad pública"])
    assert not df_filtrado.empty, "Debe haber registros filtrados para la prueba de exportación."

    csv_bytes = exportar_noticias_csv(df_filtrado)
    assert isinstance(csv_bytes, bytes), "La exportación debe retornar un objeto de bytes."
    assert len(csv_bytes) > 0, "Los bytes del CSV no deben estar vacíos."

    # Comprobar BOM UTF-8 (\xef\xbb\xbf) para compatibilidad con Microsoft Excel
    assert csv_bytes.startswith(b'\xef\xbb\xbf'), "El CSV debe incluir BOM UTF-8 (utf-8-sig) para compatibilidad con Excel."

    # Decodificar y validar estructura con pandas
    csv_str = csv_bytes.decode("utf-8-sig")
    df_leido = pd.read_csv(io.StringIO(csv_str))

    # Comprobar encabezados obligatorios
    encabezados_esperados = ["fecha", "institucion", "categoria", "titulo", "fuente", "url"]
    for enc in encabezados_esperados:
        assert enc in df_leido.columns, f"El encabezado '{enc}' debe estar presente en el CSV exportado."

    # Comprobar número de filas coincidentes
    assert len(df_leido) == len(df_filtrado), "La cantidad de filas en el CSV debe ser idéntica a la filtrada."


def test_generacion_reporte_pdf():
    """Comprueba que el módulo de reportes genere un binario PDF válido (iniciando con %PDF)."""
    df = obtener_noticias()
    pdf_bytes = generar_informe_pdf(
        df_filtrado=df,
        titulo_informe="INFORME DE TEST",
        filtros_aplicados_texto="Prueba unitaria"
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000, "El PDF generado debe tener un tamaño razonable."
    assert pdf_bytes.startswith(b"%PDF"), "El archivo binario generado debe tener el encabezado oficial %PDF."

