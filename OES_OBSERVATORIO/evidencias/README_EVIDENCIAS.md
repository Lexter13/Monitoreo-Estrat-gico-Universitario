# REGISTRO DE EVIDENCIAS DE PRUEBAS Y VALIDACIÓN — OES
## Práctica Guiada N.° 08: Observatorio de Educación Superior

---

## 1. REGISTRO OFICIAL DE EJECUCIÓN DE PRUEBAS AUTOMATIZADAS (PYTEST)

A continuación se transcribe la salida real obtenida de la ejecución de la suite automatizada de pruebas ejecutada en la consola del sistema:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\xampp\htdocs\Marketing con IA\OES_OBSERVATORIO
plugins: anyio-4.16.0
collecting ... collected 15 items

tests/test_database.py::test_claves_foraneas_activadas PASSED            [  6%]
tests/test_database.py::test_tablas_principales_creadas PASSED           [ 13%]
tests/test_database.py::test_disparador_auditoria_automatico PASSED      [ 20%]
tests/test_exportacion.py::test_prueba_p5_exportacion_csv PASSED         [ 26%]
tests/test_exportacion.py::test_generacion_reporte_pdf PASSED            [ 33%]
tests/test_filtros.py::test_prueba_p2_filtrar_universidad_publica PASSED [ 40%]
tests/test_filtros.py::test_prueba_p3_buscar_pucp PASSED                 [ 46%]
tests/test_filtros.py::test_prueba_p4_buscar_termino_inexistente PASSED  [ 53%]
tests/test_noticias.py::test_prueba_p1_evitar_duplicados_en_doble_carga PASSED [ 60%]
tests/test_noticias.py::test_prueba_p6_registro_noticia_real_verificada PASSED [ 66%]
tests/test_validaciones.py::test_validacion_campos_obligatorios PASSED   [ 73%]
tests/test_validaciones.py::test_validacion_formato_url PASSED           [ 80%]
tests/test_validaciones.py::test_rechazo_url_duplicada PASSED            [ 86%]
tests/test_validaciones.py::test_validacion_estado_verificacion_invalido PASSED [ 93%]
tests/test_validaciones.py::test_deteccion_alertas_normativas PASSED     [100%]

============================= 15 passed in 2.83s ==============================
```

---

## 2. GUÍA Y ESPACIOS ASIGNADOS PARA CAPTURAS DE PANTALLA REALES

Para documentar la entrega física requerida por la docente, tome capturas de pantalla de la aplicación en ejecución (`Win + Shift + S` en Windows) y guárdelas en esta carpeta con los siguientes nombres:

### Espacio E1: Tablero Principal de Streamlit (`captura_01_dashboard.png`)
- **Procedimiento:** Ejecutar `streamlit run app.py`, abrir el navegador en `http://localhost:8501` y capturar el encabezado institucional, las 4 tarjetas de métricas y el gráfico de barras.
- **Evidencia requerida:** Visualización de noticias, instituciones y distribución temática inicial.

### Espacio E2: Prueba P2 - Filtro Universidad Pública (`captura_02_filtro_p2.png`)
- **Procedimiento:** En la barra lateral, desmarcar todas las categorías excepto *"Universidad pública"*.
- **Evidencia requerida:** La tabla debe mostrar únicamente a la UNMSM con su URL y resumen demostrativo.

### Espacio E3: Prueba P3 - Búsqueda de PUCP (`captura_03_busqueda_p3.png`)
- **Procedimiento:** Escribir *"PUCP"* en la caja de búsqueda de la barra lateral.
- **Evidencia requerida:** La tabla debe filtrar y mostrar exactamente la fila de PUCP.

### Espacio E4: Prueba P4 - Término Inexistente (`captura_04_inexistente_p4.png`)
- **Procedimiento:** Escribir un término que no exista (ej. *"X9Z9"*).
- **Evidencia requerida:** Mensaje informativo: *"No hay resultados con esos filtros"* sin error en pantalla.

### Espacio E5: Prueba P5 - Archivo CSV Descargado (`captura_05_csv_p5.png`)
- **Procedimiento:** Presionar el botón *"Exportar CSV"* y abrir el archivo `oes_resultados.csv` en Microsoft Excel o bloc de notas.
- **Evidencia requerida:** Encabezados correctos (`fecha`, `institucion`, `categoria`, etc.) y visualización adecuada de tildes gracias a UTF-8 con BOM.

### Espacio E6: Prueba P6 - Registro de Noticia Real (`captura_06_noticia_real_p6.png`)
- **Procedimiento:** Ir a la página `2_Noticias.py`, pestaña *"Registrar Noticia"*, ingresar una noticia con URL real y guardar.
- **Evidencia requerida:** Mensaje de éxito verde con ID asignado y reflejo en el contador del dashboard.

### Espacio E7: Informe PDF Generado con ReportLab (`captura_07_informe_pdf.png`)
- **Procedimiento:** Ir a la página `7_Reportes.py`, presionar *"Compilar y Generar PDF Oficial"* y abrir el documento descargado.
- **Evidencia requerida:** Documento formal con logotipo OES, tabla de noticias con trazabilidad de URL y firma de auditoría.

