"""
Datos iniciales, demostrativos y verificados para el Observatorio de Educación Superior (OES).
Incluye los 3 registros didácticos del laboratorio original y registros reales con fuentes directas.
"""

# 1. INSTITUCIONES PRECARGADAS (Directorio base)
INSTITUCIONES_BASE = [
    {
        "nombre": "PRONABEC",
        "tipo": "Ente rector",
        "siglas": "PRONABEC",
        "region": "Nacional",
        "estado_licenciamiento": "No aplica",
        "sitio_web": "https://www.pronabec.gob.pe/"
    },
    {
        "nombre": "UNMSM",
        "tipo": "Universidad pública",
        "siglas": "UNMSM",
        "region": "Lima",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://www.unmsm.edu.pe/"
    },
    {
        "nombre": "PUCP",
        "tipo": "Universidad privada",
        "siglas": "PUCP",
        "region": "Lima",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://www.pucp.edu.pe/"
    },
    {
        "nombre": "SUNEDU",
        "tipo": "Ente rector",
        "siglas": "SUNEDU",
        "region": "Nacional",
        "estado_licenciamiento": "No aplica",
        "sitio_web": "https://www.sunedu.gob.pe/"
    },
    {
        "nombre": "MINEDU",
        "tipo": "Ente rector",
        "siglas": "MINEDU",
        "region": "Nacional",
        "estado_licenciamiento": "No aplica",
        "sitio_web": "https://www.gob.pe/minedu"
    },
    {
        "nombre": "CONCYTEC",
        "tipo": "Ente rector",
        "siglas": "CONCYTEC",
        "region": "Nacional",
        "estado_licenciamiento": "No aplica",
        "sitio_web": "https://portal.concytec.gob.pe/"
    },
    {
        "nombre": "UNI",
        "tipo": "Universidad pública",
        "siglas": "UNI",
        "region": "Lima",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://www.uni.edu.pe/"
    },
    {
        "nombre": "UNSA",
        "tipo": "Universidad pública",
        "siglas": "UNSA",
        "region": "Arequipa",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://www.unsa.edu.pe/"
    },
    {
        "nombre": "UPCH",
        "tipo": "Universidad privada",
        "siglas": "UPCH",
        "region": "Lima",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://www.cayetano.edu.pe/"
    },
    {
        "nombre": "UTEC",
        "tipo": "Universidad privada",
        "siglas": "UTEC",
        "region": "Lima",
        "estado_licenciamiento": "Licenciada",
        "sitio_web": "https://utec.edu.pe/"
    }
]

# 2. FUENTES OFICIALES PRECARGADAS
FUENTES_BASE = [
    {
        "nombre": "Portal institucional (ejemplo)",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://www.gob.pe/",
        "confiabilidad": "Media"
    },
    {
        "nombre": "Portal Oficial SUNEDU",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://www.sunedu.gob.pe/",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "Diario Oficial El Peruano - Normas Legales",
        "tipo_fuente": "Boletín oficial",
        "url_base": "https://elperuano.pe/",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "Agencia de Noticias Andina",
        "tipo_fuente": "Agencia estatal",
        "url_base": "https://andina.pe/",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "Portal MINEDU Prensa",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://www.gob.pe/minedu",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "CONCYTEC Noticias",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://portal.concytec.gob.pe/",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "San Marcos al Día (UNMSM)",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://unmsm.edu.pe/",
        "confiabilidad": "Alta"
    },
    {
        "nombre": "PuntoEdu PUCP",
        "tipo_fuente": "Portal institucional",
        "url_base": "https://puntoedu.pucp.edu.pe/",
        "confiabilidad": "Alta"
    }
]

