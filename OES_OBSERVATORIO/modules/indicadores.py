"""
Módulo de Cálculo de Indicadores y Visualizaciones Gráficas Interactivas con Plotly.
Permite evaluar en tiempo real métricas cuantitativas del ecosistema universitario peruano.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Paleta de colores institucional para educación superior y tecnología
COLOR_PRIMARY = "#1A365D"    # Azul marino institucional
COLOR_SECONDARY = "#0D9488"  # Verde azulado / teal
COLOR_ACCENT = "#D97706"     # Ámbar dorado
COLOR_VERIFICADO = "#16A34A" # Verde éxito
COLOR_PENDIENTE = "#EAB308"  # Amarillo alerta
COLOR_OBSERVADO = "#DC2626"  # Rojo observación
COLOR_BG = "#F8FAFC"         # Gris azulado muy claro


def calcular_metricas_globales(df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula indicadores clave de desempeño (KPIs) sobre el conjunto de datos filtrado."""
    if df.empty:
        return {
            "total_noticias": 0,
            "total_instituciones": 0,
            "total_categorias": 0,
            "total_fuentes": 0,
            "total_verificadas": 0,
            "porcentaje_verificadas": 0.0,
            "tasa_impacto_alto": 0.0
        }

    total_noticias = len(df)
    total_instituciones = df["institucion"].nunique() if "institucion" in df.columns else 0
    total_categorias = df["categoria"].nunique() if "categoria" in df.columns else 0
    total_fuentes = df["fuente"].nunique() if "fuente" in df.columns else 0

    verificadas = len(df[df["estado_verificacion"] == "Verificada"]) if "estado_verificacion" in df.columns else 0
    pct_verificadas = round((verificadas / total_noticias) * 100, 1)

    impacto_alto = len(df[df["impacto_regulatorio"] == "Alto"]) if "impacto_regulatorio" in df.columns else 0
    pct_impacto_alto = round((impacto_alto / total_noticias) * 100, 1)

    return {
        "total_noticias": total_noticias,
        "total_instituciones": total_instituciones,
        "total_categorias": total_categorias,
        "total_fuentes": total_fuentes,
        "total_verificadas": verificadas,
        "porcentaje_verificadas": pct_verificadas,
        "tasa_impacto_alto": pct_impacto_alto
    }


def grafico_distribucion_categorias(df: pd.DataFrame) -> go.Figure:
    """Genera un gráfico de barras horizontal ordenado por frecuencia de categorías."""
    if df.empty or "categoria" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Sin datos para mostrar")
        return fig

    conteo = df["categoria"].value_counts().reset_index()
    conteo.columns = ["Categoría", "Cantidad"]

    fig = px.bar(
        conteo,
        x="Cantidad",
        y="Categoría",
        orientation="h",
        text="Cantidad",
        color="Categoría",
        color_discrete_sequence=px.colors.qualitative.Prism,
        title="<b>Distribución de Novedades por Categoría Temática</b>"
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Número de Noticias",
        yaxis_title="",
        showlegend=False,
        height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_traces(textposition="outside")
    return fig


def grafico_evolucion_temporal(df: pd.DataFrame) -> go.Figure:
    """Genera gráfico de línea con la evolución cronológica de registros."""
    if df.empty or "fecha" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Sin datos temporales")
        return fig

    df_temp = df.copy()
    df_temp["fecha"] = pd.to_datetime(df_temp["fecha"], errors="coerce")
    df_temp = df_temp.dropna(subset=["fecha"])
    
    if df_temp.empty:
        fig = go.Figure()
        fig.update_layout(title="Fechas no válidas")
        return fig

    conteo_fecha = df_temp.groupby(df_temp["fecha"].dt.strftime("%Y-%m-%d")).size().reset_index(name="Noticias")
    conteo_fecha = conteo_fecha.sort_values(by="fecha")

    fig = px.area(
        conteo_fecha,
        x="fecha",
        y="Noticias",
        markers=True,
        title="<b>Evolución Cronológica de Noticias Capturadas</b>",
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Fecha de Novedad",
        yaxis_title="Cantidad Registrada",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def grafico_estados_verificacion(df: pd.DataFrame) -> go.Figure:
    """Genera un gráfico tipo Donut con los estados de verificación ética."""
    if df.empty or "estado_verificacion" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Sin datos de verificación")
        return fig

    conteo = df["estado_verificacion"].value_counts().reset_index()
    conteo.columns = ["Estado", "Cantidad"]

    color_map = {
        "Verificada": COLOR_VERIFICADO,
        "Pendiente": COLOR_PENDIENTE,
        "Observada": COLOR_OBSERVADO
    }

    fig = px.pie(
        conteo,
        names="Estado",
        values="Cantidad",
        hole=0.45,
        title="<b>Control Ético y Calidad Informativa</b>",
        color="Estado",
        color_discrete_map=color_map
    )
    fig.update_layout(
        paper_bgcolor="white",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig


def grafico_top_instituciones(df: pd.DataFrame, top_n: int = 7) -> go.Figure:
    """Genera gráfico de barras con las instituciones con mayor cobertura."""
    if df.empty or "institucion" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Sin datos institucionales")
        return fig

    top_inst = df["institucion"].value_counts().head(top_n).reset_index()
    top_inst.columns = ["Institución", "Noticias"]

    fig = px.bar(
        top_inst,
        x="Institución",
        y="Noticias",
        text="Noticias",
        title=f"<b>Top {top_n} Instituciones con Mayor Frecuencia</b>",
        color="Noticias",
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="",
        yaxis_title="Noticias",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_traces(textposition="outside")
    return fig

