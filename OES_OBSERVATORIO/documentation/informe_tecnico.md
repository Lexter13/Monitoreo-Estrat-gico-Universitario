# INFORME TÉCNICO DE INGENIERÍA DE SISTEMAS
## PROYECTO: OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)
### Versión 2.0 — Plataforma Integral de Vigilancia Tecnológica, Regulatoria y Calidad Universitaria

---

## 1. RESUMEN EJECUTIVO

El presente informe documenta el diseño, construcción, aseguramiento de calidad y despliegue del prototipo funcional del **Observatorio de Educación Superior (OES)**, desarrollado en cumplimiento estricto de las directivas y requerimientos establecidos en la **Práctica Guiada N.° 08**.

El sistema ha sido concebido desde los principios de la **Ingeniería de Software**, trascendiendo la mera recopilación agregada de noticias para transformarse en una plataforma integral de **monitoreo estratégico, trazabilidad de fuentes oficiales y control ético de calidad informativa**. La solución funciona de forma totalmente local en sistemas Windows, empleando **Python 3.11+**, **SQLite 3** como motor relacional con soporte de integridad referencial, **Streamlit** como framework de interfaz analítica, **Plotly** para visualización interactiva multidimensional y **ReportLab** para la emisión de informes técnicos ejecutivos en formato PDF.

---

## 2. MATRIZ DE CUMPLIMIENTO DE REQUISITOS (AUDITORÍA OFICIAL)

| ID | Requerimiento Oficial | Componente / Archivo | Funcionalidad Implementada | Prueba Asociada | Resultado | Estado |
|:---|:----------------------|:---------------------|:---------------------------|:----------------|:----------|:-------|
| **RF01** | Registro de noticias con fuente, institución, fecha, título, URL y categoría | `modules/noticias.py`<br>`pages/2_Noticias.py` | Formulario estructurado con validación regex de URL y restricción UNIQUE | P1, P6, Unitarias | Aprobado (100%) | **CUMPLIDO** |
| **RF02** | Filtrar por categoría, institución y texto | `modules/noticias.py`<br>`app.py`, `pages/1_Dashboard.py` | Consultas SQL parametrizadas con operadores `IN`, `LIKE` y filtros dinámicos | P2, P3, P4 | Aprobado (100%) | **CUMPLIDO** |
| **RF03** | Calcular indicadores cuantitativos y distribución | `modules/indicadores.py`<br>`pages/6_Indicadores.py` | Métricas dinámicas en tiempo real, KPIs globales y gráficos Plotly | P2, P3, P6 | Aprobado (100%) | **CUMPLIDO** |
| **RF04** | Exportar resultados filtrados a formato estándar | `modules/noticias.py`<br>`app.py` | Exportación CSV con codificación UTF-8 con BOM (`utf-8-sig`) para Microsoft Excel | P5 | Aprobado (100%) | **CUMPLIDO** |
| **RNF01** | Trazabilidad y ética informativa | `pages/10_Acerca_del_sistema.py`<br>`modules/verificaciones.py` | URLs directas persistidas, advertencia de datos demostrativos e historial de auditoría | P6, Inspección | Aprobado (100%) | **CUMPLIDO** |
| **RNF02** | Funcionamiento 100% local sin costos | `.env.example`, `app.py`<br>`database/conexion.py` | Despliegue en Windows sin APIs comerciales forzosas ni servicios de pago | Ejecución local | Aprobado (100%) | **CUMPLIDO** |
| **MEJ01** | Base de datos normalizada con claves foráneas | `database/schema.sql`<br>`database/conexion.py` | Tablas: `instituciones`, `fuentes`, `noticias`, `verificaciones`, `auditoria` con `PRAGMA foreign_keys = ON` | `test_database.py` | Aprobado (100%) | **CUMPLIDO** |
| **MEJ02** | Verificación humana de noticias | `modules/verificaciones.py`<br>`pages/5_Verificacion.py` | Estados: *Pendiente*, *Verificada*, *Observada*, asignación de revisor y observaciones | `test_validaciones.py` | Aprobado (100%) | **CUMPLIDO** |
| **MEJ03** | Emisión de Informes Ejecutivos en PDF | `modules/reportes.py`<br>`pages/7_Reportes.py` | Generación con ReportLab de informe con encabezado, KPIs, tablas y metodología | `test_exportacion.py` | Aprobado (100%) | **CUMPLIDO** |
| **MEJ04** | Detección de Alertas Tempranas | `modules/alertas.py`<br>`pages/8_Alertas.py` | Escáner de las 8 temáticas sensibles (Licenciamiento, Becas, Presupuesto, etc.) | `test_validaciones.py` | Aprobado (100%) | **CUMPLIDO** |
| **MEJ05** | Bitácora inmutable de Auditoría | `modules/auditoria.py`<br>`pages/9_Auditoria.py` | Triggers SQLite que capturan INSERT, UPDATE, DELETE y VERIFICACION | `test_database.py` | Aprobado (100%) | **CUMPLIDO** |
| **MEJ06** | Análisis asistido por IA / PLN local | `modules/analisis_ia.py` | Motor determinista basado en reglas y léxico educativo sin fuga de información | Inspección y prueba | Aprobado (100%) | **CUMPLIDO** |

---

## 3. ARQUITECTURA DEL SISTEMA Y TECNOLOGÍAS

El sistema adopta un modelo arquitectónico de **6 capas desacopladas**:
1. **Capa de Fuentes Oficiales:** Mapeo de portales institucionales de entes rectores (MINEDU, SUNEDU, CONCYTEC, PRONABEC) y universidades licenciadas.
2. **Capa de Ingesta y Validación:** Valida formatos, evita inyecciones mediante consultas preparadas e impide duplicados aplicando restricción `UNIQUE` sobre la URL canónica.
3. **Capa de Supervisión Ética:** Módulo Human-in-the-Loop donde analistas colegiados auditan y certifican la nota antes de considerarse un insumo verificado.
4. **Capa de Persistencia:** Base de datos relacional SQLite 3 con esquema normalizado en 3FN, índices B-Tree para optimización de filtros y triggers transaccionales.
5. **Capa de Servicios de Negocio:** Módulos Python encapsulados para cálculo de indicadores, generación de alertas por palabras clave y exportación binaria.
6. **Capa de Presentación:** Interfaz responsiva desarrollada con Streamlit y estilizada con CSS institucional moderno, enriquecida con gráficos vectoriales interactivos en Plotly.

---

## 4. RESULTADOS DE LAS PRUEBAS OBLIGATORIAS (P1 - P6)

Todas las pruebas exigidas en la sección 8 y 9 de la guía fueron automatizadas e incorporadas a la suite de pruebas bajo el framework `pytest`. En la ejecución oficial se obtuvieron **15 pruebas aprobadas sobre 15 (100% de éxito en 2.83 segundos)**:

1. **P1 (Antiduplicados):** La ejecución consecutiva del script de carga inicial no duplica ninguna de las tres URLs demostrativas originales de PRONABEC, UNMSM y PUCP.
2. **P2 (Filtro por Categoría):** Al filtrar por *"Universidad pública"*, se visualiza la UNMSM correctamente identificada como dato demostrativo de laboratorio (`es_demostrativo = 1`).
3. **P3 (Búsqueda de PUCP):** Al buscar la palabra clave *"PUCP"*, el sistema retorna la fila correspondiente preservando su enlace institucional.
4. **P4 (Búsqueda Inexistente):** Al buscar un término sin coincidencias, el sistema retorna 0 resultados limpiamente, mostrando un mensaje informativo sin excepciones ni bloqueos de interfaz.
5. **P5 (Exportación CSV):** El archivo exportado contiene los encabezados esperados y filas filtradas, codificado en `utf-8-sig` (BOM) para compatibilidad nativa con Microsoft Excel en Windows.
6. **P6 (Registro Real Verificado):** El registro de una noticia real con URL directa incrementa el contador general en 1 y preserva íntegramente su dirección web para auditoría externa.

---

## 5. CONCLUSIÓN GENERAL

El Observatorio de Educación Superior (OES) entregado constituye una solución robusta, mantenible y escalable. Cumple de manera integral con la especificación de la docente, respeta los límites éticos de la vigilancia tecnológica universitaria y entrega un software real listo para operar.

