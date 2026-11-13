# DICCIONARIO DE DATOS — OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)
## Estructura Relacional de la Base de Datos SQLite (`database/oes.db`)

---

## 1. TABLA: `instituciones`
Almacena el catálogo oficial de universidades, entes rectores e institutos de educación superior bajo vigilancia.

| Campo | Tipo de Dato | Nulo | Restricciones / Descripción |
|:------|:-------------|:----:|:----------------------------|
| `id` | INTEGER | NO | PRIMARY KEY AUTOINCREMENT. Identificador único de la institución. |
| `nombre` | TEXT | NO | UNIQUE. Nombre oficial completo de la institución (ej. "UNMSM"). |
| `tipo` | TEXT | NO | CHECK (`tipo` IN ('Universidad pública', 'Universidad privada', 'Ente rector', 'Instituto superior', 'Organismo internacional')). |
| `siglas` | TEXT | SÍ | Acrónimo o sigla institucional (ej. "SUNEDU", "PUCP"). |
| `region` | TEXT | SÍ | Departamento o ámbito territorial (Default: 'Lima'). |
| `estado_licenciamiento` | TEXT | SÍ | CHECK ('Licenciada', 'En proceso', 'Denegada', 'No aplica'). Default: 'Licenciada'. |
| `sitio_web` | TEXT | SÍ | URL del portal institucional raíz. |
| `fecha_registro` | TEXT | SÍ | Marca temporal de creación (Default: datetime('now', 'localtime')). |

---

## 2. TABLA: `fuentes`
Registra los medios formales y portales de difusión monitoreados por el observatorio.

| Campo | Tipo de Dato | Nulo | Restricciones / Descripción |
|:------|:-------------|:----:|:----------------------------|
| `id` | INTEGER | NO | PRIMARY KEY AUTOINCREMENT. Identificador único de la fuente. |
| `nombre` | TEXT | NO | UNIQUE. Nombre del medio o portal (ej. "Diario Oficial El Peruano"). |
| `tipo_fuente` | TEXT | NO | CHECK ('Portal institucional', 'Boletín oficial', 'Diario de circulación', 'Agencia estatal', 'Red social oficial'). |
| `url_base` | TEXT | NO | URL raíz del sitio emisor. |
| `confiabilidad` | TEXT | SÍ | CHECK ('Alta', 'Media', 'En verificación'). Default: 'Alta'. |
| `fecha_registro` | TEXT | SÍ | Marca temporal de alta en el sistema. |

---

## 3. TABLA: `noticias`
Entidad principal que almacena las novedades capturadas, garantizando compatibilidad con la Práctica 08 y normalización relacional.

| Campo | Tipo de Dato | Nulo | Restricciones / Descripción |
|:------|:-------------|:----:|:----------------------------|
| `id` | INTEGER | NO | PRIMARY KEY AUTOINCREMENT. Identificador de la noticia. |
| `titulo` | TEXT | NO | Titular completo de la novedad capturada. |
| `institucion` | TEXT | NO | Nombre textual de la institución involucrada. |
| `categoria` | TEXT | NO | Categoría temática del registro (ej. "Ente rector", "Universidad pública"). |
| `fuente` | TEXT | NO | Nombre del canal o fuente oficial de origen. |
| `fecha` | TEXT | NO | Fecha de publicación original en formato ISO `YYYY-MM-DD`. |
| `url` | TEXT | NO | **UNIQUE**. Enlace web canónico directo a la nota. Impide duplicados (P1). |
| `resumen` | TEXT | NO | Síntesis redactada del contenido informativo. |
| `institucion_id` | INTEGER | SÍ | FOREIGN KEY REFERENCES `instituciones(id)` ON DELETE SET NULL. |
| `fuente_id` | INTEGER | SÍ | FOREIGN KEY REFERENCES `fuentes(id)` ON DELETE SET NULL. |
| `estado_verificacion`| TEXT | SÍ | CHECK ('Pendiente', 'Verificada', 'Observada'). Default: 'Pendiente'. |
| `es_demostrativo` | INTEGER | SÍ | 1 si es registro demostrativo didáctico de laboratorio; 0 si es noticia real. |
| `prioridad` | TEXT | SÍ | CHECK ('Alta', 'Media', 'Baja'). Default: 'Media'. |
| `impacto_regulatorio`| TEXT | SÍ | CHECK ('Alto', 'Medio', 'Informativo'). Default: 'Informativo'. |
| `palabras_clave` | TEXT | SÍ | Términos clave para el motor de detección de alertas tempranas. |
| `fecha_captura` | TEXT | SÍ | Fecha y hora en la que el analista ingresó el registro al OES. |

---

## 4. TABLA: `verificaciones`
Historial de control de calidad ética y supervisión humana aplicada a las noticias.

| Campo | Tipo de Dato | Nulo | Restricciones / Descripción |
|:------|:-------------|:----:|:----------------------------|
| `id` | INTEGER | NO | PRIMARY KEY AUTOINCREMENT. |
| `noticia_id` | INTEGER | NO | FOREIGN KEY REFERENCES `noticias(id)` ON DELETE CASCADE. |
| `estado` | TEXT | NO | CHECK ('Pendiente', 'Verificada', 'Observada'). Dictamen emitido. |
| `responsable` | TEXT | NO | Nombre y cargo del analista colegiado que emite el dictamen. |
| `fecha_verificacion` | TEXT | NO | Fecha en que se realizó la revisión técnica (`YYYY-MM-DD`). |
| `observaciones` | TEXT | SÍ | Justificación detallada del dictamen o motivos de observación. |
| `evidencia_url` | TEXT | SÍ | Enlace complementario que sustenta la verificación. |
| `criterio_evaluado` | TEXT | SÍ | Criterio metodológico aplicado en la revisión. |
| `fecha_registro` | TEXT | SÍ | Marca de tiempo del registro en la base de datos. |

---

## 5. TABLA: `auditoria`
Bitácora inmutable de seguridad que registra cada operación efectuada en el sistema.

| Campo | Tipo de Dato | Nulo | Restricciones / Descripción |
|:------|:-------------|:----:|:----------------------------|
| `id` | INTEGER | NO | PRIMARY KEY AUTOINCREMENT. |
| `tabla` | TEXT | NO | Nombre de la tabla afectada (`noticias`, `instituciones`, `fuentes`, etc.). |
| `operacion` | TEXT | NO | CHECK ('INSERT', 'UPDATE', 'DELETE', 'VERIFICACION', 'EXPORTACION', 'LOGIN'). |
| `registro_id` | INTEGER | SÍ | Identificador del registro afectado. |
| `detalles` | TEXT | NO | Descripción textual forense del cambio realizado. |
| `usuario` | TEXT | SÍ | Usuario responsable de la transacción (Default: 'admin'). |
| `ip_origen` | TEXT | SÍ | Dirección IP desde la que se originó la solicitud (Default: '127.0.0.1'). |
| `fecha_hora` | TEXT | SÍ | Marca temporal exacta de la transacción (Default: datetime('now', 'localtime')). |

