import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE INTERFAZ CORPORATIVA ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Forzar paleta corporativa mediante CSS (Azul #1F497D y Gris #D9D9D9)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    h1 { color: #1F497D !important; font-family: 'Arial Black', Gadget, sans-serif; font-size: 30px !important; margin-bottom: 5px; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: bold; color: #1F497D !important; }
    /* Ajuste para evitar que los contenedores de gráficos colapsen */
    div[data-testid="stColumn"] { padding: 10px !important; }
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

    # Métricas calculadas
    df['Total_Ingresos'] = df['Fis_Aduana'] + df['Muertos'] + df['Cajas']
    df['Eficiencia_Recorridos'] = (df['Real_Rec'] / df['Meta_Rec']) * 100
    df['Utilizacion_Habilitado'] = ((df['Habilitadas'] / df['Recolectadas']).replace([float('inf'), -float('inf')], 0).fillna(0) * 100)
    df['Porcentaje_Ubicado'] = ((df['Ubicadas'] / df['Recolectadas']).replace([float('inf'), -float('inf')], 0).fillna(0) * 100)
    
    df['Dia_Texto'] = df['Fecha'].dt.strftime('%a %d')
    return df

df = get_operational_data()

# --- HEADER ---
st.markdown("<h1>👚 PRICE SHOES • Operaciones ropa</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#1F497D; font-size:16px; font-weight:bold; margin-top:-10px;'>Proceso de Muertos y cambios (Semana 21)</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 2px; background: #1F497D; margin-top:0px; margin-bottom:15px;'>", unsafe_allow_html=True)

# --- FILTROS SIDEBAR ---
st.sidebar.markdown("### 🎛️ Filtros de Operación")
tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + list(df['Tienda'].unique()))

min_date = df['Fecha'].min().date()
max_date = df['Fecha'].max().date()
fecha_rango = st.sidebar.date_input("Rango Temporal", [min_date, max_date])

# Aplicar filtros
df_filtered = df.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

if len(fecha_rango) == 2:
    start_date, end_date = fecha_rango
    df_filtered = df_filtered[(df_filtered['Fecha'].dt.date >= start_date) & (df_filtered['Fecha'].dt.date <= end_date)]

