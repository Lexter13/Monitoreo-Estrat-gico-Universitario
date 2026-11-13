"""
Página 4: Fuentes Oficiales Monitoreadas — Observatorio de Educación Superior (OES).
Garantiza la trazabilidad hacia los orígenes de información institucional y legal.
"""

import streamlit as st
import pandas as pd
from modules.fuentes import (
    listar_fuentes,
    registrar_fuente,
    actualizar_fuente,
    eliminar_fuente
)

st.set_page_config(page_title="Fuentes Oficiales — OES", page_icon="📡", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📡 Fuentes Oficiales de Monitoreo</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Trazabilidad, confiabilidad y auditoría de portales gubernamentales y universitarios</p>
</div>
""", unsafe_allow_html=True)

df_fuentes = listar_fuentes()

# Métricas de fuentes
f1, f2, f3 = st.columns(3)
f1.metric("📡 Fuentes Monitoreadas", len(df_fuentes))
alta_cnt = len(df_fuentes[df_fuentes["confiabilidad"] == "Alta"]) if not df_fuentes.empty else 0
f2.metric("Confiabilidad Alta", alta_cnt)
med_cnt = len(df_fuentes[df_fuentes["confiabilidad"] == "Media"]) if not df_fuentes.empty else 0
f3.metric("Confiabilidad Media / En Revisión", med_cnt)

st.markdown("---")

tab1, tab2 = st.tabs(["📋 Catálogo de Fuentes", "➕ Registrar Nueva Fuente"])

with tab1:
    st.subheader("Directorio de Canales de Vigilancia")
    if df_fuentes.empty:
        st.warning("No hay fuentes registradas en el observatorio.")
    else:
        st.dataframe(
            df_fuentes[["nombre", "tipo_fuente", "url_base", "confiabilidad", "total_noticias"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "url_base": st.column_config.LinkColumn("Portal Base", display_text="Acceder ↗"),
                "total_noticias": st.column_config.NumberColumn("Noticias Emitidas")
            }
        )

with tab2:
    st.subheader("Incorporar Fuente de Información")
    with st.form("form_nueva_fuente"):
        nombre = st.text_input("Nombre de la Fuente (*)", placeholder="Ej: Diario Oficial El Peruano - Separata Especial")
        tipo_fte = st.selectbox("Tipo de Fuente (*)", [
            "Portal institucional", "Boletín oficial", "Diario de circulación", "Agencia estatal", "Red social oficial"
        ])
        url_base = st.text_input("URL Base Oficial (*)", placeholder="https://elperuano.pe/")
        confiabilidad = st.selectbox("Nivel de Confiabilidad Inicial", ["Alta", "Media", "En verificación"])

        btn_fte = st.form_submit_button("💾 Guardar Fuente")

    if btn_fte:
        ok, msg = registrar_fuente(
            nombre=nombre,
            tipo_fuente=tipo_fte,
            url_base=url_base,
            confiabilidad=confiabilidad,
            usuario="admin_fuentes"
        )
        if ok:
            st.success(f"✅ {msg}")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

