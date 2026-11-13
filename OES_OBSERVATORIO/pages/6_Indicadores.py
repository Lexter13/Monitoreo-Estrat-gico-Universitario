"""
Página 6: Indicadores y Métricas Estratégicas — Observatorio de Educación Superior (OES).
Análisis cuantitativo avanzado de cobertura, impacto regulatorio y tendencias.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.noticias import obtener_noticias
from modules.indicadores import (
    calcular_metricas_globales,
    grafico_distribucion_categorias,
    grafico_evolucion_temporal,
    grafico_estados_verificacion,
    grafico_top_instituciones
)

st.set_page_config(page_title="Indicadores y KPIs — OES", page_icon="📈", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📈 Tablero de Indicadores y Métricas de Vigilancia</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Análisis cuantitativo, tendencias temporales y cobertura regulatoria universitaria</p>
</div>
""", unsafe_allow_html=True)

# Filtros para los indicadores
st.sidebar.header("⚙️ Segmentación de Indicadores")
df_all = obtener_noticias()

if df_all.empty:
    st.warning("No hay datos disponibles para calcular indicadores.")
    st.stop()

cats = sorted(df_all["categoria"].dropna().unique().tolist())
sel_cat = st.sidebar.multiselect("Categorías", cats, default=cats)

df_ind = obtener_noticias(categorias=sel_cat if sel_cat else None)
metricas = calcular_metricas_globales(df_ind)

# KPIs Superiores
c1, c2, c3, c4 = st.columns(4)
c1.metric("Volumen Analizado", metricas["total_noticias"])
c2.metric("Instituciones Distintas", metricas["total_instituciones"])
c3.metric("Tasa de Verificación", f"{metricas['porcentaje_verificadas']}%")
c4.metric("Alto Impacto Regulatorio", f"{metricas['tasa_impacto_alto']}%")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_distribucion_categorias(df_ind), use_container_width=True)

with col2:
    st.plotly_chart(grafico_evolucion_temporal(df_ind), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(grafico_estados_verificacion(df_ind), use_container_width=True)

with col4:
    # Gráfico de Impacto Regulatorio
    if not df_ind.empty and "impacto_regulatorio" in df_ind.columns:
        fig_imp = px.pie(
            df_ind["impacto_regulatorio"].value_counts().reset_index(),
            names="impacto_regulatorio",
            values="count",
            hole=0.4,
            title="<b>Distribución por Nivel de Impacto Regulatorio</b>",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_imp.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.info("Sin datos de impacto.")

st.markdown("---")

# Tabla de Resumen Estadístico por Categoría
st.subheader("📊 Tabla Resumen Consolidada por Categoría")
if not df_ind.empty:
    resumen_cat = df_ind.groupby("categoria").agg(
        Total_Noticias=("id", "count"),
        Instituciones=("institucion", "nunique"),
        Verificadas=("estado_verificacion", lambda x: (x == "Verificada").sum()),
        Alto_Impacto=("impacto_regulatorio", lambda x: (x == "Alto").sum())
    ).reset_index()
    
    st.dataframe(resumen_cat, use_container_width=True, hide_index=True)

