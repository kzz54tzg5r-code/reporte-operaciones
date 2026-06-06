import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE INTERFAZ GENERAL ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Estilos corporativos globales (Azul Énfasis 1 y Gris Obscuro)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estilos para Tarjetas de KPI */
    .kpi-card {
        background-color: #F8F9FA;
        border: 1px solid #D9D9D9;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .kpi-label { color: #555555; font-size: 13px; font-weight: bold; text-transform: uppercase; }
    .kpi-value { color: #1F497D; font-size: 26px; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET CONSOLIDADO OPERATIVO ---
@st.cache_data
def get_operational_data():
    data = [
        # Lunes 25
        {"Fecha": "2026-05-25", "Tienda": "Vallejo", "Sis_Aduana": 293, "Fis_Aduana": 332, "Muertos": 32, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 229, "Habilitadas": 248, "Ubicadas": 356},
        {"{"Fecha": "2026-05-25", "Tienda": "Arco Norte", "Sis_Aduana": 109, "Fis_Aduana": 82, "Muertos": 36, "Cajas": 73, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 109, "Habilitadas": 409, "Ubicadas": 545},
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

    # Cálculos Operativos
    df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
    df['Eficiencia_Recorridos'] = (df['Real_Rec'] / df['Meta_Rec']) * 100
    df['Porcentaje_Habilitado'] = (df['Habilitadas'] / df['Total_Ingresos']).fillna(0) * 100
    df['Porcentaje_Ubicado'] = (df['Ubicadas'] / df['Total_Ingresos']).fillna(0) * 100
    
    # Formateo de días
    dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
    df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
    
    return df

df = get_operational_data()

# --- HEADER GENERAL DE LA APLICACIÓN ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CONTROL DE ACONDICIONAMIENTO, SEGUIMIENTO DE RECORRIDOS Y MATRIZ DE PISO (SEM 21)</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

# --- FILTROS DE SIDEBAR ---
st.sidebar.markdown("### 🎛️ Filtros de Operación")
tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + list(df['Tienda'].unique()))

df_filtered = df.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

# =========================================================================
# --- SECCIÓN 1: TARJETAS DE INDICADORES (KPIs RESUMEN) ---
# =========================================================================
if not df_filtered.empty:
    total_ing = df_filtered['Total_Ingresos'].sum()
    total_hab = df_filtered['Habilitadas'].sum()
    avg_ef = df_filtered['Eficiencia_Recorridos'].mean()
    avg_ub = df_filtered['Porcentaje_Ubicado'].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">📥 Total Ingresos</p><p class="kpi-value">{total_ing:,}</p></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">✨ Piezas Habilitadas</p><p class="kpi-value">{total_hab:,}</p></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">🎯 Eficiencia Recorridos</p><p class="kpi-value">{avg_ef:.1f}%</p></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="kpi-card"><p class="kpi-label">📍 % Ubicado Total</p><p class="kpi-value">{avg_ub:.1f}%</p></div>', unsafe_allow_html=True)

# =========================================================================
# --- SECCIÓN 2: BLOQUE DE GRÁFICOS SOLICITADOS POR DÍA Y TIENDA ---
# =========================================================================
st.markdown('<p class="graph-title">📊 Gráficos de Rendimiento y Distribución Operativa</p>', unsafe_allow_html=True)

if not df_filtered.empty:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Gráfico 1: Piezas Habilitadas por Tienda
        df_g1 = df_filtered.groupby("Tienda")["Habilitadas"].sum().reset_index()
        fig1 = px.bar(df_g1, x="Tienda", y="Habilitadas", title="Piezas Habilitadas por Sucursal",
                     color_discrete_sequence=['#1F497D'])
        fig1.update_layout(plot_bgcolor='white', margin=dict(t=40, b=40, l=40, r=40))
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Evolución de Eficiencia del Recorridos por Día
        df_g2 = df_filtered.groupby(["Dia_Semana_Num", "Dia_Nombre"])["Eficiencia_Recorridos"].mean().reset_index()
        df_g2 = df_g2.sort_values("Dia_Semana_Num")
        fig2 = px.line(df_g2, x="Dia_Nombre", y="Eficiencia_Recorridos", title="Evolución % Eficiencia de Recorridos",
                      color_discrete_sequence=['#E6007E'], markers=True)
        fig2.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    with col_g2:
        # Gráfico 3: Desglose de Origen de Ingresos (Aduana, Muertos, Cajas)
        df_g3 = df_filtered.groupby("Tienda")[["Sis_Aduana", "Muertos", "Cajas"]].sum().reset_index()
        fig3 = px.bar(df_g3, x="Tienda", y=["Sis_Aduana", "Muertos", "Cajas"], title="Composición de Ingresos por Tienda",
                     color_discrete_sequence=['#1F497D', '#E6007E', '#7F7F7F'])
        fig3.update_layout(barmode='stack', plot_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Gráfico 4: Comparativo % Habilitado vs % Ubicado por Día
        df_g4 = df_filtered.groupby(["Dia_Semana_Num", "Dia_Nombre"])[["Porcentaje_Habilitado", "Porcentaje_Ubicado"]].mean().reset_index()
        df_g4 = df_g4.sort_values("Dia_Semana_Num")
        fig4 = px.bar(df_g4, x="Dia_Nombre", y=["Porcentaje_Habilitado", "Porcentaje_Ubicado"], title="% Habilitado vs Ubicado por Día",
                     barmode='group', color_discrete_sequence=['#1F497D', '#555555'])
        fig4.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig4, use_container_width=True)

# =========================================================================
# --- SECCIÓN 3: MATRIZ GENERAL DE AUDITORÍA OPERATIVA (HTML FIJO) ---
# =========================================================================
st.markdown('<p class="graph-title">🔍 Matriz General de Auditoría Operativa</p>', unsafe_allow_html=True)

if not df_filtered.empty:
    # Ordenamiento cronológico estricto de Lunes a Domingo
    df_table = df_filtered.sort_values(by=["Dia_Semana_Num", "Tienda"], ascending=[True, True]).copy()
    
    # Construcción estructurada de la tabla HTML
    html_table = """
    <table style="width:100%; border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; border: 1px solid #D9D9D9;">
        <thead>
            <tr style="background-color: #1F497D !important; color: #FFFFFF !important; font-weight: bold;">
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Día</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Tienda</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Aduana Sist.</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Aduana Fís.</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Muertos</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Cajas</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Total Ingresos</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Piezas Habilitadas</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Ef. Recorridos %</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">% Habilitado</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Ubicado %</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Agrupación dinámica por Día
    grouped_by_day = df_table.groupby("Dia_Nombre", sort=False)
    
    for dia, group in grouped_by_day:
        row_count = len(group)
        first_row = True
        
        for idx, row in group.iterrows():
            html_table += '<tr style="border-bottom: 1px solid #EFEFEF;">'
            
            if first_row:
                html_table += f'<td rowspan="{row_count}" style="padding: 10px; border: 1px solid #D9D9D9; font-weight: bold; text-align: center; background-color: #F9FBFD; color: #1F497D; vertical-align: middle;">{dia}</td>'
                first_row = False
                
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: 500;">{row["Tienda"]}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Sis_Aduana"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Fis_Aduana"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Muertos"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Cajas"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right; font-weight: bold; background-color: #F9F9F9;">{int(row["Total_Ingresos"]):,}</td>'
            
            # Orden de columnas exacto y cálculos dinámicos
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Habilitadas"]):,}</td>'
            
            # Ef. Recorridos con semáforo
            ef_rec = row["Eficiencia_Recorridos"]
            bg_ef = "#FADBD8" if ef_rec < 85.0 else ("#D4E6F1" if ef_rec >= 100.0 else "#FFFFFF")
            color_ef = "#78281F" if ef_rec < 85.0 else ("#1B4F72" if ef_rec >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_ef}; color: {color_ef};">{ef_rec:.1f}%</td>'
            
            # % Habilitado con semáforo
            pct_hab = row["Porcentaje_Habilitado"]
            bg_hab = "#FADBD8" if pct_hab < 85.0 else ("#D4E6F1" if pct_hab >= 100.0 else "#FFFFFF")
            color_hab = "#78281F" if pct_hab < 85.0 else ("#1B4F72" if pct_hab >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_hab}; color: {color_hab};">{pct_hab:.1f}%</td>'
            
            # Ubicado % con semáforo
            pct_ub = row["Porcentaje_Ubicado"]
            bg_ub = "#FADBD8" if pct_ub < 85.0 else ("#D4E6F1" if pct_ub >= 100.0 else "#FFFFFF")
            color_ub = "#78281F" if pct_ub < 85.0 else ("#1B4F72" if pct_ub >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_ub}; color: {color_ub};">{pct_ub:.1f}%</td>'
            
            html_table += '</tr>'
            
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.warning("No hay registros disponibles para los filtros seleccionados actualmente.")

st.markdown("<br><p style='font-size:12px; color:#999999;'>CONFIDENCIAL • Dirección de Operaciones Ropa Price Shoes.</p>", unsafe_allow_html=True)
