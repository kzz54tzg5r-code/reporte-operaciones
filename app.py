import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuración de página ancha (Wide Mode) Estilo Corporativo
st.set_page_config(layout="wide", page_title="PRICE SHOES • Operaciones Ropa")

# --- CABECERA ESTILO PRICE SHOES ---
st.markdown("<h1 style='color: #000000; margin-bottom: 0px;'>👚 PRICE SHOES • Operaciones Ropa</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #E6007E; margin-top: 0px; font-weight: bold;'>CONTROL DE ACONDICIONAMIENTO, SEGUIMIENTO DE RECORRIDOS Y MATRIZ DE PISO</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- BASE DE DATOS COMPLETA (Datos extraídos de tus archivos) ---
# Creamos un DataFrame estructurado para poder agrupar por Mes o Semana de forma dinámica
raw_data = {
    'Mes': ['Mayo', 'Mayo', 'Mayo', 'Junio'],
    'Periodo': ['Semana 19', 'Semana 20', 'Semana 21', 'Semana 22 (Corte)'],
    'Ingresos': [15724, 13758, 13561, 1424],
    'Habilitadas': [10456, 11644, 11544, 1100],
    'Ubicadas': [6851, 6796, 12598, 5224],
    # Datos de composición simulados manteniendo la proporción de tus checklists
    'Sis_Aduana': [4000, 3500, 3800, 500],
    'Muertos': [2500, 3000, 2200, 300],
    'Cajas': [9224, 7258, 7561, 624]
}
df_base = pd.DataFrame(raw_data)

# --- MENÚ DE FILTROS (POR MES O SEMANA) ---
st.sidebar.header("⚙️ Configuración del Reporte")
tipo_vista = st.sidebar.radio(
    "Visualizar datos por:",
    ["Por Semana", "Por Mes"]
)

# --- LÓGICA DE AGREGACIÓN DE BI ---
if tipo_vista == "Por Semana":
    # Selección individual de la semana para las tarjetas estáticas
    elemento_sel = st.selectbox("Selecciona la Semana Operativa:", df_base['Periodo'].unique())
    
    # Filtrado para KPIs de la parte superior
    data_filtrada = df_base[df_base['Periodo'] == elemento_sel].iloc[0]
    
    # Configuración para las gráficas históricas (Eje X)
    eje_x = 'Periodo'
    df_graficas = df_base

else:
    # Agrupamos los datos por mes sumando los volúmenes
    df_mensual = df_base.groupby('Mes', as_index=False).agg({
        'Ingresos': 'sum',
        'Habilitadas': 'sum',
        'Ubicadas': 'sum',
        'Sis_Aduana': 'sum',
        'Muertos': 'sum',
        'Cajas': 'sum'
    })
    
    elemento_sel = st.selectbox("Selecciona el Mes Operativo:", df_mensual['Mes'].unique())
    
    # Filtrado para KPIs de la parte superior
    data_filtrada = df_mensual[df_mensual['Mes'] == elemento_sel].iloc[0]
    
    # Configuración para las gráficas históricas (Eje X)
    eje_x = 'Mes'
    df_graficas = df_mensual

# Cálculo de porcentajes de eficiencia dinámicos para las tarjetas
eficiencia_recorrido = round((data_filtrada['Habilitadas'] / data_filtrada['Ingresos']) * 100, 1)
porcentaje_ubicado = round((data_filtrada['Ubicadas'] / data_filtrada['Habilitadas']) * 100, 1)


# --- BLOQUE DE TARJETAS DE INDICES (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"<div style='background-color: #F8F9FA; padding: 20px; border-radius: 5px; text-align: center; border: 1px solid #E2E8F0;'>"
        f"<p style='color: #4A5568; font-weight: bold; margin-bottom: 5px;'>📥 TOTAL INGRESOS ({elemento_sel})</p>"
        f"<h2 style='color: #1A365D; margin-top: 0px;'>{data_filtrada['Ingresos']:,}</h2>"
        f"</div>", unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div style='background-color: #F8F9FA; padding: 20px; border-radius: 5px; text-align: center; border: 1px solid #E2E8F0;'> "
        f"<p style='color: #4A5568; font-weight: bold; margin-bottom: 5px;'>✨ PIEZAS HABILITADAS</p>"
        f"<h2 style='color: #1A365D; margin-top: 0px;'>{data_filtrada['Habilitadas']:,}</h2>"
        f"</div>", unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div style='background-color: #F8F9FA; padding: 20px; border-radius: 5px; text-align: center; border: 1px solid #E2E8F0;'>"
        f"<p style='color: #4A5568; font-weight: bold; margin-bottom: 5px;'>🎯 EFICIENCIA RECORRIDOS</p>"
        f"<h2 style='color: #1A365D; margin-top: 0px;'>{eficiencia_recorrido}%</h2>"
        f"</div>", unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"<div style='background-color: #F8F9FA; padding: 20px; border-radius: 5px; text-align: center; border: 1px solid #E2E8F0;'>"
        f"<p style='color: #4A5568; font-weight: bold; margin-bottom: 5px;'>📍 % UBICADO TOTAL</p>"
        f"<h2 style='color: #1A365D; margin-top: 0px;'>{porcentaje_ubicado}%</h2>"
        f"</div>", unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# --- TÍTULO DE GRÁFICOS CON BARRA AZUL DE DETALLE ---
st.markdown(
    f"<div style='border-left: 5px solid #1A365D; padding-left: 10px; margin-bottom: 20px;'>"
    f"<h4 style='color: #1A365D; margin: 0px; font-weight: bold;'>📊 Gráficos de Rendimiento y Distribución Operativa ({tipo_vista})</h4>"
    f"</div>", unsafe_allow_html=True
)


# --- SECCIÓN DE GRÁFICOS EN PARALELO ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown(f"**Piezas Habilitadas {tipo_vista}**")
    fig1 = px.bar(df_graficas, x=eje_x, y='Habilitadas', text_auto='.3s',
                  color_discrete_sequence=['#1A365D'])
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10))
    fig1.update_yaxes(showgrid=True, gridcolor='#E2E8F0', title_text="Piezas")
    fig1.update_xaxes(title_text=tipo_vista)
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    st.markdown(f"**Composición de Ingresos {tipo_vista}**")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='Sis_Aduana', x=df_graficas[eje_x], y=df_graficas['Sis_Aduana'], marker_color='#1A365D'))
    fig2.add_trace(go.Bar(name='Muertos', x=df_graficas[eje_x], y=df_graficas['Muertos'], marker_color='#E6007E'))
    fig2.add_trace(go.Bar(name='Cajas', x=df_graficas[eje_x], y=df_graficas['Cajas'], marker_color='#718096'))
    
    fig2.update_layout(barmode='stack', plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=10, b=10, l=10, r=10))
    fig2.update_yaxes(showgrid=True, gridcolor='#E2E8F0', title_text="Piezas")
    fig2.update_xaxes(title_text=tipo_vista)
    st.plotly_chart(fig2, use_container_width=True)
    