# --- TARJETAS KPI ---
if not df_filtered.empty:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#D9D9D9; border-left: 6px solid #1F497D;'><strong>Pzas Ropa Ingresadas</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:,}</span></div>".format(df_filtered['Total_Ingresos'].sum()), unsafe_allow_html=True)
    with kpi_col2:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#F0F4F8; border-left: 6px solid #1F497D;'><strong>Eficiencia Recorridos Prom.</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:.1f}%</span></div>".format(df_filtered['Eficiencia_Recorridos'].mean()), unsafe_allow_html=True)
    with kpi_col3:
        st.markdown("<div style='padding:12px; border-radius:4px; background-color:#D9D9D9; border-left: 6px solid #1F497D;'><strong>Prendas Ubicadas (Piso)</strong><br><span style='font-size:24px; font-weight:bold; color:#1F497D;'>{:,}</span></div>".format(df_filtered['Ubicadas'].sum()), unsafe_allow_html=True)
    with kpi_col4:
        diff_aduana = df_filtered['Fis_Aduana'].sum() - df_filtered['Sis_Aduana'].sum()
        status_color = "#27AE60" if diff_aduana >= 0 else "#C0392B"
        st.markdown(f"<div style='padding:12px; border-radius:4px; background-color:#F0F4F8; border-left: 6px solid {status_color};'><strong>Desviación Aduana Ropa</strong><br><span style='font-size:24px; font-weight:bold; color:{status_color};'>{diff_aduana:+,}</span></div>", unsafe_allow_html=True)

    st.write("")

    # --- BLOQUE DE GRÁFICOS COMPLETO (REDISEÑO TOTAL DE ESPACIOS) ---
    col1, col2 = st.columns(2)

    with col1:
        fig_line = px.line(
            df_filtered.sort_values("Fecha"), 
            x="Dia_Texto", y="Eficiencia_Recorridos", color="Tienda",
            markers=True,
            color_discrete_sequence=["#1F497D", "#5B9BD5", "#7F97B2", "#A6A6A6"]
        )
        # Título integrado internamente en Plotly para evitar cortes CSS
        fig_line.update_layout(
            title={"text": "📈 Tendencia de Eficiencia de Recorridos por Día", "font": {"size": 16, "color": "#1F497D"}},
            plot_bgcolor="white", paper_bgcolor="white", height=420,
            margin=dict(l=40, r=20, t=60, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        fig_line.update_xaxes(showgrid=True, gridcolor='#D9D9D9', title="Día del Proceso")
        fig_line.update_yaxes(showgrid=True, gridcolor='#D9D9D9', title="% Eficiencia")
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        fig_stack = px.bar(
            df_filtered.sort_values("Fecha"),
            x="Dia_Texto", y="Total_Ingresos", color="Tienda",
            color_discrete_sequence=["#1F497D", "#5B9BD5", "#7F97B2", "#A6A6A6"]
        )
        fig_stack.update_layout(
            title={"text": "📦 Volumen Total de Ingresos (Carga Operativa por Día)", "font": {"size": 16, "color": "#1F497D"}},
            barmode="stack", plot_bgcolor="white", paper_bgcolor="white", height=420,
            margin=dict(l=40, r=20, t=60, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        fig_stack.update_xaxes(showgrid=True, gridcolor='#D9D9D9', title="Día")
        fig_stack.update_yaxes(showgrid=True, gridcolor='#D9D9D9', title="Prendas Totales")
        st.plotly_chart(fig_stack, use_container_width=True)

    # --- SEGUNDA FILA DE GRÁFICOS ---
    col3, col4 = st.columns(2)

    with col3:
        df_tienda = df_filtered.groupby("Tienda").mean(numeric_only=True).reset_index()
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_tienda['Tienda'], x=df_tienda['Eficiencia_Recorridos'],
            name='% Eficiencia Recorridos', orientation='h', marker_color='#1F497D'
        ))
        fig_bar.add_trace(go.Bar(
            y=df_tienda['Tienda'], x=df_tienda['Porcentaje_Ubicado'],
            name='% Comercial Ubicado', orientation='h', marker_color='#7F97B2'
        ))
        fig_bar.update_layout(
            title={"text": "🎯 Eficiencia Global Promedio por Sucursal", "font": {"size": 16, "color": "#1F497D"}},
            barmode='group', plot_bgcolor="white", paper_bgcolor="white", height=420,
            margin=dict(l=40, r=20, t=60, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor='#D9D9D9')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col4:
        fig_scatter = px.scatter(
            df_filtered, x="Ubicadas", y="Porcentaje_Ubicado", color="Tienda", 
            size="Total_Ingresos", text="Dia_Texto",
            color_discrete_sequence=["#1F497D", "#5B9BD5", "#7F97B2", "#A6A6A6"]
        )
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(
            title={"text": "🔍 Dispersión: Relación de Prendas Ubicadas vs Éxito de Piso", "font": {"size": 16, "color": "#1F497D"}},
            plot_bgcolor="white", paper_bgcolor="white", height=420,
            margin=dict(l=40, r=20, t=60, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        fig_scatter.update_xaxes(showgrid=True, gridcolor='#D9D9D9', title="Cantidad de Prendas en Piso")
        fig_scatter.update_yaxes(showgrid=True, gridcolor='#D9D9D9', title="% Éxito Ubicación")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- MATRIZ DE AUDITORÍA ---
    st.markdown("#### 🔍 Matriz General de Auditoría Operativa")
    st.dataframe(
        df_filtered.sort_values("Fecha", ascending=False),
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha Operación"),
            "Tienda": "Sucursal",
            "Sis_Aduana": "Aduana (Sist)",
            "Fis_Aduana": "Aduana (Fís)",
            "Muertos": "Muertos",
            "Cajas": "Cajas",
            "Total_Ingresos": "Total Ingresos",
            "Eficiencia_Recorridos": st.column_config.ProgressColumn(
                "Eficiencia Recorridos", format="%.0f%%", min_value=0, max_value=280, color="gray"
            ),
            "Utilizacion_Habilitado": st.column_config.NumberColumn(
                "Utilización Habilitado", format="%.1f%%"
            ),
            "Porcentaje_Ubicado": st.column_config.ProgressColumn(
                "% Ubicado (Éxito)", format="%.0f%%", min_value=0, max_value=260, color="#1F497D"
            ),
            "Ubicadas": "Prendas en Piso"
        }, hide_index=True, use_container_width=True
    )
else:
    st.warning("No hay registros disponibles para los filtros seleccionados actualmente.")

st.markdown("<p style='font-size:12px; color:#999999;'>CONFIDENCIAL • Dirección de Operaciones Ropa Price Shoes.</p>", unsafe_allow_html=True)
