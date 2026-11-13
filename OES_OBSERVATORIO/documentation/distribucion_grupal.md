# DISTRIBUCIÓN GRUPAL Y GUÍA DE EXPOSICIÓN — OES
## Plan de Trabajo en Equipo y Defensa Técnica del Laboratorio N.° 08

---

## 1. ESTRUCTURA DE RESPONSABILIDADES DEL EQUIPO

| Rol de Ingeniería | Responsable Sugerido | Módulos y Entregables Asignados |
|:------------------|:---------------------|:--------------------------------|
| **Líder de Proyecto y Arquitectura de Datos** | Integrante 1 | Diseño del esquema SQLite en 3FN (`database/schema.sql`), triggers de auditoría, configuración de entorno y orquestación general. |
| **Ingeniero Backend y Lógica de Negocio** | Integrante 2 | Desarrollo de módulos `noticias.py`, `instituciones.py`, `fuentes.py` y motor de validaciones antiduplicados. |
| **Ingeniero Frontend y Visualización (UI/UX)** | Integrante 3 | Desarrollo de `app.py`, `1_Dashboard.py`, `6_Indicadores.py`, integración de gráficos Plotly y estilos CSS institucionales. |
| **Ingeniero de Calidad y Pruebas (QA / Testing)** | Integrante 4 | Automatización de pruebas unitarias con Pytest (`tests/`), verificación de casos P1 a P6 y módulo de control ético (`5_Verificacion.py`). |
| **Especialista en Reportes y Documentación** | Integrante 5 | Implementación del motor de PDF en ReportLab (`modules/reportes.py`), redacción del informe técnico, diagramas Mermaid y análisis crítico. |

---

## 2. GUÍA DE EXPOSICIÓN ANTE LA DOCENTE (15 MINUTOS)

### Minuto 0:00 - 02:30 | Introducción y Delimitación Conceptual (Integrante 1)
- Explicar la diferencia sustantiva entre un simple portal de noticias y un **Observatorio Estratégico de Educación Superior**.
- Presentar la arquitectura de 6 capas y justificar la elección de tecnologías 100% locales (Python, SQLite, Streamlit).
- Destacar el respeto por la delimitación ética: los 3 registros didácticos del laboratorio no se presentan como noticias reales.

### Minuto 02:30 - 05:30 | Base de Datos Normalizada y Antiduplicados (Integrante 2)
- Abrir la consola o SQLite viewer y mostrar las 5 tablas normalizadas: `instituciones`, `fuentes`, `noticias`, `verificaciones`, `auditoria`.
- Demostrar en vivo la **Prueba P1**: ejecutar la carga de datos dos veces y comprobar que no se duplican las URLs.
- Demostrar el funcionamiento de las claves foráneas activadas con `PRAGMA foreign_keys = ON;`.

### Minuto 05:30 - 09:00 | Demostración del Dashboard y Funcionalidades (Integrante 3)
- Ejecutar `streamlit run app.py` y proyectar la interfaz principal.
- Demostrar los filtros obligatorios: **Prueba P2** (filtrar Universidad pública y mostrar UNMSM) y **Prueba P3** (buscar PUCP).
- Demostrar la **Prueba P4**: buscar un término inexistente y mostrar que el sistema responde limpiamente con 0 resultados sin caerse.
- Navegar por el Tablero de Monitoreo Plotly con gráficos de distribución por categoría y evolución temporal.

### Minuto 09:00 - 12:00 | Verificación Ética, Alertas y Pruebas P5-P6 (Integrante 4)
- Explicar el flujo *Human-in-the-Loop* en la página `5_Verificacion.py`: cómo un analista evalúa una noticia y le asigna estado (*Verificada*, *Pendiente*, *Observada*).
- Demostrar la **Prueba P6**: registrar una noticia real verificada y comprobar el incremento del contador y la preservación de la URL directa.
- Demostrar la **Prueba P5**: exportar el dataset a CSV y verificar que contiene encabezados y codificación compatible con Excel (UTF-8 con BOM).
- Ejecutar en terminal `python -m pytest tests -v` y mostrar las 15 pruebas pasando exitosamente.

### Minuto 12:00 - 15:00 | Generación de PDF, Auditoría y Conclusiones (Integrante 5)
- Demostrar la generación en vivo del **Informe Ejecutivo en PDF** desde la página `7_Reportes.py` con ReportLab.
- Mostrar la bitácora inmutable en `9_Auditoria.py` donde quedaron registradas todas las operaciones realizadas durante la sesión.
- Responder a las preguntas de reflexión de la docente basándose en el documento `analisis_critico.md`.

