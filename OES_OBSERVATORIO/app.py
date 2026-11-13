"""
Observatorio de Educación Superior (OES) — Prototipo Académico y Profesional
Práctica Guiada N.° 08 — Construcción de un Observatorio de Educación Superior
Ingeniería de Sistemas — Versión 2.0 con Arquitectura Normalizada
"""

import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# Configuración de página institucional
st.set_page_config(
    page_title="OES Académico — Observatorio de Educación Superior",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Resolución de base de datos resiliente (raíz o carpeta database)
BASE_DIR = Path(__file__).resolve().parent
DB_ROOT = BASE_DIR / "oes.db"
DB_DATA = BASE_DIR / "database" / "oes.db"

if DB_DATA.exists():
    DB = DB_DATA
elif DB_ROOT.exists():
    DB = DB_ROOT
else:
    # Auto-inicialización para garantizar que nunca falle en el primer arranque
    try:
        from preparar_datos import preparar_datos
        preparar_datos(DB_ROOT)
        DB = DB_ROOT
    except Exception:
        DB = DB_ROOT

# Inyección de estilos CSS si existe
CSS_PATH = BASE_DIR / "assets" / "styles.css"
if CSS_PATH.exists():
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Encabezado Institucional
st.markdown("""
<div class="oes-header-container">
    <h1 class="oes-header-title">🎓 Observatorio de Educación Superior — Prototipo Académico</h1>
    <p class="oes-header-subtitle">Monitoreo Estratégico, Trazabilidad de Fuentes y Vigilancia Regulatoria Universitaria</p>
    <span class="oes-header-tag">Versión 2.0 • Ingeniería de Sistemas</span>
</div>
""", unsafe_allow_html=True)

st.caption("📌 Registros didácticos y verificados; confirmar fuentes primarias antes de uso institucional.")

# Carga de datos
if not DB.exists():
    st.warning("⚠️ No se encontró la base de datos. Ejecute `python preparar_datos.py` o inicialice el sistema.")
    st.stop()

with sqlite3.connect(DB) as con:
    df = pd.read_sql_query("SELECT * FROM noticias ORDER BY fecha DESC", con)

if df.empty:
    st.warning("No hay noticias en la base de datos. Ejecute preparar_datos.py para cargar los registros demostrativos.")
    st.stop()

# Barra lateral de filtros obligatorios del laboratorio
st.sidebar.markdown("### 🔍 Filtros de Consulta")
categorias = sorted(df["categoria"].unique().tolist())
seleccion = st.sidebar.multiselect("Categoría", categorias, default=categorias)

busqueda = st.sidebar.text_input("Buscar título o institución")

# Filtro de ámbito de datos (mejora para distinguir datos didácticos de reales)
tipo_vista = st.sidebar.radio(
    "Conjunto de datos:",
    ["Todas las noticias", "Solo verificadas", "Solo datos demostrativos (Lab)"],
    index=0
)

# Aplicar filtros
filtrado = df[df["categoria"].isin(seleccion)].copy()

if tipo_vista == "Solo verificadas" and "estado_verificacion" in filtrado.columns:
    filtrado = filtrado[filtrado["estado_verificacion"] == "Verificada"]
elif tipo_vista == "Solo datos demostrativos (Lab)" and "es_demostrativo" in filtrado.columns:
    filtrado = filtrado[filtrado["es_demostrativo"] == 1]

if busqueda.strip():
    patron = busqueda.strip()
    mascara = (
        filtrado["titulo"].str.contains(patron, case=False, regex=False, na=False) |
        filtrado["institucion"].str.contains(patron, case=False, regex=False, na=False)
    )
    filtrado = filtrado[mascara]

# Métricas principales obligatorias del laboratorio
c1, c2, c3, c4 = st.columns(4)
c1.metric("Noticias", len(filtrado))
c2.metric("Instituciones", filtrado["institucion"].nunique() if not filtrado.empty else 0)
c3.metric("Categorías", filtrado["categoria"].nunique() if not filtrado.empty else 0)

if "estado_verificacion" in filtrado.columns and not filtrado.empty:
    pct_verif = round((len(filtrado[filtrado["estado_verificacion"] == "Verificada"]) / len(filtrado)) * 100, 1)
    c4.metric("% Verificadas", f"{pct_verif}%")
else:
    c4.metric("Cobertura", "100%")

st.markdown("---")

# Visualizaciones obligatorias y mejoradas
col_grafico, col_info = st.columns([2, 1])

with col_grafico:
    st.subheader("📊 Distribución por categoría")
    if not filtrado.empty:
        st.bar_chart(filtrado["categoria"].value_counts())
    else:
        st.info("ℹ️ No hay resultados con esos filtros para generar el gráfico.")

with col_info:
    st.subheader("🧭 Navegación de Módulos")
    st.markdown("""
    Explore los módulos especializados en el menú lateral:
    - **1_Dashboard:** Tableros analíticos interactivos Plotly.
    - **2_Noticias:** Registro, edición y búsqueda con URL única.
    - **3_Instituciones:** Directorio de universidades y entes rectores.
    - **4_Fuentes:** Registro y auditoría de fuentes oficiales.
    - **5_Verificacion:** Control de calidad ético y validación humana.
    - **6_Indicadores:** KPIs y análisis de tendencias.
    - **7_Reportes:** Generador oficial de informes ejecutivos en PDF.
    - **8_Alertas:** Detección automática de temas sensibles.
    - **9_Auditoria:** Bitácora inmutable de operaciones.
    *(La documentación metodológica, arquitectura y reflexión ética se encuentran en la carpeta `documentation/`).*
    """)

# Tabla de noticias registradas con enlace directo y trazabilidad
st.subheader("📋 Noticias registradas")

if not filtrado.empty:
    columnas_mostrar = [col for col in ["fecha", "institucion", "categoria", "titulo", "fuente", "url"] if col in filtrado.columns]
    
    st.dataframe(
        filtrado[columnas_mostrar],
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn("Enlace Fuente Directa", display_text="Abrir Fuente ↗"),
            "fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD")
        }
    )
    
    # Exportación en CSV compatible con Excel (UTF-8 con BOM)
    csv_bytes = filtrado.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 Exportar CSV (Excel)",
        data=csv_bytes,
        file_name="oes_resultados.csv",
        mime="text/csv",
        help="Descargar los registros filtrados en formato compatible con Microsoft Excel"
    )
else:
    st.info("ℹ️ No hay noticias que coincidan con los criterios de búsqueda seleccionados.")

