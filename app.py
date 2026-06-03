import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE INTERFAZ GENERAL ---
st.set_page_config(page_title="Price Shoes - Business Intelligence", layout="wide", page_icon="👚")

# Estilos corporativos basados en la identidad visual de Price Shoes
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: bold; color: #1F497D !important; }
    
    /* Inyección de estilo para asegurar que el encabezado del dataframe respete el Azul Énfasis 1 Oscuro */
    .stDataFrame th {
        background-color: #1F497D !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET CONSOLIDADO OPERATIVO ---
@st.cache_data
def get_operational_data():
    data = [
        # Lunes 25
        {"Fecha": "2026-05-25", "Tienda": "Vallejo", "Sis_Aduana": 293, "Fis_Aduana": 332, "Muertos": 32, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 229, "Habilitadas": 248, "Ubicadas": 356},
        {"Fecha": "2026-05-25", "Tienda": "Arco Norte", "Sis_Aduana": 109, "Fis_Aduana": 82, "Muertos": 36, "Cajas": 73, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 109, "Habilitadas": 409, "Ubicadas": 545},
        {"Fecha": "2026-05-25", "Tienda": "Puebla Sur", "Sis_Aduana": 79, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 185, "Ubicadas": 197},
        {"Fecha": "2026-05-25", "Tienda": "Miravalle", "Sis_Aduana": 44, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Martes 26
        {"Fecha": "2026-05-26", "Tienda": "Vallejo", "Sis_Aduana": 441, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 235, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 235, "Habilitadas": 595, "Ubicadas": 381},
        {"Fecha": "2026-05-26", "Tienda": "Arco Norte", "Sis_Aduana": 164, "Fis_Aduana": 75, "Muertos": 30, "Cajas": 144, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 174, "Habilitadas": 201, "Ubicadas": 309},
        {"Fecha": "2026-05-26", "Tienda": "Puebla Sur", "Sis_Aduana": 113, "Fis_Aduana": 108, "Muertos": 98, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 98, "Habilitadas": 116, "Ubicadas": 198},
        {"Fecha": "2026-05-26", "Tienda": "Miravalle", "Sis_Aduana": 47, "Fis_Aduana": 37, "Muertos": 39, "Cajas": 17, "Meta_Rec": 5, "Real_Rec": 2, "Recolectadas": 39, "Habilitadas": 81, "Ubicadas": 129},
        
        # Miércoles 27
        {"Fecha": "2026-05-27", "Tienda": "Vallejo", "Sis_Aduana": 436, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 3, "Recolectadas": 197, "Habilitadas": 478, "Ubicadas": 452},
        {"Fecha": "2026-05-27", "Tienda": "Arco Norte", "Sis_Aduana": 170, "Fis_Aduana": 47, "Muertos": 51, "Cajas": 51, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 102, "Habilitadas": 171, "Ubicadas": 350},
        {"Fecha": "2026-05-27", "Tienda": "Puebla Sur", "Sis_Aduana": 67, "Fis_Aduana": 65, "Muertos": 160, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 160, "Habilitadas": 307, "Ubicadas": 617},
        {"Fecha": "2026-05-27", "Tienda": "Miravalle", "Sis_Aduana": 64, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Jueves 28
        {"Fecha": "2026-05-28", "Tienda": "Vallejo", "Sis_Aduana": 550, "Fis_Aduana": 563, "Muertos": 168, "Cajas": 224, "Meta_Rec": 8, "Real_Rec": 8, "Recolectadas": 392, "Habilitadas": 755, "Ubicadas": 452},
        {"Fecha": "2026-05-28", "Tienda": "Arco Norte", "Sis_Aduana": 200, "Fis_Aduana": 134, "Muertos": 103, "Cajas": 75, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 178, "Habilitadas": 84, "Ubicadas": 350},
        {"Fecha": "2026-05-28", "Tienda": "Puebla Sur", "Sis_Aduana": 131, "Fis_Aduana": 146, "Muertos": 103, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 103, "Habilitadas": 32, "Ubicadas": 617},
        {"Fecha": "2026-05-28", "Tienda": "Miravalle", "Sis_Aduana": 57, "Fis_Aduana": 4, "Muertos": 31, "Cajas": 6, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 37, "Habilitadas": 0, "Ubicadas": 0},
        
        # Viernes 29
        {"Fecha": "2026-05-29", "Tienda": "Vallejo", "Sis_Aduana": 571, "Fis_Aduana": 596, "Muertos": 282, "Cajas": 196, "Meta_Rec": 5, "Real_Rec": 14, "Recolectadas": 503, "Habilitadas": 1017, "Ubicadas": 2099},
        {"Fecha": "2026-05-29", "Tienda": "Arco Norte", "Sis_Aduana": 260, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 22, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 22, "Habilitadas": 0, "Ubicadas": 0},
        {"Fecha": "2026-05-29", "Tienda": "Puebla Sur", "Sis_Aduana": 160, "Fis_Aduana": 152, "Muertos": 39, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 39, "Habilitadas": 226, "Ubicadas": 384},
        {"Fecha": "2026-05-29", "Tienda": "Miravalle", "Sis_Aduana": 55, "Fis_Aduana": 7, "Muertos": 14, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 14, "Habilitadas": 58, "Ubicadas": 105},
        
        # Sábado 30
        {"Fecha": "2026-05-30", "Tienda": "Vallejo", "Sis_Aduana": 513, "Fis_Aduana": 0, "Muertos": 68, "Cajas": 363, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 431, "Habilitadas": 624, "Ubicadas": 611},
        {"Fecha": "2026-05-30", "Tienda": "Arco Norte", "Sis_Aduana": 240, "Fis_Aduana": 246, "Muertos": 60, "Cajas": 115, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 175, "Habilitadas": 206, "Ubicadas": 1083},
        {"Fecha": "2026-05-30", "Tienda": "Puebla Sur", "Sis_Aduana": 85, "Fis_Aduana": 70, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 70, "Ubicadas": 70},
        {"Fecha": "2026-05-30", "Tienda": "Miravalle", "Sis_Aduana": 88, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Domingo 31
        {"Fecha": "2026-05-31", "Tienda": "Vallejo", "Sis_Aduana": 351, "Fis_Aduana": 351, "Muertos": 326, "Cajas": 488, "Meta_Rec": 8, "Real_Rec": 16, "Recolectadas": 884, "Habilitadas": 705, "Ubicadas": 2605},
        {"Fecha": "2026-05-31", "Tienda": "Arco Norte", "Sis_Aduana": 264, "Fis_Aduana": 107, "Muertos": 57, "Cajas": 78, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 135, "Habilitadas": 784, "Ubicadas": 482},
        {"Fecha": "2026-05-31", "Tienda": "Puebla Sur", "Sis_Aduana": 104, "Fis_Aduana": 110, "Muertos": 198, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 198, "Habilitadas": 340, "Ubicadas": 440},
        {"Fecha": "2026-05-31", "Tienda": "Miravalle", "Sis_Aduana": 41, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0}
    ]
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Métricas Base
    df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
    df['Eficiencia_Recorridos'] = (df['Real_Rec'] / df['Meta_Rec']) * 100
    
    # % Habilitado = (Piezas Habilitadas / Total Ingresos) * 100
    df['Porcentaje_Habilitado'] = ((df['Habilitadas'] / df['Total_Ingresos']).replace([float('inf'), -float('inf')], 0).fillna(0) * 100)
    
    # % Ubicado (Efectividad en Piso original)
    df['Porcentaje_Ubicado'] = ((df['Ubicadas'] / df['Total_Ingresos']).replace([float('inf'), -float('inf')], 0).fillna(0) * 100).clip(upper=100.0)
    
    # Texto de días en español
    dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
    df['Dia_Texto'] = df['Dia_Semana_Num'].map(dias_espanol) + df['Fecha'].dt.strftime(' (%Y-%m-%d)')
    
    return df.sort_values("Fecha")

df = get_operational_data()

# --- HEADER CORPORATIVO ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Business Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">MÓDULO: OPERACIONES ROPA – CONTROL DE ACONDICIONAMIENTO Y PISO (SEM 21)</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

# --- FILTROS EN SIDEBAR ---
st.sidebar.markdown("### 🎛️ Filtros de Operación")
tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + list(df['Tienda'].unique()))

min_date = df['Fecha'].min().date()
max_date = df['Fecha'].max().date()
fecha_rango = st.sidebar.date_input("Rango Temporal", [min_date, max_date])

# Aplicación dinámica de filtros
df_filtered = df.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

if len(fecha_rango) == 2:
    start_date, end_date = fecha_rango
    df_filtered = df_filtered[(df_filtered['Fecha'].dt.date >= start_date) & (df_filtered['Fecha'].dt.date <= end_date)]

lista_dias_ordenados = df_filtered.sort_values("Fecha")['Dia_Texto'].unique()

# --- TARJETAS KPI DE INICIO ---
if not df_filtered.empty:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#D9D9D9; border-left: 6px solid #1F497D;'><strong>Pzas Ropa Ingresadas</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:,}</span></div>".format(df_filtered['Total_Ingresos'].sum()), unsafe_allow_html=True)
    with kpi_col2:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#F0F4F8; border-left: 6px solid #1F497D;'><strong>Eficiencia Recorridos Prom.</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:.1f}%</span></div>".format(df_filtered['Eficiencia_Recorridos'].mean()), unsafe_allow_html=True)
    with kpi_col3:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#D9D9D9; border-left: 6px solid #1F497D;'><strong>Prendas Habilitadas Total</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:,}</span></div>".format(df_filtered['Habilitadas'].sum()), unsafe_allow_html=True)
    with kpi_col4:
        diff_aduana = df_filtered['Fis_Aduana'].sum() - df_filtered['Sis_Aduana'].sum()
        status_color = "#27AE60" if diff_aduana >= 0 else "#C0392B"
        st.markdown(f"<div style='padding:12px; border-radius:4px; background-color:#F0F4F8; border-left: 6px solid {status_color};'><strong>Desviación Aduana Ropa</strong><br><span style='font-size:24px; font-weight:bold; color:{status_color};'>{diff_aduana:+,}</span></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # --- BLOQUE DE GRÁFICOS INTERACTIVOS ---
    # =========================================================================

    # --- GRÁFICO 1 ---
    st.markdown('<p class="graph-title">🎯 1. Eficiencia del Recorrido (Meta Objetivo 100%)</p>', unsafe_allow_html=True)
    df_line_data = df_filtered.sort_values("Fecha").copy()
    df_line_data['Eficiencia_Etiqueta'] = "<b>" + df_line_data['Eficiencia_Recorridos'].round(1).astype(str) + '%</b>'
    
    fig_line = px.line(
        df_line_data, 
        x="Dia_Texto", y="Eficiencia_Recorridos", color="Tienda",
        markers=True, text="Eficiencia_Etiqueta",
        color_discrete_sequence=["#1F497D", "#5B9BD5", "#7F97B2", "#A6A6A6"]
    )
    fig_line.add_hline(y=100.0, line_dash="dash", line_color="#C0392B", annotation_text="Meta 100%", annotation_position="top left")
    fig_line.update_traces(
        line=dict(width=4.5), 
        marker=dict(size=12), 
        textposition="top center",
        textfont=dict(size=12, color="black")
    )
    fig_line.update_layout(
        plot_bgcolor="white", paper_bgcolor="white", height=540,
        margin=dict(l=50, r=50, t=40, b=50), legend=dict(orientation="h", y=1.09, x=0, font=dict(size=13))
    )
    fig_line.update_xaxes(showgrid=True, gridcolor='#EFEFEF', title="Día", title_font=dict(size=14),
                          type='category', categoryorder='array', categoryarray=lista_dias_ordenados)
    fig_line.update_yaxes(showgrid=True, gridcolor='#EFEFEF', title="% Eficiencia Real", title_font=dict(size=14))
    st.plotly_chart(fig_line, use_container_width=True)

    # --- GRÁFICO 2 ---
    st.markdown('<p class="graph-title">📦 2. Volumen de Prendas: Habilitado vs Ingreso Total</p>', unsafe_allow_html=True)
    df_daily_totals = df_filtered.groupby(["Fecha", "Dia_Texto"]).sum(numeric_only=True).reset_index().sort_values("Fecha")
    df_daily_totals['Pct_Habilitado'] = (df_daily_totals['Habilitadas'] / df_daily_totals['Total_Ingresos'] * 100).fillna(0).round(1)
    df_daily_totals['Pct_Text'] = "<b>" + df_daily_totals['Pct_Habilitado'].astype(str) + '%</b>'

    fig_grouped = go.Figure()
    fig_grouped.add_trace(go.Bar(
        name='Ingreso Total', x=df_daily_totals['Dia_Texto'], y=df_daily_totals['Total_Ingresos'], 
        marker_color='#1F497D', yaxis='y',
        text=[f"<b>{int(val):,}</b>" for val in df_daily_totals['Total_Ingresos']], textposition='outside', textfont=dict(size=12)
    ))
    fig_grouped.add_trace(go.Bar(
        name='Prendas Habilitadas', x=df_daily_totals['Dia_Texto'], y=df_daily_totals['Habilitadas'], 
        marker_color='#7F97B2', yaxis='y',
        text=[f"<b>{int(val):,}</b>" for val in df_daily_totals['Habilitadas']], textposition='outside', textfont=dict(size=12)
    ))
    fig_grouped.add_trace(go.Scatter(
        name='% Real Habilitado', x=df_daily_totals['Dia_Texto'], y=df_daily_totals['Pct_Habilitado'],
        mode='lines+markers+text', text=df_daily_totals['Pct_Text'], textposition='top center',
        line=dict(color='#E6007E', width=5), marker=dict(size=12, symbol='diamond'), yaxis='y2',
        textfont=dict(size=13, color="#E6007E")
    ))
    fig_grouped.update_layout(
        barmode='group', plot_bgcolor="white", paper_bgcolor="white", height=540,
        margin=dict(l=50, r=60, t=40, b=50), legend=dict(orientation="h", y=1.09, x=0, font=dict(size=13)),
        yaxis=dict(title="Cantidad de Prendas (Barras)", title_font=dict(size=14), showgrid=True, gridcolor='#EFEFEF'),
        yaxis2=dict(title="% Real Habilitado (Línea)", title_font=dict(size=14), overlaying='y', side='right', range=[0, 130], showgrid=False)
    )
    fig_grouped.update_xaxes(title="Día", title_font=dict(size=14),
                             type='category', categoryorder='array', categoryarray=lista_dias_ordenados)
    st.plotly_chart(fig_grouped, use_container_width=True)


    # =========================================================================
    # --- NUEVA MATRIZ CON MULTI-ÍNDICE CON AGRUPACIÓN REAL ---
    # =========================================================================
    st.markdown('<p class="graph-title">🔍 Matriz General de Auditoría Operativa</p>', unsafe_allow_html=True)
    
    # Clonamos y ordenamos cronológicamente
    df_table = df_filtered.copy()
    df_table = df_table.sort_values(by=["Fecha", "Tienda"], ascending=[True, True])
    
    # Renombrado exacto de columnas para la interfaz corporativa
    df_table = df_table.rename(columns={
        "Dia_Texto": "Día",
        "Sis_Aduana": "Aduana Sist.",
        "Fis_Aduana": "Aduana Fís.",
        "Total_Ingresos": "Total Ingresos",
        "Habilitadas": "Piezas Habilitadas",
        "Eficiencia_Recorridos": "Ef. Recorridos %",
        "Porcentaje_Habilitado": "% Habilitado",
        "Porcentaje_Ubicado": "Ubicado %"
    })
    
    # Definición del esquema estricto de columnas solicitado
    cols_to_show = [
        "Día", "Tienda", "Aduana Sist.", "Aduana Fís.", "Muertos", "Cajas", 
        "Total Ingresos", "Piezas Habilitadas", "Ef. Recorridos %", "% Habilitado", "Ubicado %"
    ]
    
    df_subset = df_table[cols_to_show].copy()
    
    # ESTABLECER MULTIINDEX: Esto fuerza a Streamlit a agrupar la celda del Día verticalmente de forma real
    df_grouped_final = df_subset.set_index(["Día", "Tienda"])
    
    # Función de formato condicional (Semaforización corporativa)
    def apply_row_styles(val):
        try:
            val_float = float(str(val).replace('%', ''))
            if val_float < 85.0:
                return 'background-color: #FADBD8; color: #78281F; font-weight: bold; text-align: center;'
            elif val_float >= 100.0:
                return 'background-color: #D4E6F1; color: #1B4F72; font-weight: bold; text-align: center;'
            return 'text-align: center;'
        except:
            return 'text-align: center;'

    # Renderizado final aplicando Estilos de Tabla e Inyección de color Azul Énfasis 1 Oscuro (#1F497D)
    styled_matrix = df_grouped_final.style\
        .map(apply_row_styles, subset=["Ef. Recorridos %", "% Habilitado", "Ubicado %"])\
        .format({
            "Aduana Sist.": "{:,}",
            "Aduana Fís.": "{:,}",
            "Muertos": "{:,}",
            "Cajas": "{:,}",
            "Total Ingresos": "{:,}",
            "Piezas Habilitadas": "{:,}",
            "Ef. Recorridos %": "{:.1f}%",
            "% Habilitado": "{:.1f}%",
            "Ubicado %": "{:.1f}%"
        })\
        .set_properties(**{
            'text-align': 'center'
        })\
        .set_table_styles([
            {
                'selector': 'th',
                'props': [('background-color', '#1F497D'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center')]
            },
            {
                'selector': 'th.index_name',
                'props': [('background-color', '#1F497D'), ('color', 'white'), ('font-style', 'italic')]
            }
        ])

    st.dataframe(styled_matrix, use_container_width=True)

else:
    st.warning("No hay registros disponibles para los filtros seleccionados actualmente.")

st.markdown("<p style='font-size:12px; color:#999999;'>CONFIDENCIAL • Dirección de Operaciones Ropa Price Shoes.</p>", unsafe_allow_html=True)
