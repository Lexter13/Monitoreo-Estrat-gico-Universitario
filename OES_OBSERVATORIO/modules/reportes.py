"""
Módulo de Generación de Informes Ejecutivos en PDF con ReportLab para el OES.
Sección 6.5: Genera documentos oficiales descargables respetando los filtros activos.
"""

import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)


def generar_informe_pdf(
    df_filtrado: pd.DataFrame,
    titulo_informe: str = "INFORME DE MONITOREO INSTITUCIONAL Y REGULATORIO",
    filtros_aplicados_texto: str = "Todos los registros",
    ruta_guardado: Optional[Path] = None
) -> bytes:
    """
    Genera un informe PDF profesional con ReportLab conteniendo:
    - Encabezado institucional OES
    - Metadatos de emisión
    - Indicadores cuantitativos clave
    - Tabla detallada de registros filtrados con trazabilidad
    - Desglose de fuentes consultadas
    - Observaciones metodológicas y éticas
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#0D9488")
    accent_color = colors.HexColor("#D97706")
    neutral_bg = colors.HexColor("#F8FAFC")
    text_dark = colors.HexColor("#1E293B")

    # Estilos tipográficos personalizados
    style_title = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=primary_color,
        alignment=0,
        spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        "HeaderSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=secondary_color,
        alignment=0,
        spaceAfter=10
    )
    style_section = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )
    style_body = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=text_dark
    )
    style_body_bold = ParagraphStyle(
        "BodyDarkBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=text_dark
    )
    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    style_table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=text_dark
    )
    style_notes = ParagraphStyle(
        "MethodNotes",
        parent=styles["Italic"],
        fontName="Helvetica-Oblique",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#475569")
    )

    elementos = []

    # 1. ENCABEZADO INSTITUCIONAL
    elementos.append(Paragraph("OBSERVATORIO DE EDUCACIÓN SUPERIOR (OES)", style_title))
    elementos.append(Paragraph("Plataforma de Vigilancia Tecnológica, Regulatoria y Calidad Universitaria — Prototipo Académico", style_subtitle))
    elementos.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    # 2. METADATOS DEL REPORTE
    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    total_reg = len(df_filtrado)
    total_inst = df_filtrado["institucion"].nunique() if not df_filtrado.empty and "institucion" in df_filtrado.columns else 0
    total_cat = df_filtrado["categoria"].nunique() if not df_filtrado.empty and "categoria" in df_filtrado.columns else 0

    verificadas_cnt = len(df_filtrado[df_filtrado["estado_verificacion"] == "Verificada"]) if not df_filtrado.empty and "estado_verificacion" in df_filtrado.columns else 0
    pendientes_cnt = len(df_filtrado[df_filtrado["estado_verificacion"] == "Pendiente"]) if not df_filtrado.empty and "estado_verificacion" in df_filtrado.columns else 0
    observadas_cnt = len(df_filtrado[df_filtrado["estado_verificacion"] == "Observada"]) if not df_filtrado.empty and "estado_verificacion" in df_filtrado.columns else 0

    tabla_meta_data = [
        [
            Paragraph("<b>Fecha de Generación:</b>", style_body_bold), Paragraph(fecha_emision, style_body),
            Paragraph("<b>Criterios / Filtros:</b>", style_body_bold), Paragraph(filtros_aplicados_texto, style_body)
        ],
        [
            Paragraph("<b>Total Novedades:</b>", style_body_bold), Paragraph(str(total_reg), style_body),
            Paragraph("<b>Instituciones Involucradas:</b>", style_body_bold), Paragraph(str(total_inst), style_body)
        ]
    ]
    t_meta = Table(tabla_meta_data, colWidths=[100, 160, 100, 180])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), neutral_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(t_meta)
    elementos.append(Spacer(1, 10))

    # 3. INDICADORES Y CONTROL DE CALIDAD
    elementos.append(Paragraph("1. Resumen Estadístico y Estado de Verificación", style_section))
    kpi_data = [
        [
            Paragraph(f"<b>Noticias:</b> {total_reg}", style_body),
            Paragraph(f"<b>Categorías:</b> {total_cat}", style_body),
            Paragraph(f"<b>Verificadas:</b> {verificadas_cnt}", style_body),
            Paragraph(f"<b>Pendientes:</b> {pendientes_cnt}", style_body),
            Paragraph(f"<b>Observadas:</b> {observadas_cnt}", style_body),
        ]
    ]
    t_kpi = Table(kpi_data, colWidths=[108, 108, 108, 108, 108])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, primary_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(t_kpi)
    elementos.append(Spacer(1, 10))

    # 4. TABLA DETALLADA DE REGISTROS CONSULTADOS
    elementos.append(Paragraph("2. Relación de Noticias y Trazabilidad de Fuentes", style_section))
    
    filas_tabla = [
        [
            Paragraph("Fecha", style_table_header),
            Paragraph("Institución", style_table_header),
            Paragraph("Categoría", style_table_header),
            Paragraph("Título de la Novedad / Enlace Directo", style_table_header),
            Paragraph("Fuente", style_table_header),
            Paragraph("Estado", style_table_header)
        ]
    ]

    if not df_filtrado.empty:
        for _, row in df_filtrado.head(30).iterrows():
            f_fecha = str(row.get("fecha", ""))
            f_inst = str(row.get("institucion", ""))
            f_cat = str(row.get("categoria", ""))
            f_tit = str(row.get("titulo", ""))
            f_url = str(row.get("url", ""))
            f_fte = str(row.get("fuente", ""))
            f_est = str(row.get("estado_verificacion", "Pendiente"))

            titulo_con_url = f"<b>{f_tit}</b><br/><font color='#0284C7' size='6'>{f_url[:65]}...</font>"

            filas_tabla.append([
                Paragraph(f_fecha, style_table_cell),
                Paragraph(f_inst, style_table_cell),
                Paragraph(f_cat, style_table_cell),
                Paragraph(titulo_con_url, style_table_cell),
                Paragraph(f_fte, style_table_cell),
                Paragraph(f_est, style_table_cell)
            ])
    else:
        filas_tabla.append([
            Paragraph("-", style_table_cell),
            Paragraph("No se encontraron registros que coincidan con los filtros seleccionados.", style_table_cell),
            Paragraph("-", style_table_cell),
            Paragraph("-", style_table_cell),
            Paragraph("-", style_table_cell),
            Paragraph("-", style_table_cell),
        ])

    t_registros = Table(filas_tabla, colWidths=[55, 75, 75, 205, 75, 55])
    t_registros.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, neutral_bg])
    ]))
    elementos.append(t_registros)
    elementos.append(Spacer(1, 12))

    # 5. OBSERVACIONES METODOLÓGICAS Y DELIMITACIÓN ÉTICA
    elementos.append(Paragraph("3. Observaciones Metodológicas y Delimitación Ética", style_section))
    nota_metodologica = (
        "<b>Aviso Institucional:</b> El presente informe es un producto de monitoreo estructurado desarrollado "
        "con fines de investigación y análisis de políticas de educación superior. Los registros catalogados como "
        "demostrativos (ej. PRONABEC, UNMSM y PUCP de la Práctica Guiada N.° 08) tienen propósitos didácticos y "
        "deben ser corroborados en los portales oficiales de origen antes de sustentar decisiones de gestión. "
        "El conteo cuantitativo de noticias no constituye por sí mismo una evaluación de calidad institucional; "
        "únicamente refleja volumen y cobertura de publicaciones emitidas por fuentes gubernamentales y universitarias."
    )
    elementos.append(Paragraph(nota_metodologica, style_notes))
    elementos.append(Spacer(1, 14))

    # 6. FIRMA Y CONSTANCIA DE AUDITORÍA
    firmas_data = [
        [
            Paragraph("____________________________<br/><b>Analista Responsable OES</b><br/>Comité de Verificación de Fuentes", style_table_cell),
            Paragraph("____________________________<br/><b>Coordinación Técnica OES</b><br/>Ingeniería de Sistemas", style_table_cell)
        ]
    ]
    t_firmas = Table(firmas_data, colWidths=[270, 270])
    t_firmas.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(KeepTogether(t_firmas))

    # Construir documento
    doc.build(elementos)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if ruta_guardado:
        ruta_guardado.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta_guardado, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes

