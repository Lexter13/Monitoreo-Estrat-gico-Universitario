"""
Página 2: Gestión Integral de Noticias — Observatorio de Educación Superior (OES).
Permite registrar nuevas noticias, consultar con filtros combinados, editar y eliminar.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from modules.noticias import (
    registrar_noticia,
    obtener_noticias,
    obtener_noticia_por_id,
    actualizar_noticia,
    eliminar_noticia,
    exportar_noticias_csv
)
from modules.instituciones import listar_instituciones
from modules.fuentes import listar_fuentes
from modules.analisis_ia import consultar_analisis_ia

st.set_page_config(page_title="Gestión de Noticias — OES", page_icon="📰", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #1A365D 0%, #0F2344 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📰 Módulo de Gestión y Registro de Noticias</h2>
    <p style="margin:4px 0 0 0; color: #94A3B8; font-size: 13px;">Captura estructurada, validación de integridad y trazabilidad hacia fuentes oficiales</p>
</div>
""", unsafe_allow_html=True)

tab_consulta, tab_registro, tab_edicion = st.tabs(["🔍 Consultar Noticias", "➕ Registrar Noticia", "✏️ Editar / Eliminar"])

# -------------------------------------------------------------
# TAB 1: CONSULTA DE NOTICIAS
# -------------------------------------------------------------
with tab_consulta:
    st.subheader("Búsqueda y Exploración de Noticias")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        txt_buscar = st.text_input("Buscar por título, resumen o palabras clave", placeholder="Ej: licenciamiento, becas, UNMSM...")
    with col_f2:
        df_todas = obtener_noticias()
        cat_list = sorted(df_todas["categoria"].dropna().unique().tolist()) if not df_todas.empty else []
        filtro_cat = st.multiselect("Filtrar por Categoría", cat_list, default=[])
    with col_f3:
        orden = st.selectbox("Ordenar por fecha", ["Más recientes primero (DESC)", "Más antiguas primero (ASC)"])
        dir_orden = "DESC" if "DESC" in orden else "ASC"

    df_res = obtener_noticias(
        categorias=filtro_cat if filtro_cat else None,
        busqueda_texto=txt_buscar,
        orden_direccion=dir_orden
    )

    if df_res.empty:
        st.warning("⚠️ No se encontraron noticias que coincidan con los criterios de búsqueda.")
    else:
        st.info(f"Se encontraron **{len(df_res)}** registros coincidentes.")
        
        columnas_ver = [
            "id", "fecha", "institucion", "categoria", "titulo", "fuente",
            "estado_verificacion", "prioridad", "url"
        ]
        col_existentes = [c for c in columnas_ver if c in df_res.columns]
        
        st.dataframe(
            df_res[col_existentes],
            use_container_width=True,
            hide_index=True,
            column_config={
                "url": st.column_config.LinkColumn("Enlace Fuente", display_text="Abrir ↗"),
                "fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD")
            }
        )

        st.download_button(
            label="📥 Exportar Resultados a CSV",
            data=exportar_noticias_csv(df_res),
            file_name="oes_noticias_filtradas.csv",
            mime="text/csv"
        )

