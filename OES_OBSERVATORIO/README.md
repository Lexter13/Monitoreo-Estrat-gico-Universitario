# OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)
## Prototipo Académico de Monitoreo Institucional, Regulatorio y Calidad Universitaria
### Práctica Guiada N.° 08 — Ingeniería de Sistemas (Versión 2.0 Normalizada)

---

## 1. DESCRIPCIÓN DEL PROYECTO

El **Observatorio de Educación Superior (OES)** es una plataforma de software diseñada para registrar, clasificar, auditar, consultar y visualizar novedades y directivas del ecosistema universitario peruano con absoluta **trazabilidad de fuentes oficiales**.

Construido íntegramente bajo estándares profesionales de **Ingeniería de Software**, el sistema integra:
- **Base de datos normalizada (SQLite 3):** Soporte de claves foráneas activas (`PRAGMA foreign_keys = ON;`), triggers de auditoría inmutable e índices de rendimiento.
- **Flujo de Calidad Ética (*Human-in-the-Loop*):** Supervisión humana obligatoria con estados de revisión (*Pendiente*, *Verificada*, *Observada*).
- **Tableros Analíticos:** Visualizaciones interactivas con Plotly y Streamlit.
- **Emisión Oficial de Informes en PDF:** Compilación nativa con ReportLab.
- **Detección Temprana de Alertas:** Escaneo automático de 8 ejes regulatorios universitarios sensibles.
- **Exportación Estándar:** Descarga de datasets filtrados en CSV con codificación UTF-8 con BOM (`utf-8-sig`) compatible con Microsoft Excel.

---

## 2. ESTRUCTURA FÍSICA DEL PROYECTO

```text
OES_OBSERVATORIO/
│
├── app.py                      # Aplicación principal Streamlit (Dashboard y navegación)
├── preparar_datos.py           # Script de preparación inicial y carga de datos demostrativos
├── requirements.txt            # Dependencias oficiales del proyecto
├── README.md                   # Manual de usuario e instrucciones técnicas
├── .gitignore                  # Exclusiones de control de versiones
├── .env.example                # Plantilla de variables de entorno
├── iniciar.bat                 # Script de arranque rápido para Windows
│
├── database/                   # Capa de Persistencia Relacional
│   ├── oes.db                  # Base de datos SQLite 3 inicializada
│   ├── conexion.py             # Módulo de conexión con soporte de claves foráneas
│   ├── schema.sql              # Esquema DDL normalizado (3FN), índices y triggers
│   └── inicializar_db.py       # Rutina de migración y carga del catálogo maestro
│
├── modules/                    # Capa de Lógica de Negocio y Servicios
│   ├── __init__.py             # Metadatos del paquete
│   ├── noticias.py             # CRUD de noticias, validaciones y exportación CSV
│   ├── instituciones.py        # Directorio de universidades y entes rectores
│   ├── fuentes.py              # Gestión y auditoría de fuentes oficiales
│   ├── indicadores.py          # Cálculo de KPIs y gráficos interactivos con Plotly
│   ├── verificaciones.py       # Workflow de control ético y supervisión humana
│   ├── reportes.py             # Motor de compilación de informes PDF con ReportLab
│   ├── auditoria.py            # Bitácora forense de operaciones del sistema
│   ├── alertas.py              # Escáner de alertas por palabras clave normativas
│   └── analisis_ia.py          # Motor determinista local de PLN basado en reglas
│
├── pages/                      # Interfaz Web Multipágina (Streamlit)
│   ├── 1_Dashboard.py          # Tablero ejecutivo con gráficos Plotly y filtros dinámicos
│   ├── 2_Noticias.py           # Consulta, registro estructurado, edición y bajas
│   ├── 3_Instituciones.py      # Catálogo y registro de universidades públicas y privadas
│   ├── 4_Fuentes.py            # Directorio de canales oficiales y niveles de confiabilidad
│   ├── 5_Verificacion.py       # Auditoría humana, asignación de analistas y dictámenes
│   ├── 6_Indicadores.py        # Análisis cuantitativo, ratios y tablas de resumen
│   ├── 7_Reportes.py           # Generador y descargador de informes PDF oficiales
│   ├── 8_Alertas.py            # Matriz de alertas normativas y coincidencias
│   └── 9_Auditoria.py          # Historial cronológico de cambios y transacciones
│
├── assets/                     # Recursos Visuales y Estilos
│   └── styles.css              # Hoja de estilos institucionales y tarjetas de métricas
│
├── reports/                    # Directorio de almacenamiento de reportes PDF generados
│
├── documentation/              # Documentación de Ingeniería
│   ├── informe_tecnico.md      # Informe de ingeniería y matriz de cumplimiento
│   ├── arquitectura.md         # Documento de arquitectura en 6 capas
│   ├── diccionario_datos.md    # Diccionario completo de tablas, campos y restricciones
│   ├── casos_de_prueba.md      # Matriz de pruebas automatizadas y resultados
│   ├── analisis_critico.md     # Respuestas a las 5 preguntas de reflexión y límites éticos
│   ├── conclusiones.md         # Conclusiones y recomendaciones para futuras fases
│   └── distribucion_grupal.md  # Distribución de responsabilidades y guía de exposición
│
├── diagrams/                   # Diagramas en Formato Mermaid
│   ├── arquitectura.mmd        # Diagrama de flujo arquitectónico
│   ├── modelo_er.mmd           # Diagrama Entidad-Relación normalizado
│   └── flujo_sistema.mmd       # Diagrama de secuencia del flujo operativo
│
├── tests/                      # Suite de Pruebas Automatizadas con Pytest
│   ├── test_database.py        # Pruebas de conexión, claves foráneas y triggers
│   ├── test_noticias.py        # Pruebas obligatorias P1 y P6
│   ├── test_filtros.py         # Pruebas obligatorias P2, P3 y P4
│   ├── test_exportacion.py     # Pruebas obligatorias P5 y compilación de PDF
│   └── test_validaciones.py    # Pruebas de integridad, URLs y estados de revisión
│
├── data/                       # Datasets de Arranque
│   └── datos_demostrativos.py  # Registros demostrativos del laboratorio y noticias reales
│
└── evidencias/                 # Evidencias de Ejecución
    └── README_EVIDENCIAS.md    # Log de pytest (15/15) e instrucciones para capturas
```

