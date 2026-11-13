"""
Página 1: Dashboard Ejecutivo Interactivo — Observatorio de Educación Superior (OES).
Visualiza métricas en tiempo real, gráficos Plotly interactivos y filtros dinámicos.
"""

import streamlit as st
import pandas as pd
from modules.noticias import obtener_noticias, exportar_noticias_csv
from modules.indicadores import (
    calcular_metricas_globales,
    grafico_distribucion_categorias,
    grafico_evolucion_temporal,
    grafico_estados_verificacion,
    grafico_top_instituciones
)

st.set_page_config(page_title="Dashboard Ejecutivo — OES", page_icon="📊", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📊 Tablero de Monitoreo Estratégico Universitario</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Supervisión en tiempo real de novedades regulatorias, institucionales y académicas</p>
</div>
""", unsafe_allow_html=True)

# Filtros Dinámicos en Barra Lateral
st.sidebar.header("🎯 Filtros del Dashboard")

df_base = obtener_noticias()

if df_base.empty:
    st.warning("No hay información registrada en el observatorio. Ejecute `preparar_datos.py`.")
    st.stop()

# Opciones de filtros
categorias_disponibles = sorted(df_base["categoria"].dropna().unique().tolist())
instituciones_disponibles = sorted(df_base["institucion"].dropna().unique().tolist())
estados_disponibles = ["Verificada", "Pendiente", "Observada"]

sel_categorias = st.sidebar.multiselect("Categorías Temáticas", categorias_disponibles, default=categorias_disponibles)
sel_instituciones = st.sidebar.multiselect("Instituciones", instituciones_disponibles, default=[])
sel_estados = st.sidebar.multiselect("Estado de Verificación", estados_disponibles, default=estados_disponibles)
busqueda = st.sidebar.text_input("Búsqueda textual (título o resumen)")

# Obtener datos filtrados
df_filtrado = obtener_noticias(
    categorias=sel_categorias if sel_categorias else None,
    instituciones=sel_instituciones if sel_instituciones else None,
    estados_verificacion=sel_estados if sel_estados else None,
    busqueda_texto=busqueda
)

# Cálculo de KPIs
kpis = calcular_metricas_globales(df_filtrado)

# 1. TARJETAS DE INDICADORES (KPIs)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📰 Total Noticias", kpis["total_noticias"])
k2.metric("🏛️ Instituciones", kpis["total_instituciones"])
k3.metric("🏷️ Categorías", kpis["total_categorias"])
k4.metric("✅ % Verificadas", f"{kpis['porcentaje_verificadas']}%")
k5.metric("⚠️ Alto Impacto", f"{kpis['tasa_impacto_alto']}%")

st.markdown("---")

if df_filtrado.empty:
    st.info("No se encontraron registros que coincidan con la combinación de filtros seleccionada.")
    st.stop()

# 2. FILA DE GRÁFICOS INTERACTIVOS (PLOTLY)
g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(grafico_distribucion_categorias(df_filtrado), use_container_width=True)

with g2:
    st.plotly_chart(grafico_estados_verificacion(df_filtrado), use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.plotly_chart(grafico_evolucion_temporal(df_filtrado), use_container_width=True)

with g4:
    st.plotly_chart(grafico_top_instituciones(df_filtrado), use_container_width=True)

st.markdown("---")

# 3. TABLA DE NOTICIAS RECIENTES CON ESTADO
st.subheader("📑 Registros Detallados Bajo Filtro")

columnas_ver = [
    col for col in [
        "fecha", "institucion", "categoria", "titulo", "fuente",
        "estado_verificacion", "prioridad", "url"
    ] if col in df_filtrado.columns
]

st.dataframe(
    df_filtrado[columnas_ver],
    use_container_width=True,
    hide_index=True,
    column_config={
        "url": st.column_config.LinkColumn("Enlace Original", display_text="Ver Enlace ↗"),
        "estado_verificacion": st.column_config.TextColumn("Estado Ético")
    }
)

# Botón de Descarga
csv_bytes = exportar_noticias_csv(df_filtrado)
st.download_button(
    label="📥 Descargar Dataset Filtrado (CSV)",
    data=csv_bytes,
    file_name="oes_dashboard_filtrado.csv",
    mime="text/csv"
)

