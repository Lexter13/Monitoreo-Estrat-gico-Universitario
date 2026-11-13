# CASOS DE PRUEBA Y EVIDENCIAS DE EJECUCIÓN — OES
## Suite de Pruebas Automatizadas y Matriz de Validación con Pytest

---

## 1. RESUMEN GENERAL DE EJECUCIÓN

- **Entorno de Pruebas:** Windows 10/11 x64, Python 3.14 / 3.11+.
- **Framework de Pruebas:** `pytest 9.2.0`.
- **Total de Pruebas Ejecutadas:** 15 pruebas automatizadas.
- **Pruebas Aprobadas:** 15 (100%).
- **Pruebas Fallidas:** 0 (0%).
- **Tiempo Total de Ejecución:** 2.83 segundos.

---

## 2. DETALLE DE CASOS DE PRUEBA OFICIALES (P1 A P6)

### Caso P1: Prevención de duplicados en doble carga
- **Procedimiento:** Ejecutar la rutina de preparación de datos dos veces consecutivas sobre la base de datos `oes.db`.
- **Criterio de Aceptación:** Las 3 URLs originales de PRONABEC, UNMSM y PUCP deben figurar exactamente una sola vez. No debe ocurrir inserción duplicada.
- **Implementación:** `tests/test_noticias.py::test_prueba_p1_evitar_duplicados_en_doble_carga`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. Conteos de URL = 1 para cada entidad.

### Caso P2: Filtrar categoría Universidad pública
- **Procedimiento:** Invocar la consulta filtrada con categoría *"Universidad pública"*.
- **Criterio de Aceptación:** Debe figurar el registro demostrativo de UNMSM con `es_demostrativo = 1`.
- **Implementación:** `tests/test_filtros.py::test_prueba_p2_filtrar_universidad_publica`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. Fila retornada correctamente.

### Caso P3: Búsqueda textual de PUCP
- **Procedimiento:** Ejecutar búsqueda por el término textual *"PUCP"*.
- **Criterio de Aceptación:** Retorna al menos una fila con el registro de la Pontificia Universidad Católica del Perú.
- **Implementación:** `tests/test_filtros.py::test_prueba_p3_buscar_pucp`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. Registro recuperado con URL `https://www.pucp.edu.pe/`.

### Caso P4: Búsqueda de término inexistente
- **Procedimiento:** Consultar por una cadena inexistente (`TERMINO_COMPLETAMENTE_INEXISTENTE_XYZ_9999`).
- **Criterio de Aceptación:** Retornar 0 registros y DataFrame vacío sin generar excepciones SQL ni errores de interfaz.
- **Implementación:** `tests/test_filtros.py::test_prueba_p4_buscar_termino_inexistente`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. 0 registros retornados limpiamente.

### Caso P5: Exportación de datos a formato CSV
- **Procedimiento:** Filtrar registros y llamar a la función `exportar_noticias_csv(df)`.
- **Criterio de Aceptación:** El binario retornado debe incluir encabezados normalizados (`fecha`, `institucion`, `categoria`, `titulo`, `fuente`, `url`), la misma cantidad de filas filtradas y la firma de bytes BOM UTF-8 (`\xef\xbb\xbf`) para compatibilidad con Excel.
- **Implementación:** `tests/test_exportacion.py::test_prueba_p5_exportacion_csv`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. CSV verificado con pandas y bytes BOM intactos.

### Caso P6: Registro de noticia real verificada
- **Procedimiento:** Insertar una noticia real mediante `registrar_noticia(...)` con URL directa oficial.
- **Criterio de Aceptación:** El contador general de noticias debe incrementarse exactamente en 1 y la URL directa debe conservarse idéntica sin truncamiento.
- **Implementación:** `tests/test_noticias.py::test_prueba_p6_registro_noticia_real_verificada`.
- **Resultado Obtenido:** **PASSED (APROBADO)**. Contador incrementado en +1 y URL persistida.

---

## 3. PRUEBAS DE MEJORAS GRUPALES Y ARQUITECTURA

| Test Case | Función Evaluada | Módulo | Resultado |
|:----------|:-----------------|:-------|:---------:|
| `test_claves_foraneas_activadas` | Soporte de claves foráneas en SQLite (`PRAGMA foreign_keys`) | `database/conexion.py` | **PASSED** |
| `test_tablas_principales_creadas` | Existencia física de las 5 tablas relacionales | `database/schema.sql` | **PASSED** |
| `test_disparador_auditoria_automatico` | Disparo de trigger SQL automático ante eventos INSERT | `database/schema.sql` | **PASSED** |
| `test_generacion_reporte_pdf` | Compilación de archivo binario PDF con ReportLab (`%PDF`) | `modules/reportes.py` | **PASSED** |
| `test_validacion_campos_obligatorios` | Rechazo de registros con título o URL vacía | `modules/noticias.py` | **PASSED** |
| `test_validacion_formato_url` | Validador regex de protocolos `http://` y `https://` | `modules/noticias.py` | **PASSED** |
| `test_rechazo_url_duplicada` | Rechazo a nivel de aplicación de URLs repetidas | `modules/noticias.py` | **PASSED** |
| `test_validacion_estado_verificacion_invalido` | Rechazo de estados éticos fuera del catálogo permitido | `modules/verificaciones.py` | **PASSED** |
| `test_deteccion_alertas_normativas` | Detección de palabras clave críticas de licenciamiento y calidad | `modules/alertas.py` | **PASSED** |

