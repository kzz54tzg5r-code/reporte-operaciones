import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS CORPORATIVOS
# ==========================================
st.set_page_config(
    page_title="Reporte de Operaciones Ropa",
    page_icon="👕",
    layout="wide"
)

# Paleta corporativa (25% más oscuras)
COLOR_AZUL_CORP = "#1a2a40"  # Accent 1
COLOR_GRIS_CORP = "#333333"  # Background 1
COLOR_GRIS_CLARO = "#f4f4f6"
COLOR_ROJO_ALERTA = "#E6007E"
COLOR_VERDE_OK = "#1F497D"

st.markdown(f"""
    <style>
    .block-container {{ padding-top: 2rem; }}
    h1, h2, h3 {{ color: {COLOR_AZUL_CORP}; font-family: 'Segoe UI', sans-serif; }}
    .metric-card {{
        background-color: {COLOR_GRIS_CLARO};
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid {COLOR_AZUL_CORP};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    /* Estilos para replicar exactamente tu tabla HTML corporativa */
    .table-corp {{ width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }}
    .table-corp th {{ background-color: {COLOR_AZUL_CORP}; color: white; padding: 10px; font-size: 13px; text-align: center; }}
    .table-corp td {{ padding: 10px; text-align: center; border-bottom: 1px solid #EFEFEF; font-size: 13px; }}
    .cell-bg {{ background-color: #F9FBFD; color: {COLOR_VERDE_OK}; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PROCESAMIENTO Y CARGA DE DATOS (HISTÓRICO CONSOLIDADO)
# ==========================================
@st.cache_data
def cargar_y_procesar_datos():
    # Histórico base Semanas 19 y 20
    data_historica = {
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
    df = pd.DataFrame(data_historica)
    
    # Filas detalladas de la Semana 21 (Se agrupan automáticamente por Tienda)
    data_s21_parcial = {
        "Semana": ["Semana 21"] * 9,
        "Tienda": ["Arco Norte", "Miravalle", "Miravalle", "Miravalle", "Miravalle", "Miravalle", "Miravalle", "Miravalle", "Puebla Sur"],
        "Sis_Aduana": [264, 44, 47, 64, 57, 55, 88, 41, 79],
        "Muertos": [107, 0, 37, 0, 4, 7, 0, 0, 0],
        "Cajas": [57, 0, 39, 0, 31, 14, 0, 0, 0],
        "Ad": [78, 0, 17, 0, 6, 0, 0, 0, 0],
        "Total Ingresos": [399, 44, 103, 64, 94, 69, 88, 41, 79],
        "Piezas Habilitadas": [784, 0, 81, 0, 0, 58, 0, 0, 185],
        "Eficiencia_Recorrido": [117.2, 0.0, 124.8, 0.0, 0.0, 80.0, 0.0, 0.0, 80.0], # Datos calculados por fila
        "Pct_Habilitado_vs_Ingreso": [127.5, 0.0, 25.1, 0.0, 0.0, 124.8, 0.0, 0.0, 83.7]
    }
    df_s21 = pd.DataFrame(data_s21_parcial)
    
    # Agrupamos la Semana 21 para que no se repitan las tiendas en la matriz general
    df_s21_agrupado = df_s21.groupby(["Semana", "Tienda"]).agg({
        "Sis_Aduana": "sum",
        "Muertos": "sum",
        "Cajas": "sum",
        "Ad": "sum",
        "Total Ingresos": "sum",
        "Piezas Habilitadas": "sum"
    }).reset_index()
    
    # Recalculamos los ratios porcentuales correctos a nivel acumulado por tienda
    df_s21_agrupado["Eficiencia_Recorrido"] = (df_s21_agrupado["Piezas Habilitadas"] / df_s21_agrupado["Total Ingresos"] * 100).round(1)
    df_s21_agrupado["Pct_Habilitado_vs_Ingreso"] = (df_s21_agrupado["Piezas Habilitadas"] / df_s21_agrupado["Total Ingresos"] * 100).round(1)
    
    # Unimos el histórico con la nueva semana limpia
    df_consolidado = pd.concat([df, df_s21_agrupado], ignore_index=True)
    return df_consolidado

df_historico = cargar_y_procesar_datos()

# ==========================================
# 3. ENCABEZADO PRINCIPAL
# ==========================================
st.title("📊 Operaciones Ropa — Dashboard de Auditoría Operativa")
st.markdown("### Histórico Consolidado de Procesos de Muertos y Cambios")
st.write("---")

# Filtro en el Sidebar
st.sidebar.header("Filtros de Búsqueda")
semana_seleccionada = st.sidebar.selectbox(
    "Selecciona la Semana para ver el desglose:",
    options=df_historico["Semana"].unique(),
    index=len(df_historico["Semana"].unique()) - 1
)
df_filtrado = df_historico[df_historico["Semana"] == semana_seleccionada]

# ==========================================
# 4. TARJETAS KPI RESUMEN (DÁMICAS POR SEMANA SELECCIONADA)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><p style="margin:0; font-size:0.9rem; color:#666;">TOTAL INGRESOS</p><h2 style="margin:0; color:{COLOR_AZUL_CORP};">{df_filtrado["Total Ingresos"].sum():,}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p style="margin:0; font-size:0.9rem; color:#666;">PIEZAS HABILITADAS</p><h2 style="margin:0; color:{COLOR_AZUL_CORP};">{df_filtrado["Piezas Habilitadas"].sum():,} ({df_filtrado["Piezas Habilitadas"].sum()/df_filtrado["Total Ingresos"].sum()*100:.1f}%)</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p style="margin:0; font-size:0.9rem; color:#666;">PIEZAS UBICADAS</p><h2 style="margin:0; color:{COLOR_AZUL_CORP};">{df_filtrado["Cajas"].sum():,}</h2></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p style="margin:0; font-size:0.9rem; color:#666;">% DE RECORRIDOS</p><h2 style="margin:0; color:{COLOR_AZUL_CORP};">{df_filtrado["Eficiencia_Recorrido"].mean():.1f}%</h2></div>', unsafe_allow_html=True)

st.write("##")

# ==========================================
# 5. TABLA DINÁMICA DE TENDENCIA Y VARIACIÓN INTERSEMANAL
# ==========================================
st.markdown("## 📈 Análisis de Tendencia y Variación Intersemanal")

# Agrupación por semanas para calcular los deltas automáticamente
df_semanal = df_historico.groupby("Semana").agg({
    "Total Ingresos": "sum",
    "Piezas Habilitadas": "sum",
    "Eficiencia_Recorrido": "mean"
}).reset_index()

# Cálculo automático de diferencias inter-semanales
df_semanal["Vol_Delta"] = df_semanal["Total Ingresos"].diff()
df_semanal["Vol_Delta_Pct"] = df_semanal["Total Ingresos"].pct_change() * 100
df_semanal["Piezas_Delta"] = df_semanal["Piezas Habilitadas"].diff()
df_semanal["Piezas_Delta_Pct"] = df_semanal["Piezas Habilitadas"].pct_change() * 100
df_semanal["Ef_Delta"] = df_semanal["Eficiencia_Recorrido"].diff()

# Construcción de la tabla HTML limpia
html_table = f"""
<table class="table-corp">
    <tr>
        <th>Dimensión Temporal</th>
        <th>Vol. Ingresos Total</th>
        <th>Δ Vs. Sem Anterior</th>
        <th>Piezas Habilitadas</th>
        <th>Δ Vs. Sem Anterior</th>
        <th>% Rendimiento Recorridos</th>
        <th>Δ Eficiencia Recorridos</th>
    </tr>
"""

for i, row in df_semanal.iterrows():
    if i == 0:
        d_vol = "N/A (Línea Base)"
        d_piezas = "N/A"
        d_ef = "N/A"
    else:
        c_vol = COLOR_ROJO_ALERTA if row["Vol_Delta"] < 0 else COLOR_VERDE_OK
        c_p = COLOR_ROJO_ALERTA if row["Piezas_Delta"] < 0 else COLOR_VERDE_OK
        c_ef = COLOR_ROJO_ALERTA if row["Ef_Delta"] < 0 else COLOR_VERDE_OK
        
        d_vol = f'<b style="color:{c_vol}">{row["Vol_Delta"]:+,} u. ({row["Vol_Delta_Pct"]:.1f}%)</b>'
        d_piezas = f'<b style="color:{c_p}">{row["Piezas_Delta"]:+,} u. ({row["Piezas_Delta_Pct"]:.1f}%)</b>'
        d_ef = f'<b style="color:{c_ef}">{row["Ef_Delta"]:+.1f} pp</b>'

    pct_hab = (row["Piezas Habilitadas"] / row["Total Ingresos"]) * 100
    
    html_table += f"""
    <tr>
        <td class="cell-bg">{row['Semana']}</td>
        <td>{row['Total Ingresos']:,}</td>
        <td>{d_vol}</td>
        <td>{row['Piezas Habilitadas']:,} <small style="color:#555">({pct_hab:.1f}%)</small></td>
        <td>{d_piezas}</td>
        <td style="font-weight:bold;">{row['Eficiencia_Recorrido']:.1f}%</td>
        <td>{d_ef}</td>
    </tr>
    """
html_table += "</table>"
st.markdown(html_table, unsafe_allow_html=True)

st.write("##")

# ==========================================
# 6. GRÁFICA DE EVOLUCIÓN (LÍNEA DE TENDENCIA VS VOLUMEN)
# ==========================================
fig_linea = go.Figure()
# Barras para el volumen de entrada
fig_linea.add_trace(go.Bar(
    name="Volumen Total Ingresos",
    x=df_semanal["Semana"],
    y=df_semanal["Total Ingresos"],
    marker_color="#EFEFEF",
    yaxis="y"
))
# Línea para el rendimiento
fig_linea.add_trace(go.Scatter(
    name="Evolución % Recorridos",
    x=df_semanal["Semana"],
    y=df_semanal["Eficiencia_Recorrido"],
    line=dict(color=COLOR_ROJO_ALERTA, width=3, dash="dash"),
    marker=dict(size=8),
    yaxis="y2"
))

fig_linea.update_layout(
    title="Línea de Tendencia: Desempeño Operativo vs Volumen de Entrada",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(title="Volumen Total Ingresos", side="left"),
    yaxis2=dict(title="Porcentaje (%)", side="right", overlaying="y", range=[0, 120]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.01)
)
st.plotly_chart(fig_linea, use_container_width=True)

# ==========================================
# 7. MATRIZ GENERAL (DATAFRAME DE LA SEMANA)
# ==========================================
st.write("---")
st.markdown(f"## 📋 Matriz de Auditoría — Detalle {semana_seleccionada}")
df_tabla = df_filtrado.copy()
for col in ["Sis_Aduana", "Muertos", "Cajas", "Ad", "Total Ingresos", "Piezas Habilitadas"]:
    df_tabla[col] = df_tabla[col].map("{:,}".format)
df_tabla["Eficiencia_Recorrido"] = df_tabla["Eficiencia_Recorrido"].map("{:.1f}%".format)
df_tabla["Pct_Habilitado_vs_Ingreso"] = df_tabla["Pct_Habilitado_vs_Ingreso"].map("{:.1f}%".format)

st.dataframe(df_tabla, use_container_width=True, hide_index=True)