# -------------------------------------------------------------
# TAB 2: REGISTRO DE NOTICIA
# -------------------------------------------------------------
with tab_registro:
    st.subheader("Captura de Nueva Noticia Universitaria")
    st.caption("Todos los campos marcados con (*) son obligatorios. Se valida que la URL sea única y no se duplique.")

    # Listas auxiliares para sugerencia
    df_inst = listar_instituciones()
    inst_sugeridas = df_inst["nombre"].tolist() if not df_inst.empty else ["UNMSM", "PUCP", "PRONABEC", "SUNEDU", "MINEDU", "UNI"]
    
    df_fte = listar_fuentes()
    fte_sugeridas = df_fte["nombre"].tolist() if not df_fte.empty else ["Portal institucional", "Diario Oficial El Peruano", "Agencia Andina"]

    with st.form("form_registro_noticia", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            titulo = st.text_input("Título de la Noticia (*)", placeholder="Ej: SUNEDU aprueba disposiciones de calidad...")
            institucion = st.selectbox("Institución Asociada (*)", inst_sugeridas)
            categoria = st.selectbox(
                "Categoría (*)",
                ["Ente rector", "Universidad pública", "Universidad privada", "Instituto superior", "Regulación y Calidad", "Investigación e Innovación", "Becas y Bienestar"]
            )
            fuente = st.selectbox("Fuente Oficial (*)", fte_sugeridas)

        with c2:
            fecha = st.date_input("Fecha de Publicación (*)", datetime.now()).strftime("%Y-%m-%d")
            url = st.text_input("URL Directa de la Noticia (*) (Debe ser única)", placeholder="https://www.gob.pe/institucion/...")
            prioridad = st.selectbox("Nivel de Prioridad", ["Alta", "Media", "Baja"], index=1)
            impacto = st.selectbox("Impacto Regulatorio", ["Alto", "Medio", "Informativo"], index=2)

        resumen = st.text_area("Resumen Redactado de la Noticia (*)", placeholder="Redacte una síntesis verificada del contenido...", height=100)
        palabras_clave = st.text_input("Palabras clave (separadas por coma)", placeholder="Ej: licenciamiento, acreditacion, presupuesto, investigacion")

        btn_enviar = st.form_submit_button("💾 Guardar y Validar Noticia")

    if btn_enviar:
        exito, mensaje, nuevo_id = registrar_noticia(
            titulo=titulo,
            institucion=institucion,
            categoria=categoria,
            fuente=fuente,
            fecha=fecha,
            url=url,
            resumen=resumen,
            prioridad=prioridad,
            impacto_regulatorio=impacto,
            palabras_clave=palabras_clave,
            es_demostrativo=0,
            usuario="analista_oes"
        )
        if exito:
            st.success(f"✅ {mensaje} (ID Asignado: #{nuevo_id})")
            
            # Análisis asistido por reglas inmediato
            st.markdown("#### 🤖 Evaluación Automática Inicial (PLN por Reglas)")
            analisis = consultar_analisis_ia(titulo, resumen, institucion)
            st.write(f"**Tono Detectado:** {analisis['tono_evaluado']} — {analisis['explicacion_tono']}")
            st.write(f"**Impacto Estimado:** {analisis['impacto_estimado']}")
            st.write(f"**Etiquetas Sugeridas:** {' '.join(analisis['tags_sugeridos'])}")
        else:
            st.error(f"❌ Error al registrar: {mensaje}")

# -------------------------------------------------------------
# TAB 3: EDICIÓN Y ELIMINACIÓN
# -------------------------------------------------------------
with tab_edicion:
    st.subheader("Modificación o Retiro de Registros")
    df_actual = obtener_noticias()
    
    if df_actual.empty:
        st.info("No hay noticias registradas para editar.")
    else:
        opciones_noticias = {f"#{row['id']} - {row['titulo'][:60]}...": row['id'] for _, row in df_actual.iterrows()}
        seleccion_label = st.selectbox("Seleccione la noticia a gestionar:", list(opciones_noticias.keys()))
        noticia_id = opciones_noticias[seleccion_label]
        
        datos_noticia = obtener_noticia_por_id(noticia_id)
        
        if datos_noticia:
            with st.form("form_edicion_noticia"):
                e_titulo = st.text_input("Título", value=datos_noticia["titulo"])
                e_inst = st.text_input("Institución", value=datos_noticia["institucion"])
                e_cat = st.text_input("Categoría", value=datos_noticia["categoria"])
                e_fuente = st.text_input("Fuente", value=datos_noticia["fuente"])
                e_fecha = st.text_input("Fecha (YYYY-MM-DD)", value=datos_noticia["fecha"])
                e_url = st.text_input("URL", value=datos_noticia["url"])
                e_resumen = st.text_area("Resumen", value=datos_noticia["resumen"], height=100)
                e_kw = st.text_input("Palabras clave", value=datos_noticia.get("palabras_clave", "") or "")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    btn_actualizar = st.form_submit_button("🔄 Actualizar Cambios")
                with col_btn2:
                    btn_eliminar = st.form_submit_button("🗑️ Eliminar Noticia Definitivamente")

            if btn_actualizar:
                ok, msg = actualizar_noticia(
                    noticia_id=noticia_id,
                    titulo=e_titulo,
                    institucion=e_inst,
                    categoria=e_cat,
                    fuente=e_fuente,
                    fecha=e_fecha,
                    url=e_url,
                    resumen=e_resumen,
                    palabras_clave=e_kw,
                    usuario="editor_oes"
                )
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

            if btn_eliminar:
                ok_del, msg_del = eliminar_noticia(noticia_id, usuario="editor_oes")
                if ok_del:
                    st.warning(f"⚠️ {msg_del}")
                else:
                    st.error(f"❌ {msg_del}")

