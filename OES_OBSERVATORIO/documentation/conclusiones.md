# CONCLUSIONES Y RECOMENDACIONES — OES
## Proyecto de Ingeniería de Sistemas: Observatorio de Educación Superior

---

## 1. CONCLUSIONES DEL PROYECTO

1. **Cumplimiento Integral de la Especificación Académica:** Se construyó exitosamente el 100% de los requerimientos funcionales y no funcionales exigidos en la Práctica Guiada N.° 08, logrando una tasa de aprobación del 100% (15/15) en las pruebas automatizadas bajo `pytest`.
2. **Elevación del Nivel Técnico mediante Normalización:** La base de datos fue profesionalizada desde una estructura plana hacia un esquema relacional normalizado en 3FN (`instituciones`, `fuentes`, `noticias`, `verificaciones`, `auditoria`), manteniendo total retrocompatibilidad con las consultas originales del laboratorio y activando claves foráneas reales en SQLite.
3. **Incorporación del Paradigma Human-in-the-Loop:** La implementación del módulo de verificación ética garantiza que la tecnología actúe como aceleradora de la captura, pero delegando en el analista humano la certificación de la calidad informativa, mitigando el riesgo de propagación de noticias falsas o datos no contrastados.
4. **Capacidad de Salida Multi-Formato:** El sistema no se limita a mostrar un tablero web; genera archivos CSV normalizados con firma BOM para Microsoft Excel y compila de forma nativa informes ejecutivos oficiales en formato PDF con encabezados institucionales, resúmenes estadísticos y advertencias metodológicas mediante ReportLab.
5. **Independencia Tecnológica y Despliegue Local:** La solución opera íntegramente en Windows sin incurrir en costos de suscripción ni depender de servicios en la nube de pago, lo que asegura su viabilidad y reproducibilidad para futuros proyectos estudiantiles.

---

## 2. RECOMENDACIONES PARA VERSIONES FUTURAS

1. **Integración con Canales RSS y APIs de Datos Abiertos:** Automatizar la ingesta controlada consumiendo los feeds RSS oficiales del diario *El Peruano* (separata de normas legales) y la API de contrataciones del Estado (SEACE) bajo cronogramas periódicos controlados.
2. **Interoperabilidad con la Plataforma Nacional de Datos Abiertos:** Implementar conectores directos con el catálogo de datos abiertos de la SUNEDU para sincronizar automáticamente el estado de licenciamiento de programas y sedes universitarias.
3. **Módulo de Análisis Semántico Avanzado:** Evaluar la incorporación de embeddings locales ligeros (ej. modelos de HuggingFace en ONNX Runtime) para agrupar noticias por similitud temática sin requerir GPUs dedicadas ni servicios en la nube.
4. **Control de Acceso Basado en Roles (RBAC):** Extender el módulo de usuarios para diferenciar perfiles de *Lector*, *Analista Capturador* y *Auditor Certificador*, incorporando autenticación segura con contraseñas cifradas en Argon2 o Bcrypt.