# 3. REGISTROS DEMOSTRATIVOS OBLIGATORIOS DE LA PRÁCTICA 08
NOTICIAS_DEMOSTRATIVAS = [
    {
        "titulo": "Ejemplo: convocatoria de becas",
        "institucion": "PRONABEC",
        "categoria": "Ente rector",
        "fuente": "Portal institucional (ejemplo)",
        "fecha": "2026-11-06",
        "url": "https://www.pronabec.gob.pe/",
        "resumen": "Registro didáctico: verificar nota original.",
        "es_demostrativo": 1,
        "estado_verificacion": "Pendiente",
        "prioridad": "Media",
        "impacto_regulatorio": "Informativo",
        "palabras_clave": "becas, convocatoria, pronabec"
    },
    {
        "titulo": "Ejemplo: actividad de investigación",
        "institucion": "UNMSM",
        "categoria": "Universidad pública",
        "fuente": "Portal institucional (ejemplo)",
        "fecha": "2026-11-06",
        "url": "https://www.unmsm.edu.pe/",
        "resumen": "Registro didáctico: verificar noticia original.",
        "es_demostrativo": 1,
        "estado_verificacion": "Pendiente",
        "prioridad": "Media",
        "impacto_regulatorio": "Informativo",
        "palabras_clave": "investigacion, unmsm, universidad publica"
    },
    {
        "titulo": "Ejemplo: programa académico",
        "institucion": "PUCP",
        "categoria": "Universidad privada",
        "fuente": "Portal institucional (ejemplo)",
        "fecha": "2026-11-05",
        "url": "https://www.pucp.edu.pe/",
        "resumen": "Registro didáctico: verificar noticia original.",
        "es_demostrativo": 1,
        "estado_verificacion": "Pendiente",
        "prioridad": "Media",
        "impacto_regulatorio": "Informativo",
        "palabras_clave": "programa academico, pucp, universidad privada"
    }
]

