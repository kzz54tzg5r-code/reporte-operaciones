import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Reporte de Operaciones Ropa",
    page_icon="👕",
    layout="wide"
)

# 2. DEFINICIÓN DE LA PALETA CORPORATIVA (Variaciones 25% más oscuras)
COLOR_AZUL_CORP = "#1a2a40"  # Accent 1 (Dark Blue)
COLOR_GRIS_CORP = "#333333"  # Background 1 (Dark Gray)
COLOR_GRIS_CLARO = "#f4f4f6"

# Estilos CSS para asegurar el look corporativo
st.markdown(f"""
    <style>
    .reportview-container .main .block-container {{
        padding-top: 2rem;
    }}
    h1, h2, h3 {{
        color: {COLOR_AZUL_CORP};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .metric-card {{
        background-color: {COLOR_GRIS_CLARO};
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid {COLOR_AZUL_CORP};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS (Histórico Consolidado extraído de la Matriz General)
@st.cache_data
def cargar_datos():
    data_operaciones = {
        "Semana": ["Semana 19", "Semana 19", "Semana 19", "Semana 19", 
                   "Semana 20", "Semana 20", "Semana 20", "Semana 20"],
        "Tienda": ["Arco Norte", "Miravalle", "Puebla Sur", "Vallejo", 
                   "Arco Norte", "Miravalle", "Puebla Sur", "Vallejo"],
        "Sis_Aduana": [511, 426, 501, 2891, 1662, 490, 870, 3625],
        "Muertos": [511, 311, 501, 2891, 1176, 257, 397, 2943],
        "Cajas": [1366, 266, 3579, 869, 660, 347, 2805, 1122],
        "Ad": [471, 692, 153, 3144, 623, 9, 458, 1933],
        "Total Ingresos": [2348, 1384, 4233, 6904, 2945, 846, 4133, 6680],
        "Piezas Habilitadas": [1866, 863, 3434, 5156, 3221, 121, 2091, 6332],
        "Eficiencia_Recorrido": [79.5, 62.4, 81.1, 74.7, 109.4, 14.3, 50.6, 94.8],
        "Pct_Habilitado_vs_Ingreso": [44.7, 40.4, 134.0, 142.6, 70.2, 51.1, 93.6, 176.6]
    }
    return pd.DataFrame(data_operaciones)

df_historico = cargar_datos()

# 4. ENCABEZADO PRINCIPAL
st.title("📊 Operaciones Ropa — Dashboard de Auditoría Operativa")
st.markdown("### Histórico Consolidado de Procesos de Muertos y Cambios")
st.write("---")

# 5. FILTROS LATERALES (Sidebar)
st.sidebar.header("Filtros de Búsqueda")
semana_seleccionada = st.sidebar.selectbox(
    "Selecciona la Semana:",
    options=df_historico["Semana"].unique(),
    index=len(df_historico["Semana"].unique()) - 1
)

# Filtrado de dataframe principal corregido
df_filtrado = df_historico[df_historico["Semana"] == semana_seleccionada]

# 6. SECCIÓN DE KPI CARDS (Resumen Semanal)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_ingresos = df_filtrado["Total Ingresos"].sum()
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin:0; font-size:0.9rem; color:#666;'>Total Ingresos</p>
        <h2 style='margin:0; color:{COLOR_AZUL_CORP};'>{total_ingresos:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_habilitado = df_filtrado["Piezas Habilitadas"].sum()
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin:0; font-size:0.9rem; color:#666;'>Piezas Habilitadas</p>
        <h2 style='margin:0; color:{COLOR_AZUL_CORP};'>{total_habilitado:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    eficiencia_promedio = df_filtrado["Eficiencia_Recorrido"].mean()
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin:0; font-size:0.9rem; color:#666;'>Eficiencia de Recorrido Prom.</p>
        <h2 style='margin:0; color:{COLOR_AZUL_CORP};'>{eficiencia_promedio:.1f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pct_gral = (total_habilitado / total_ingresos) * 100 if total_ingresos > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <p style='margin:0; font-size:0.9rem; color:#666;'>% Habilitado vs Ingreso</p>
        <h2 style='margin:0; color:{COLOR_AZUL_CORP};'>{pct_gral:.1f}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("##")

# 7. SECCIÓN DE GRÁFICOS COMPACTOS (4 KPIs en cuadrícula 2x2)
st.markdown("## 📈 Gráficos de Rendimiento por Tienda")
fila_graficos_1 = st.columns(2)
fila_graficos_2 = st.columns(2)

# Gráfico 1: Eficiencia del Recorrido por Tienda
with fila_graficos_1[0]:
    fig_recorrido = go.Figure()
    fig_recorrido.add_trace(go.Bar(
        x=df_filtrado["Tienda"],
        y=df_filtrado["Eficiencia_Recorrido"],
        marker_color=COLOR_AZUL_CORP,
        text=df_filtrado["Eficiencia_Recorrido"].apply(lambda x: f"{x}%"),
        textposition='auto'
    ))
    fig_recorrido.update_layout(
        title="Eficiencia del Recorrido (%)",
        xaxis_title="Tiendas",
        yaxis_title="Porcentaje",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor=COLOR_GRIS_CLARO)
    )
    st.plotly_chart(fig_recorrido, use_container_width=True)

# Gráfico 2: % Habilitado vs Ingreso Total
with fila_graficos_1[1]:
    fig_pct_hab = go.Figure()
    fig_pct_hab.add_trace(go.Bar(
        x=df_filtrado["Tienda"],
        y=df_filtrado["Pct_Habilitado_vs_Ingreso"],
        marker_color=COLOR_GRIS_CORP,
        text=df_filtrado["Pct_Habilitado_vs_Ingreso"].apply(lambda x: f"{x}%"),
        textposition='auto'
    ))
    fig_pct_hab.update_layout(
        title="% Habilitado vs Ingreso Total",
        xaxis_title="Tiendas",
        yaxis_title="Porcentaje",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor=COLOR_GRIS_CLARO)
    )
    st.plotly_chart(fig_pct_hab, use_container_width=True)

# Gráfico 3: Comparativo de Volumen (Ingreso vs Piezas Habilitadas)
with fila_graficos_2[0]:
    fig_volumen = go.Figure()
    fig_volumen.add_trace(go.Bar(
        name='Total Ingresos',
        x=df_filtrado["Tienda"],
        y=df_filtrado["Total Ingresos"],
        marker_color=COLOR_AZUL_CORP
    ))
    fig_volumen.add_trace(go.Bar(
        name='Piezas Habilitadas',
        x=df_filtrado["Tienda"],
        y=df_filtrado["Piezas Habilitadas"],
        marker_color=COLOR_GRIS_CORP
    ))
    fig_volumen.update_layout(
        barmode='group',
        title="Comparativo Volumen: Ingresos vs Piezas Habilitadas",
        xaxis_title="Tiendas",
        yaxis_title="Cantidad de Piezas",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor=COLOR_GRIS_CLARO),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_volumen, use_container_width=True)

# Gráfico 4: Desglose del Proceso Operativo (Sis_Aduana vs Muertos)
with fila_graficos_2[1]:
    fig_desglose = go.Figure()
    fig_desglose.add_trace(go.Bar(
        name='Sis_Aduana',
        x=df_filtrado["Tienda"],
        y=df_filtrado["Sis_Aduana"],
        marker_color="#2b4c7e"  # Tono azul secundario coordinado
    ))
    fig_desglose.add_trace(go.Bar(
        name='Muertos',
        x=df_filtrado["Tienda"],
        y=df_filtrado["Muertos"],
        marker_color="#555555"  # Tono gris secundario coordinado
    ))
    fig_desglose.update_layout(
        barmode='stack',
        title="Desglose Operativo: Sis_Aduana vs Muertos",
        xaxis_title="Tiendas",
        yaxis_title="Cantidad",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor=COLOR_GRIS_CLARO),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_desglose, use_container_width=True)

st.write("---")

# 8. MATRIZ GENERAL DE DATOS (Dataframe formateado)
st.markdown("## 📋 Matriz General de Auditoría Operativa")
st.markdown("Visualización completa del subset de datos de la semana activa.")

df_tabla = df_filtrado.copy()
df_tabla["Sis_Aduana"] = df_tabla["Sis_Aduana"].map("{:,}".format)
df_tabla["Muertos"] = df_tabla["Muertos"].map("{:,}".format)
df_tabla["Cajas"] = df_tabla["Cajas"].map("{:,}".format)
df_tabla["Ad"] = df_tabla["Ad"].map("{:,}".format)
df_tabla["Total Ingresos"] = df_tabla["Total Ingresos"].map("{:,}".format)
df_tabla["Piezas Habilitadas"] = df_tabla["Piezas Habilitadas"].map("{:,}".format)
df_tabla["Eficiencia_Recorrido"] = df_tabla["Eficiencia_Recorrido"].map("{:.1f}%".format)
df_tabla["Pct_Habilitado_vs_Ingreso"] = df_tabla["Pct_Habilitado_vs_Ingreso"].map("{:.1f}%".format)

st.dataframe(df_tabla, use_container_width=True, hide_index=True)
