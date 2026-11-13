"""
Página 9: Bitácora de Auditoría del Sistema — Observatorio de Educación Superior (OES).
Trazabilidad completa de operaciones: inserciones, modificaciones, verificaciones y bajas.
"""

import streamlit as st
import pandas as pd
from modules.auditoria import consultar_auditoria, obtener_estadisticas_auditoria

st.set_page_config(page_title="Auditoría del Sistema — OES", page_icon="🕵️", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">🕵️ Bitácora y Registro Inmutable de Auditoría</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Supervisión forense de operaciones realizadas por los analistas y el sistema</p>
</div>
""", unsafe_allow_html=True)

# Estadísticas de auditoría
stats = obtener_estadisticas_auditoria()

c1, c2, c3 = st.columns(3)
c1.metric("Total de Operaciones Registradas", stats["total_operaciones"])
c2.metric("Usuarios Distintos", stats["usuarios_activos"])
c3.metric("Tipo Más Frecuente", max(stats["operaciones_por_tipo"], key=stats["operaciones_por_tipo"].get) if stats["operaciones_por_tipo"] else "N/A")

st.markdown("---")

# Filtros
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    sel_op = st.selectbox("Operación", ["Todas", "INSERT", "UPDATE", "DELETE", "VERIFICACION", "LOGIN"])
with col_f2:
    sel_tbl = st.selectbox("Tabla Auditada", ["Todas", "noticias", "instituciones", "fuentes", "verificaciones", "sistema"])
with col_f3:
    txt_user = st.text_input("Filtrar por Usuario", placeholder="Ej: analista, admin...")

df_audit = consultar_auditoria(
    tabla=sel_tbl,
    operacion=sel_op,
    usuario=txt_user,
    limite=200
)

st.subheader("📋 Registro Cronológico de Operaciones")

if df_audit.empty:
    st.info("No hay eventos registrados que coincidan con los filtros.")
else:
    st.dataframe(
        df_audit[["fecha_hora", "tabla", "operacion", "registro_id", "detalles", "usuario", "ip_origen"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "fecha_hora": st.column_config.DatetimeColumn("Marca Temporal", format="YYYY-MM-DD HH:mm:ss"),
            "operacion": st.column_config.TextColumn("Tipo de Operación"),
            "detalles": st.column_config.TextColumn("Descripción de la Acción", width="large")
        }
    )