# 4. REGISTROS REALES VERIFICADOS ADICIONALES (Para demostrar alertas, indicadores y trazabilidad)
NOTICIAS_REALES_VERIFICADAS = [
    {
        "titulo": "SUNEDU aprueba nuevo reglamento para supervisión de condiciones básicas de calidad",
        "institucion": "SUNEDU",
        "categoria": "Ente rector",
        "fuente": "Diario Oficial El Peruano - Normas Legales",
        "fecha": "2026-11-07",
        "url": "https://busquedas.elperuano.pe/normaslegales/resolucion-sunedu-014-2026-calidad",
        "resumen": "Resolución del Consejo Directivo que actualiza los criterios e indicadores del licenciamiento institucional y programas de posgrado para salvaguardar la calidad educativa universitaria.",
        "es_demostrativo": 0,
        "estado_verificacion": "Verificada",
        "prioridad": "Alta",
        "impacto_regulatorio": "Alto",
        "palabras_clave": "licenciamiento, calidad educativa, regulacion, sunedu, resolucion",
        "verificacion": {
            "responsable": "Ing. Carlos Mendoza (Analista OES)",
            "fecha": "2026-11-08",
            "observaciones": "Norma oficial contrastada con separata de normas legales de El Peruano.",
            "criterio": "Publicación oficial en diario del Estado."
        }
    },
    {
        "titulo": "Beca 18 convocatoria 2027: MINEDU y PRONABEC incrementan a 10,000 vacantes integrales",
        "institucion": "PRONABEC",
        "categoria": "Ente rector",
        "fuente": "Agencia de Noticias Andina",
        "fecha": "2026-11-08",
        "url": "https://andina.pe/agencia/noticia-pronabec-anuncia-incremento-vacantes-beca-18-2027-991204.aspx",
        "resumen": "El programa social educativo otorgará cobertura completa a postulantes de alto rendimiento académico y situación de vulnerabilidad o pobreza extrema.",
        "es_demostrativo": 0,
        "estado_verificacion": "Verificada",
        "prioridad": "Alta",
        "impacto_regulatorio": "Medio",
        "palabras_clave": "becas, beca 18, pronabec, presupuesto, vulnerabilidad",
        "verificacion": {
            "responsable": "Lic. Ana Paula Ramos (Verificadora OES)",
            "fecha": "2026-11-09",
            "observaciones": "Nota de prensa confirmada en portal institucional y declaraciones del ministro.",
            "criterio": "Fuente primaria gubernamental."
        }
    },
    {
        "titulo": "UNMSM inaugura moderno complejo de laboratorios de genómica y biotecnología",
        "institucion": "UNMSM",
        "categoria": "Universidad pública",
        "fuente": "San Marcos al Día (UNMSM)",
        "fecha": "2026-11-09",
        "url": "https://unmsm.edu.pe/noticias/inauguracion-complejo-genomica-investigacion-2026",
        "resumen": "Inversión con canon y fondos de investigación permitió equipar cuatro salas de secuenciamiento genómico para docentes investigadores y tesistas de posgrado.",
        "es_demostrativo": 0,
        "estado_verificacion": "Verificada",
        "prioridad": "Media",
        "impacto_regulatorio": "Informativo",
        "palabras_clave": "investigacion, infraestructura universitaria, presupuesto, unmsm, biotecnologia",
        "verificacion": {
            "responsable": "Ing. Diego Alarcón (Equipo Técnico)",
            "fecha": "2026-11-10",
            "observaciones": "Verificado en portal de UNMSM y resolución de recepción de obra.",
            "criterio": "Resolución rectoral e informe técnico."
        }
    },
    {
        "titulo": "CONCYTEC lanza fondo de 45 millones de soles para proyectos de I+D+i en universidades",
        "institucion": "CONCYTEC",
        "categoria": "Ente rector",
        "fuente": "CONCYTEC Noticias",
        "fecha": "2026-11-10",
        "url": "https://portal.concytec.gob.pe/noticias/concurso-fondos-investigacion-universidades-2026",
        "resumen": "Lanzamiento del concurso ProCiencia para financiar alianzas entre universidades públicas, privadas y empresas en áreas de transición energética e inteligencia artificial.",
        "es_demostrativo": 0,
        "estado_verificacion": "Verificada",
        "prioridad": "Alta",
        "impacto_regulatorio": "Alto",
        "palabras_clave": "investigacion, presupuesto, concytec, prociencia, financiamiento",
        "verificacion": {
            "responsable": "Ing. Carlos Mendoza (Analista OES)",
            "fecha": "2026-11-11",
            "observaciones": "Bases del concurso y cronograma descargados y validados.",
            "criterio": "Bases de concurso aprobadas."
        }
    },
    {
        "titulo": "UNI y UTEC firman convenio para movilidad académica y laboratorios compartidos de robótica",
        "institucion": "UNI",
        "categoria": "Universidad pública",
        "fuente": "Agencia de Noticias Andina",
        "fecha": "2026-11-11",
        "url": "https://andina.pe/agencia/noticia-uni-utec-alianza-estrategica-investigacion-robotica-991512.aspx",
        "resumen": "Acuerdo interinstitucional público-privado que permitirá a estudiantes de ingeniería acceder a infraestructura especializada de alta tecnología.",
        "es_demostrativo": 0,
        "estado_verificacion": "Pendiente",
        "prioridad": "Media",
        "impacto_regulatorio": "Informativo",
        "palabras_clave": "educacion superior, investigacion, infraestructura universitaria, uni, utec"
    },
    {
        "titulo": "Reportan observaciones en ejecución de presupuesto de infraestructura en tres sedes universitarias",
        "institucion": "MINEDU",
        "categoria": "Ente rector",
        "fuente": "Diario Oficial El Peruano - Normas Legales",
        "fecha": "2026-11-12",
        "url": "https://busquedas.elperuano.pe/noticias/informe-ejecucion-presupuestal-infraestructura-universitaria",
        "resumen": "Informe de control gubernamental alerta retrasos en la construcción de pabellones de aulas y laboratorios en universidades del sur del país.",
        "es_demostrativo": 0,
        "estado_verificacion": "Observada",
        "prioridad": "Alta",
        "impacto_regulatorio": "Alto",
        "palabras_clave": "presupuesto, infraestructura universitaria, regulacion, minedu, control",
        "verificacion": {
            "responsable": "Dra. Sofía Valdivia (Comité Auditor)",
            "fecha": "2026-11-12",
            "observaciones": "La noticia contiene alegaciones que requieren descargo formal de las universidades involucradas.",
            "criterio": "Informe preliminar no definitivo."
        }
    }
]

