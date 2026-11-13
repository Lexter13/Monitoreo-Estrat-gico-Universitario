"""
Página 7: Generador de Informes Oficiales en PDF — Observatorio de Educación Superior (OES).
Emite informes descargables con ReportLab respetando filtros, indicadores y observaciones éticas.
"""

from datetime import datetime
from pathlib import Path
import streamlit as st
import pandas as pd
from modules.noticias import obtener_noticias
from modules.reportes import generar_informe_pdf

st.set_page_config(page_title="Informes PDF — OES", page_icon="📄", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📄 Emisión de Informes Técnicos y Ejecutivos (PDF)</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Generación de documentos imprimibles con trazabilidad, indicadores y metodología</p>
</div>
""", unsafe_allow_html=True)

st.subheader("1. Configuración de Filtros para el Informe")
df_todos = obtener_noticias()

if df_todos.empty:
    st.warning("No hay noticias para generar informes.")
    st.stop()

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    cats = sorted(df_todos["categoria"].dropna().unique().tolist())
    filtro_cat = st.multiselect("Categorías a incluir", cats, default=cats)
with col_f2:
    insts = sorted(df_todos["institucion"].dropna().unique().tolist())
    filtro_inst = st.multiselect("Instituciones específicas (opcional)", insts, default=[])
with col_f3:
    filtro_est = st.multiselect("Estado de verificación", ["Verificada", "Pendiente", "Observada"], default=["Verificada", "Pendiente", "Observada"])

titulo_personalizado = st.text_input("Título del Informe Oficial", value="INFORME DE MONITOREO INSTITUCIONAL Y REGULATORIO")

# Aplicar filtros
df_reporte = obtener_noticias(
    categorias=filtro_cat if filtro_cat else None,
    instituciones=filtro_inst if filtro_inst else None,
    estados_verificacion=filtro_est if filtro_est else None
)

st.info(f"📊 Registros seleccionados para el informe: **{len(df_reporte)} noticias**.")

# Vista previa de los registros a incluir
with st.expander("👁️ Vista Previa de Registros a Incluir", expanded=False):
    st.dataframe(df_reporte[["fecha", "institucion", "categoria", "titulo", "fuente", "estado_verificacion"]], use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("2. Generación y Descarga del Documento")

col_btn, col_info = st.columns([1, 2])

with col_btn:
    btn_generar = st.button("🔨 Compilar y Generar PDF Oficial", type="primary")

with col_info:
    st.caption("ℹ️ El documento se compila usando ReportLab incorporando encabezado institucional, indicadores clave, tabla de registros con trazabilidad de URL y delimitación metodológica.")

if btn_generar:
    with st.spinner("Compilando documento PDF..."):
        txt_filtros = f"Categorías: {len(filtro_cat)} seleccionadas | Estados: {', '.join(filtro_est)}"
        pdf_bytes = generar_informe_pdf(
            df_filtrado=df_reporte,
            titulo_informe=titulo_personalizado,
            filtros_aplicados_texto=txt_filtros
        )
        
        nombre_archivo = f"OES_Informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        st.success("✅ Informe PDF generado exitosamente.")
        st.download_button(
            label="📥 Descargar Informe PDF Ahora",
            data=pdf_bytes,
            file_name=nombre_archivo,
            mime="application/pdf"
        )

