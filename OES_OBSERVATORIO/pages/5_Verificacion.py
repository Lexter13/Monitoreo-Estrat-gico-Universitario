"""
Página 5: Verificación y Control Ético de Noticias — Observatorio de Educación Superior (OES).
Implementa la supervisión humana obligatoria, estados éticos e historial de trazabilidad.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from modules.noticias import obtener_noticias, obtener_noticia_por_id
from modules.verificaciones import (
    registrar_verificacion,
    obtener_historial_verificaciones,
    resumen_metricas_verificacion
)

st.set_page_config(page_title="Verificación de Noticias — OES", page_icon="🛡️", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">🛡️ Módulo de Verificación y Control de Calidad Ética</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Validación humana obligatoria antes de incorporar novedades a reportes decisorios</p>
</div>
""", unsafe_allow_html=True)

# Métricas de verificación
stats = resumen_metricas_verificacion()
k1, k2, k3, k4 = st.columns(4)
k1.metric("📰 Noticias Totales", stats["total"])
k2.metric("✅ Verificadas", stats["verificadas"])
k3.metric("⏳ Pendientes", stats["pendientes"])
k4.metric("⚠️ Observadas", stats["observadas"])

st.progress(stats["porcentaje_verificadas"] / 100.0, text=f"Tasa de Verificación: {stats['porcentaje_verificadas']}%")

st.markdown("---")

tab_revisar, tab_historial = st.tabs(["✍️ Aplicar Verificación a Noticia", "📜 Historial de Revisiones"])

with tab_revisar:
    st.subheader("Auditoría y Cambio de Estado de una Noticia")
    
    # Filtro para encontrar la noticia a revisar
    filtro_estado = st.radio("Listar noticias según estado actual:", ["Todas", "Pendiente", "Observada", "Verificada"], horizontal=True)
    
    estados_param = [filtro_estado] if filtro_estado != "Todas" else None
    df_lista = obtener_noticias(estados_verificacion=estados_param)
    
    if df_lista.empty:
        st.info("No hay noticias con el estado seleccionado.")
    else:
        opciones = {f"#{r['id']} [{r['estado_verificacion']}] - {r['institucion']}: {r['titulo'][:65]}...": r['id'] for _, r in df_lista.iterrows()}
        seleccion = st.selectbox("Seleccione la noticia a auditar:", list(opciones.keys()))
        noticia_id = opciones[seleccion]
        
        datos = obtener_noticia_por_id(noticia_id)
        
        if datos:
            # Mostrar ficha de la noticia
            with st.expander("👁️ Ver Ficha Completa de la Noticia", expanded=True):
                st.write(f"**Título:** {datos['titulo']}")
                st.write(f"**Institución:** {datos['institucion']} | **Categoría:** {datos['categoria']}")
                st.write(f"**Fecha:** {datos['fecha']} | **Fuente:** {datos['fuente']}")
                st.markdown(f"**URL:** [{datos['url']}]({datos['url']})")
                st.write(f"**Resumen Original:** {datos['resumen']}")
                if datos.get("es_demostrativo") == 1:
                    st.warning("⚠️ Esta noticia es un registro didáctico demostrativo de laboratorio.")
            
            # Formulario de verificación humana
            with st.form("form_verificacion"):
                st.markdown("#### Dictamen del Analista")
                c_v1, c_v2 = st.columns(2)
                with c_v1:
                    nuevo_estado = st.selectbox(
                        "Nuevo Estado de Verificación (*)",
                        ["Verificada", "Observada", "Pendiente"],
                        index=0 if datos["estado_verificacion"] == "Verificada" else 1 if datos["estado_verificacion"] == "Observada" else 0
                    )
                    responsable = st.text_input("Nombre del Analista / Responsable (*)", value="Ing. Carlos Mendoza (Analista OES)")
                with c_v2:
                    criterio = st.selectbox("Criterio Metodológico Aplicado", [
                        "Trazabilidad de fuente primaria gubernamental",
                        "Resolución oficial cotejada en El Peruano",
                        "Comunicado institucional verificado",
                        "Contraste con informe técnico externo",
                        "Dato didáctico / pendiente de confirmación"
                    ])
                    evidencia = st.text_input("URL de Evidencia o Soporte Adicional", placeholder="https://...")

                observaciones = st.text_area("Observaciones Técnicas y Justificación del Dictamen (*)", height=80, placeholder="Detalle por qué se aprueba o se observa este registro...")

                btn_verificar = st.form_submit_button("🛡️ Registrar Verificación Ética")

            if btn_verificar:
                ok, msg = registrar_verificacion(
                    noticia_id=noticia_id,
                    estado=nuevo_estado,
                    responsable=responsable,
                    observaciones=observaciones,
                    criterio_evaluado=criterio,
                    evidencia_url=evidencia,
                    usuario=responsable.split()[0]
                )
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

with tab_historial:
    st.subheader("Bitácora de Verificaciones Realizadas")
    df_noticias = obtener_noticias()
    
    if df_noticias.empty:
        st.info("Sin registros.")
    else:
        opciones_h = {f"#{r['id']} - {r['titulo'][:60]}...": r['id'] for _, r in df_noticias.iterrows()}
        sel_h = st.selectbox("Seleccione noticia para ver su historial de control:", list(opciones_h.keys()), key="sel_hist")
        nid_h = opciones_h[sel_h]
        
        historial = obtener_historial_verificaciones(nid_h)
        if historial:
            st.table(pd.DataFrame(historial)[["fecha_verificacion", "estado", "responsable", "criterio_evaluado", "observaciones"]])
        else:
            st.info("Esta noticia aún no cuenta con dictámenes de verificación registrados.")

