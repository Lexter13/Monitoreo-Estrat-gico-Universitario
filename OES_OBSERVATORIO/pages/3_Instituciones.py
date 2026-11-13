"""
Página 3: Directorio de Instituciones — Observatorio de Educación Superior (OES).
Mantiene el registro maestro de universidades públicas, privadas y entes rectores peruanos.
"""

import streamlit as st
import pandas as pd
from modules.instituciones import (
    listar_instituciones,
    registrar_institucion,
    actualizar_institucion,
    eliminar_institucion
)
from modules.noticias import obtener_noticias

st.set_page_config(page_title="Instituciones — OES", page_icon="🏛️", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">🏛️ Directorio Institucional de Educación Superior</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Catálogo normalizado de universidades públicas, privadas, entes rectores y sedes</p>
</div>
""", unsafe_allow_html=True)

df_inst = listar_instituciones()

# Métricas rápidas
m1, m2, m3, m4 = st.columns(4)
m1.metric("🏛️ Total Instituciones", len(df_inst))
pub_cnt = len(df_inst[df_inst["tipo"] == "Universidad pública"]) if not df_inst.empty else 0
priv_cnt = len(df_inst[df_inst["tipo"] == "Universidad privada"]) if not df_inst.empty else 0
rector_cnt = len(df_inst[df_inst["tipo"] == "Ente rector"]) if not df_inst.empty else 0

m2.metric("Públicas", pub_cnt)
m3.metric("Privadas", priv_cnt)
m4.metric("Entes Rectores", rector_cnt)

st.markdown("---")

tab_dir, tab_nueva = st.tabs(["📋 Catálogo Institucional", "➕ Registrar Nueva Institución"])

with tab_dir:
    st.subheader("Entidades en Vigilancia")
    
    if df_inst.empty:
        st.warning("No hay instituciones registradas en el catálogo.")
    else:
        st.dataframe(
            df_inst[["nombre", "tipo", "siglas", "region", "estado_licenciamiento", "total_noticias", "sitio_web"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "sitio_web": st.column_config.LinkColumn("Sitio Web", display_text="Visitar Portal ↗"),
                "total_noticias": st.column_config.NumberColumn("Noticias Asociadas")
            }
        )

with tab_nueva:
    st.subheader("Añadir Institución al Directorio")
    with st.form("form_nueva_inst"):
        c1, c2 = st.columns(2)
        with c1:
            nombre = st.text_input("Nombre de la Institución (*)", placeholder="Ej: Universidad Nacional de Trujillo")
            tipo = st.selectbox("Tipo de Entidad (*)", [
                "Universidad pública", "Universidad privada", "Ente rector", "Instituto superior", "Organismo internacional"
            ])
            siglas = st.text_input("Siglas", placeholder="Ej: UNT")
        with c2:
            region = st.text_input("Región / Departamento", value="Lima")
            licenciamiento = st.selectbox("Estado de Licenciamiento", ["Licenciada", "En proceso", "Denegada", "No aplica"])
            sitio_web = st.text_input("Sitio Web Oficial", placeholder="https://www.untumbes.edu.pe/")

        btn_guardar = st.form_submit_button("💾 Guardar Institución")

    if btn_guardar:
        ok, msg = registrar_institucion(
            nombre=nombre,
            tipo=tipo,
            siglas=siglas,
            region=region,
            estado_licenciamiento=licenciamiento,
            sitio_web=sitio_web,
            usuario="admin_institucional"
        )
        if ok:
            st.success(f"✅ {msg}")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

