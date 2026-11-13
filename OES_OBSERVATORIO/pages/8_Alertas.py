"""
Página 8: Detección Temprana de Alertas Temáticas — Observatorio de Educación Superior (OES).
Monitoreo automático de palabras clave normativas y de alta sensibilidad política universitaria.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.noticias import obtener_noticias
from modules.alertas import generar_matriz_alertas, PALABRAS_CLAVE_ALERTAS, NIVELES_CRITICIDAD

st.set_page_config(page_title="Alertas Temáticas — OES", page_icon="🚨", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">🚨 Detección Temprana de Alertas Temáticas</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Monitoreo automatizado de 8 ejes clave: Licenciamiento, Acreditación, Calidad, Investigación, Becas, Presupuesto, Infraestructura y Educación Superior</p>
</div>
""", unsafe_allow_html=True)

df_noticias = obtener_noticias()

if df_noticias.empty:
    st.warning("No hay noticias en el observatorio para realizar el escaneo de alertas.")
    st.stop()

# Ejecutar escaneo automático
df_alertas, conteos = generar_matriz_alertas(df_noticias)

# 1. TARJETAS DE CONTEO POR CATEGORÍA DE ALERTA
st.subheader("📊 Frecuencia de Alertas por Eje Temático")

cols = st.columns(4)
categorias_lista = list(PALABRAS_CLAVE_ALERTAS.keys())

for idx, cat in enumerate(categorias_lista):
    col = cols[idx % 4]
    conteo = conteos.get(cat, 0)
    criticidad = NIVELES_CRITICIDAD.get(cat, "INFORMATIVO")
    col.metric(f"{cat}", f"{conteo} alertas", help=f"Nivel de Criticidad: {criticidad}")

st.markdown("---")

# 2. FILTRADO Y EXPLORACIÓN DETALLADA
st.subheader("📑 Coincidencias y Notificaciones Detectadas")

c_filtro1, c_filtro2 = st.columns(2)
with c_filtro1:
    filtro_cat = st.selectbox("Filtrar por eje de alerta:", ["Todos los ejes"] + categorias_lista)
with c_filtro2:
    filtro_crit = st.selectbox("Filtrar por criticidad:", ["Todas", "CRÍTICO", "ALTO", "MEDIO", "INFORMATIVO"])

df_mostrar = df_alertas.copy()

if not df_mostrar.empty:
    if filtro_cat != "Todos los ejes":
        df_mostrar = df_mostrar[df_mostrar["categoria_alerta"] == filtro_cat]
    if filtro_crit != "Todas":
        df_mostrar = df_mostrar[df_mostrar["criticidad"] == filtro_crit]

if df_mostrar.empty:
    st.info("No se encontraron coincidencias para los criterios seleccionados.")
else:
    st.write(f"Mostrando **{len(df_mostrar)}** alertas encontradas:")
    st.dataframe(
        df_mostrar[["fecha", "institucion", "categoria_alerta", "criticidad", "titulo", "terminos", "url"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn("Fuente Original", display_text="Ver Enlace ↗"),
            "criticidad": st.column_config.TextColumn("Nivel de Criticidad")
        }
    )