---

## 3. REQUISITOS DEL SISTEMA

- **Sistema Operativo:** Windows 10 o Windows 11 (también compatible con macOS y Linux).
- **Lenguaje:** Python 3.11, 3.12, 3.13 o 3.14.
- **Navegador Web:** Google Chrome, Microsoft Edge, Mozilla Firefox o Brave.
- **Conectividad:** Funciona **100% offline y de manera local**, sin necesidad de conexión permanente ni servicios de suscripción de pago.

---

## 4. INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN (PASO A PASO)

Abra una ventana de **PowerShell** o **Símbolo del sistema (CMD)** en la carpeta del proyecto `OES_OBSERVATORIO` y ejecute los siguientes comandos:

### Paso 1: Crear y activar el entorno virtual (Recomendado)
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Paso 2: Instalar las dependencias del proyecto
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 3: Inicializar la base de datos SQLite
```powershell
python preparar_datos.py
```
*Salida esperada: Mensaje confirmando la creación y sincronización de `oes.db` con el esquema normalizado y los 3 registros demostrativos del laboratorio.*

### Paso 4: Ejecutar la aplicación web Streamlit
```powershell
streamlit run app.py
```
*El sistema abrirá automáticamente su navegador en `http://localhost:8501` mostrando el Observatorio en funcionamiento.*

---

## 5. EJECUCIÓN DE PRUEBAS AUTOMATIZADAS (PYTEST)

Para comprobar la calidad del software y validar los casos obligatorios (P1 a P6), ejecute:

```powershell
python -m pytest tests -v
```

**Resultado verificado:**
```text
tests/test_database.py::test_claves_foraneas_activadas PASSED
tests/test_database.py::test_tablas_principales_creadas PASSED
tests/test_database.py::test_disparador_auditoria_automatico PASSED
tests/test_exportacion.py::test_prueba_p5_exportacion_csv PASSED
tests/test_exportacion.py::test_generacion_reporte_pdf PASSED
tests/test_filtros.py::test_prueba_p2_filtrar_universidad_publica PASSED
tests/test_filtros.py::test_prueba_p3_buscar_pucp PASSED
tests/test_filtros.py::test_prueba_p4_buscar_termino_inexistente PASSED
tests/test_noticias.py::test_prueba_p1_evitar_duplicados_en_doble_carga PASSED
tests/test_noticias.py::test_prueba_p6_registro_noticia_real_verificada PASSED
tests/test_validaciones.py::test_validacion_campos_obligatorios PASSED
tests/test_validaciones.py::test_validacion_formato_url PASSED
tests/test_validaciones.py::test_rechazo_url_duplicada PASSED
tests/test_validaciones.py::test_validacion_estado_verificacion_invalido PASSED
tests/test_validaciones.py::test_deteccion_alertas_normativas PASSED

============================= 15 passed in 2.83s ==============================
```

---

## 6. VERIFICACIÓN DE LAS 6 PRUEBAS OFICIALES DEL LABORATORIO

| Prueba | Descripción del Laboratorio | Cómo Verificarla en la Aplicación |
|:------:|:----------------------------|:-----------------------------------|
| **P1** | Carga doble no duplica URLs | Ejecutar `python preparar_datos.py` dos veces. El conteo de las 3 URLs demostrativas se mantiene estrictamente en 1. |
| **P2** | Filtrar Universidad pública | En el menú lateral de `app.py`, filtrar por *"Universidad pública"*. Se despliega la fila de UNMSM como dato demostrativo. |
| **P3** | Buscar PUCP | En el buscador escribir *"PUCP"*. Retorna la fila correspondiente de la PUCP con su URL institucional. |
| **P4** | Término inexistente | En el buscador escribir un término inexistente (ej. *"XYZ99"*). Se muestra *"0 noticias y aviso informativo"* sin error. |
| **P5** | Exportar CSV | Presionar *"Exportar CSV"*. El archivo `oes_resultados.csv` se descarga con encabezados y codificación UTF-8 con BOM. |
| **P6** | Noticia real verificada | En la página `2_Noticias.py`, registrar una noticia con URL real. El contador general se incrementa en +1 y la URL directa se preserva intacta. |

---

## 7. CRÉDITOS Y DELIMITACIÓN ACADÉMICA

Proyecto desarrollado por el **Equipo de Ingeniería de Sistemas** para la **Práctica Guiada N.° 08: Construcción de un Observatorio de Educación Superior (OES)**. 

*Aviso ético:* Los registros iniciales de PRONABEC, UNMSM y PUCP corresponden a ejemplos didácticos de laboratorio; para su uso en decisiones institucionales deben cotejarse con sus respectivas fuentes originales.

