-- ====================================================================
-- SISTEMA OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)
-- ESQUEMA NORMALIZADO DE BASE DE DATOS (SQLite 3)
-- Integridad referencial activada con PRAGMA foreign_keys = ON;
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. TABLA DE INSTITUCIONES
CREATE TABLE IF NOT EXISTS instituciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK (tipo IN ('Universidad pública', 'Universidad privada', 'Ente rector', 'Instituto superior', 'Organismo internacional')),
    siglas TEXT,
    region TEXT DEFAULT 'Lima',
    estado_licenciamiento TEXT DEFAULT 'Licenciada' CHECK (estado_licenciamiento IN ('Licenciada', 'En proceso', 'Denegada', 'No aplica')),
    sitio_web TEXT,
    fecha_registro TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 2. TABLA DE FUENTES
CREATE TABLE IF NOT EXISTS fuentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo_fuente TEXT NOT NULL CHECK (tipo_fuente IN ('Portal institucional', 'Boletín oficial', 'Diario de circulación', 'Agencia estatal', 'Red social oficial')),
    url_base TEXT NOT NULL,
    confiabilidad TEXT DEFAULT 'Alta' CHECK (confiabilidad IN ('Alta', 'Media', 'En verificación')),
    fecha_registro TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 3. TABLA DE NOTICIAS (Compatible con Práctica 08 y normalizada)
CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    institucion TEXT NOT NULL,
    categoria TEXT NOT NULL,
    fuente TEXT NOT NULL,
    fecha TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    resumen TEXT NOT NULL,
    institucion_id INTEGER,
    fuente_id INTEGER,
    estado_verificacion TEXT DEFAULT 'Pendiente' CHECK (estado_verificacion IN ('Pendiente', 'Verificada', 'Observada')),
    es_demostrativo INTEGER DEFAULT 0,
    prioridad TEXT DEFAULT 'Media' CHECK (prioridad IN ('Alta', 'Media', 'Baja')),
    impacto_regulatorio TEXT DEFAULT 'Informativo' CHECK (impacto_regulatorio IN ('Alto', 'Medio', 'Informativo')),
    palabras_clave TEXT,
    fecha_captura TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (institucion_id) REFERENCES instituciones(id) ON DELETE SET NULL,
    FOREIGN KEY (fuente_id) REFERENCES fuentes(id) ON DELETE SET NULL
);

-- 4. TABLA DE VERIFICACIONES
CREATE TABLE IF NOT EXISTS verificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    noticia_id INTEGER NOT NULL,
    estado TEXT NOT NULL CHECK (estado IN ('Pendiente', 'Verificada', 'Observada')),
    responsable TEXT NOT NULL,
    fecha_verificacion TEXT NOT NULL,
    observaciones TEXT,
    evidencia_url TEXT,
    criterio_evaluado TEXT,
    fecha_registro TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (noticia_id) REFERENCES noticias(id) ON DELETE CASCADE
);

-- 5. TABLA DE AUDITORÍA
CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tabla TEXT NOT NULL,
    operacion TEXT NOT NULL CHECK (operacion IN ('INSERT', 'UPDATE', 'DELETE', 'VERIFICACION', 'EXPORTACION', 'LOGIN')),
    registro_id INTEGER,
    detalles TEXT NOT NULL,
    usuario TEXT DEFAULT 'admin',
    ip_origen TEXT DEFAULT '127.0.0.1',
    fecha_hora TEXT DEFAULT (datetime('now', 'localtime'))
);

-- ÍNDICES DE RENDIMIENTO Y BÚSQUEDA
CREATE INDEX IF NOT EXISTS idx_noticias_fecha ON noticias(fecha);
CREATE INDEX IF NOT EXISTS idx_noticias_categoria ON noticias(categoria);
CREATE INDEX IF NOT EXISTS idx_noticias_institucion ON noticias(institucion);
CREATE INDEX IF NOT EXISTS idx_noticias_estado ON noticias(estado_verificacion);
CREATE INDEX IF NOT EXISTS idx_verificaciones_noticia ON verificaciones(noticia_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha_hora);

-- TRIGGERS DE AUDITORÍA AUTOMÁTICA
CREATE TRIGGER IF NOT EXISTS trg_noticias_audit_insert
AFTER INSERT ON noticias
BEGIN
    INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
    VALUES ('noticias', 'INSERT', NEW.id, 'Registro de noticia: ' || NEW.titulo, 'sistema');
END;

CREATE TRIGGER IF NOT EXISTS trg_noticias_audit_update
AFTER UPDATE ON noticias
BEGIN
    INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
    VALUES ('noticias', 'UPDATE', NEW.id, 'Actualización de noticia: ' || NEW.titulo || ' (Estado: ' || NEW.estado_verificacion || ')', 'sistema');
END;

CREATE TRIGGER IF NOT EXISTS trg_noticias_audit_delete
AFTER DELETE ON noticias
BEGIN
    INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
    VALUES ('noticias', 'DELETE', OLD.id, 'Eliminación de noticia: ' || OLD.titulo, 'sistema');
END;

CREATE TRIGGER IF NOT EXISTS trg_verificacion_sync
AFTER INSERT ON verificaciones
BEGIN
    UPDATE noticias 
    SET estado_verificacion = NEW.estado 
    WHERE id = NEW.noticia_id;
    
    INSERT INTO auditoria (tabla, operacion, registro_id, detalles, usuario)
    VALUES ('verificaciones', 'VERIFICACION', NEW.noticia_id, 
            'Verificación aplicada [' || NEW.estado || '] por ' || NEW.responsable || '. Obs: ' || COALESCE(NEW.observaciones, 'Sin observaciones'), 
            NEW.responsable);
END;

