# ARQUITECTURA DEL SISTEMA — OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)
## Documento de Diseño Arquitectónico y Especificación Técnica

---

## 1. VISIÓN GENERAL Y PRINCIPIOS DE DISEÑO

El **Observatorio de Educación Superior (OES)** está diseñado bajo una arquitectura en capas con bajo acoplamiento y alta cohesión (*Separation of Concerns*). 

### Principios Fundamentales:
1. **Trazabilidad Absoluta:** Ningún registro informativo puede ingresar a la base sin fecha explícita, denominación de la fuente y enlace web directo a la nota original.
2. **Control Ético (Human-in-the-Loop):** La tecnología asiste en la captura, pero un analista humano debe dictaminar la veracidad y calidad de la noticia mediante estados auditables (*Pendiente*, *Verificada*, *Observada*).
3. **Resiliencia Operativa:** Si un módulo secundario o servicio externo falla, la interfaz principal y los demás módulos continúan operando sin interrupción.
4. **Independencia de Proveedores de Pago:** El software opera de manera autosuficiente en Windows utilizando librerías open-source libres de costos recurrentes.

---

## 2. FLUJO LÓGICO DE LA INFORMACIÓN

```
[FUENTES OFICIALES]
  │ (MINEDU, SUNEDU, CONCYTEC, Universidades)
  ▼
[CAPTURA CONTROLADA]
  │ (Formularios estructurados, validación regex, restricción UNIQUE de URL)
  ▼
[VALIDACIÓN Y SUPERVISIÓN ÉTICA]
  │ (Analista asignado, dictamen: Pendiente/Verificada/Observada, bitácora)
  ▼
[BASE DE DATOS RELACIONAL SQLite]
  │ (Tablas 3FN: instituciones, fuentes, noticias, verificaciones, auditoria)
  ▼
[CAPA ANALÍTICA Y PRESENTACIÓN]
  │ (Streamlit, Plotly, filtros dinámicos, detector de alertas temáticas)
  ▼
[SALIDAS Y APOYO A LA TOMA DE DECISIONES]
    (Dashboard ejecutivo, CSV con BOM, Informes PDF en ReportLab)
```

---

## 3. DESGLOSE DE CAPAS DEL SISTEMA

### 3.1. Capa de Datos (SQLite 3 Normalizada)
- **Motor:** SQLite 3 integrado nativamente en Python.
- **Integridad:** Claves foráneas habilitadas explícitamente mediante `PRAGMA foreign_keys = ON;`.
- **Automatización:** Triggers SQL para el registro inmutable de auditoría forense (`trg_noticias_audit_insert`, `trg_noticias_audit_update`, `trg_noticias_audit_delete`, `trg_verificacion_sync`).
- **Optimización:** Índices B-Tree en columnas de alta selectividad (`fecha`, `categoria`, `institucion`, `estado_verificacion`).

### 3.2. Capa de Lógica de Negocio (`modules/`)
- `noticias.py`: Reglas de negocio para registro, prevención de duplicados, filtros avanzados y exportación compatible con Excel.
- `instituciones.py`: Mantenimiento del catálogo maestro institucional y estadísticas de cobertura.
- `fuentes.py`: Evaluación y registro de fuentes formales y confiabilidad.
- `indicadores.py`: Métricas estadísticas consolidadas y visualizaciones vectoriales con Plotly.
- `verificaciones.py`: Flujo de trabajo de calidad ética y asignación de analistas responsables.
- `reportes.py`: Motor de maquetación y generación de documentos PDF con ReportLab.
- `auditoria.py`: Consulta forense de transacciones y operaciones del sistema.
- `alertas.py`: Algoritmo de correspondencia léxica sobre los 8 ejes regulatorios universitarios.
- `analisis_ia.py`: Motor determinista local de procesamiento de lenguaje natural simbólico.

### 3.3. Capa de Presentación (`app.py` y `pages/`)
- Desarrollada en **Streamlit** bajo arquitectura multipágina nativa.
- Estilos visuales personalizados mediante inyección de CSS institucional (`assets/styles.css`).
- Interfaz reactiva adaptada para computadoras personales y laptops bajo Windows.

---

## 4. CONSIDERACIONES DE SEGURIDAD Y CALIDAD

1. **Prevención de Inyecciones SQL:** Todas las consultas a la base de datos se ejecutan a través de parámetros tipados (`?`), sin concatenación de cadenas en sentencias SQL.
2. **Validación de Entradas:** Validación estricta de campos obligatorios y expresiones regulares para URLs.
3. **Manejo de Excepciones:** Bloques `try/except` estructurados con retorno de tuplas `(exito, mensaje)` para evitar caídas de servidor.
4. **Preservación de Codificación:** Exportación en UTF-8 con BOM (`utf-8-sig`) para garantizar que tildes y caracteres especiales se abran sin alteraciones en Microsoft Excel para Windows.

