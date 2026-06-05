import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE INTERFAZ GENERAL ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Estilos corporativos globales (Azul Énfasis 1 Oscuro y Gris)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Nueva estructura de tarjetas apiladas por semana */
    .semana-header {
        background-color: #1F497D;
        color: white !important;
        font-weight: bold;
        text-align: center;
        padding: 6px;
        border-radius: 4px 4px 0 0;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 0px;
    }
    .kpi-card-nested {
        background-color: #F8F9FA;
        border-left: 1px solid #D9D9D9;
        border-right: 1px solid #D9D9D9;
        border-bottom: 1px solid #D9D9D9;
        border-radius: 0 0 4px 4px;
        padding: 12px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    .kpi-sub-block {
        border-bottom: 1px dashed #D9D9D9;
        padding: 6px 0;
    }
    .kpi-sub-block:last-child {
        border-bottom: none;
    }
    .kpi-label-nested { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .kpi-value-nested { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET CONSOLIDADO OPERATIVO HISTÓRICO ---
@st.cache_data
def get_operational_data():
    data = [
        # === DATOS DETALLADOS SEMANA 21 ===
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-25", "Tienda": "Vallejo", "Sis_Aduana": 293, "Fis_Aduana": 332, "Muertos": 32, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 229, "Habilitadas": 248, "Ubicadas": 356},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-25", "Tienda": "Arco Norte", "Sis_Aduana": 109, "Fis_Aduana": 82, "Muertos": 36, "Cajas": 73, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 109, "Habilitadas": 409, "Ubicadas": 545},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-25", "Tienda": "Puebla Sur", "Sis_Aduana": 79, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 185, "Ubicadas": 197},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-25", "Tienda": "Miravalle", "Sis_Aduana": 44, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-26", "Tienda": "Vallejo", "Sis_Aduana": 441, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 235, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 235, "Habilitadas": 595, "Ubicadas": 381},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-26", "Tienda": "Arco Norte", "Sis_Aduana": 164, "Fis_Aduana": 75, "Muertos": 30, "Cajas": 144, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 174, "Habilitadas": 201, "Ubicadas": 309},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-26", "Tienda": "Puebla Sur", "Sis_Aduana": 113, "Fis_Aduana": 108, "Muertos": 98, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 98, "Habilitadas": 116, "Ubicadas": 198},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-26", "Tienda": "Miravalle", "Sis_Aduana": 47, "Fis_Aduana": 37, "Muertos": 39, "Cajas": 17, "Meta_Rec": 5, "Real_Rec": 2, "Recolectadas": 39, "Habilitadas": 81, "Ubicadas": 129},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-27", "Tienda": "Vallejo", "Sis_Aduana": 436, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 3, "Recolectadas": 197, "Habilitadas": 478, "Ubicadas": 452},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-27", "Tienda": "Arco Norte", "Sis_Aduana": 170, "Fis_Aduana": 47, "Muertos": 51, "Cajas": 51, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 102, "Habilitadas": 171, "Ubicadas": 350},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-27", "Tienda": "Puebla Sur", "Sis_Aduana": 67, "Fis_Aduana": 65, "Muertos": 160, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 160, "Habilitadas": 307, "Ubicadas": 617},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-27", "Tienda": "Miravalle", "Sis_Aduana": 64, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-28", "Tienda": "Vallejo", "Sis_Aduana": 550, "Fis_Aduana": 563, "Muertos": 168, "Cajas": 224, "Meta_Rec": 8, "Real_Rec": 8, "Recolectadas": 392, "Habilitadas": 755, "Ubicadas": 452},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-28", "Tienda": "Arco Norte", "Sis_Aduana": 200, "Fis_Aduana": 134, "Muertos": 103, "Cajas": 75, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 178, "Habilitadas": 84, "Ubicadas": 350},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-28", "Tienda": "Puebla Sur", "Sis_Aduana": 131, "Fis_Aduana": 146, "Muertos": 103, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 103, "Habilitadas": 32, "Ubicadas": 617},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-28", "Tienda": "Miravalle", "Sis_Aduana": 57, "Fis_Aduana": 4, "Muertos": 31, "Cajas": 6, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 37, "Habilitadas": 0, "Ubicadas": 0},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-29", "Tienda": "Vallejo", "Sis_Aduana": 571, "Fis_Aduana": 596, "Muertos": 282, "Cajas": 196, "Meta_Rec": 5, "Real_Rec": 14, "Recolectadas": 503, "Habilitadas": 1017, "Ubicadas": 2099},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-29", "Tienda": "Arco Norte", "Sis_Aduana": 260, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 22, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 22, "Habilitadas": 0, "Ubicadas": 0},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-29", "Tienda": "Puebla Sur", "Sis_Aduana": 160, "Fis_Aduana": 152, "Muertos": 39, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 39, "Habilitadas": 226, "Ubicadas": 384},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-29", "Tienda": "Miravalle", "Sis_Aduana": 55, "Fis_Aduana": 7, "Muertos": 14, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 14, "Habilitadas": 58, "Ubicadas": 105},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-30", "Tienda": "Vallejo", "Sis_Aduana": 513, "Fis_Aduana": 0, "Muertos": 68, "Cajas": 363, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 431, "Habilitadas": 624, "Ubicadas": 611},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-30", "Tienda": "Arco Norte", "Sis_Aduana": 240, "Fis_Aduana": 246, "Muertos": 60, "Cajas": 115, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 175, "Habilitadas": 206, "Ubicadas": 1083},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-30", "Tienda": "Puebla Sur", "Sis_Aduana": 85, "Fis_Aduana": 70, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 70, "Ubicadas": 70},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-30", "Tienda": "Miravalle", "Sis_Aduana": 88, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-31", "Tienda": "Vallejo", "Sis_Aduana": 351, "Fis_Aduana": 351, "Muertos": 326, "Cajas": 488, "Meta_Rec": 8, "Real_Rec": 16, "Recolectadas": 884, "Habilitadas": 705, "Ubicadas": 2605},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-31", "Tienda": "Arco Norte", "Sis_Aduana": 264, "Fis_Aduana": 107, "Muertos": 57, "Cajas": 78, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 135, "Habilitadas": 784, "Ubicadas": 482},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-31", "Tienda": "Puebla Sur", "Sis_Aduana": 104, "Fis_Aduana": 110, "Muertos": 198, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 198, "Habilitadas": 340, "Ubicadas": 440},
        {"Mes": "Mayo", "Semana": "Semana 21", "Fecha": "2026-05-31", "Tienda": "Miravalle", "Sis_Aduana": 41, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},

        # === DATOS HISTÓRICOS ADICIONALES ===
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Vallejo", "Sis_Aduana": 3867, "Fis_Aduana": 2891, "Muertos": 869, "Cajas": 3144, "Meta_Rec": 47, "Real_Rec": 67, "Recolectadas": 4022, "Habilitadas": 5156, "Ubicadas": 513},
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Arco Norte", "Sis_Aduana": 1546, "Fis_Aduana": 511, "Muertos": 1366, "Cajas": 471, "Meta_Rec": 47, "Real_Rec": 21, "Recolectadas": 1837, "Habilitadas": 1866, "Ubicadas": 2994},
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Puebla Sur", "Sis_Aduana": 729, "Fis_Aduana": 501, "Muertos": 3579, "Cajas": 153, "Meta_Rec": 47, "Real_Rec": 63, "Recolectadas": 3723, "Habilitadas": 3434, "Ubicadas": 3544},
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Miravalle", "Sis_Aduana": 426, "Fis_Aduana": 311, "Muertos": 266, "Cajas": 692, "Meta_Rec": 47, "Real_Rec": 19, "Recolectadas": 368, "Habilitadas": 863, "Ubicadas": 348},

        {"Mes": "Mayo", "Semana": "Semana 20", "Fecha": "2026-05-17", "Tienda": "Vallejo", "Sis_Aduana": 3625, "Fis_Aduana": 2943, "Muertos": 1122, "Cajas": 1933, "Meta_Rec": 47, "Real_Rec": 83, "Recolectadas": 3101, "Habilitadas": 6332, "Ubicadas": 759},
        {"Mes": "Mayo", "Semana": "Semana 20", "Fecha": "2026-05-17", "Tienda": "Arco Norte", "Sis_Aduana": 1662, "Fis_Aduana": 1176, "Muertos": 660, "Cajas": 623, "Meta_Rec": 47, "Real_Rec": 33, "Recolectadas": 1292, "Habilitadas": 3221, "Ubicadas": 3451},
        {"Mes": "Mayo", "Semana": "Semana 20", "Fecha": "2026-05-17", "Tienda": "Puebla Sur", "Sis_Aduana": 870, "Fis_Aduana": 397, "Muertos": 2805, "Cajas": 458, "Meta_Rec": 47, "Real_Rec": 44, "Recolectadas": 2605, "Habilitadas": 2091, "Ubicadas": 2586},
        {"Mes": "Mayo", "Semana": "Semana 20", "Fecha": "2026-05-17", "Tienda": "Miravalle", "Sis_Aduana": 490, "Fis_Aduana": 257, "Muertos": 347, "Cajas": 9, "Meta_Rec": 47, "Real_Rec": 24, "Recolectadas": 347, "Habilitadas": 121, "Ubicadas": 1056},

        {"Mes": "Junio", "Semana": "Semana 22 (Corte)", "Fecha": "2026-06-01", "Tienda": "Vallejo", "Sis_Aduana": 291, "Fis_Aduana": 291, "Muertos": 331, "Cajas": 253, "Meta_Rec": 5, "Real_Rec": 12, "Recolectadas": 584, "Habilitadas": 736, "Ubicadas": 4313},
        {"Mes": "Junio", "Semana": "Semana 22 (Corte)", "Fecha": "2026-06-01", "Tienda": "Arco Norte", "Sis_Aduana": 99, "Fis_Aduana": 10, "Muertos": 301, "Cajas": 67, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 378, "Habilitadas": 364, "Ubicadas": 911},
        {"Mes": "Junio", "Semana": "Semana 22 (Corte)", "Fecha": "2026-06-01", "Tienda": "Puebla Sur", "Sis_Aduana": 82, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        {"Mes": "Junio", "Semana": "Semana 22 (Corte)", "Fecha": "2026-06-01", "Tienda": "Miravalle", "Sis_Aduana": 46, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0}
    ]
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
    
    # Agregar días estructurados en español
    dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
    df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
    
    return df

df_master = get_operational_data()

# --- TITULARES PRINCIPALES DEL DASHBOARD ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CONTROL DE ACONDICIONAMIENTO, SEGUIMIENTO DE RECORRIDOS Y MATRIZ DE PISO</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

# --- PANEL DE CONTROL (BARRA LATERAL) ---
st.sidebar.markdown("### 🎛️ Filtros de Operación")

tipo_periodo = st.sidebar.radio("Agrupar Reporte por:", ["Por Semana", "Por Mes"])

if tipo_periodo == "Por Semana":
    periodo_seleccionado = st.sidebar.selectbox("Selecciona la Semana Operativa:", sorted(list(df_master['Semana'].unique())))
    df_filtrado_periodo = df_master[df_master['Semana'] == periodo_seleccionado]
    label_corte = f"({periodo_seleccionado.upper()})"
else:
    periodo_seleccionado = st.sidebar.selectbox("Selecciona el Mes Operativo:", ["Mayo", "Junio"])
    df_filtrado_periodo = df_master[df_master['Mes'] == periodo_seleccionado]
    label_corte = f"(MES DE {periodo_seleccionado.upper()})"

tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + list(df_master['Tienda'].unique()))

df_filtered = df_filtrado_periodo.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

# --- VALIDACIÓN DE REGISTROS ---
if not df_filtered.empty:
    
    # =========================================================================
    # --- RESUMEN SUPERIOR: DESGLOSE COMPLETO DE LAS ÚLTIMAS 4 SEMANAS ---
    # =========================================================================
    st.markdown('<p style="color: #555555; font-weight: bold; font-size: 14px; margin-bottom: 10px; letter-spacing: 0.5px;">📋 DESGLOSE COMPARATIVO HISTÓRICO (ÚLTIMAS 4 SEMANAS)</p>', unsafe_allow_html=True)
    
    ultimas_4_semanas = ["Semana 19", "Semana 20", "Semana 21", "Semana 22 (Corte)"]
    
    # Columnas para acomodar horizontalmente cada semana
    cols_semanas = st.columns(4)
    
    for i, sem in enumerate(ultimas_4_semanas):
        # Filtrar datos de la semana específica
        df_sem = df_master[df_master['Semana'] == sem].copy()
        if tienda != "Todas las Tiendas":
            df_sem = df_sem[df_sem['Tienda'] == tienda]
            
        # Cálculos de indicadores para esa semana
        t_ing = df_sem['Total_Ingresos'].sum()
        t_hab = df_sem['Habilitadas'].sum()
        m_rec = df_sem['Meta_Rec'].sum()
        r_rec = df_sem['Real_Rec'].sum()
        
        ef_rec = (r_rec / m_rec * 100) if m_rec > 0 else 0.0
        p_ub = (df_sem['Ubicadas'].sum() / t_ing * 100) if t_ing > 0 else 0.0
        
        # Renderizado de la tarjeta estructurada verticalmente en su columna
        with cols_semanas[i]:
            st.markdown(f'<p class="semana-header">{sem}</p>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="kpi-card-nested">
                    <div class="kpi-sub-block">
                        <p class="kpi-label-nested">📥 Total Ingresos</p>
                        <p class="kpi-value-nested">{t_ing:,}</p>
                    </div>
                    <div class="kpi-sub-block">
                        <p class="kpi-label-nested">✨ Piezas Habilitadas</p>
                        <p class="kpi-value-nested">{t_hab:,}</p>
                    </div>
                    <div class="kpi-sub-block">
                        <p class="kpi-label-nested">🎯 % de Recorridos</p>
                        <p class="kpi-value-nested">{ef_rec:.1f}%</p>
                    </div>
                    <div class="kpi-sub-block">
                        <p class="kpi-label-nested">📍 % Ubicado Total</p>
                        <p class="kpi-value-nested">{p_ub:.1f}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # =========================================================================
    # --- SECCIÓN 2: MATRIZ GRÁFICA PARALELA (DINÁMICA AL FILTRO DE PERIODO) ---
    # =========================================================================
    st.markdown(f'<p class="graph-title">📊 Gráficos de Rendimiento y Distribución Operativa {label_corte}</p>', unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Gráfico 1: Piezas Habilitadas por Tienda
        df_g1 = df_filtered.groupby("Tienda")["Habilitadas"].sum().reset_index()
        fig1 = px.bar(df_g1, x="Tienda", y="Habilitadas", title="Piezas Habilitadas por Sucursal",
                     color_discrete_sequence=['#1F497D'], text_auto='.3s')
        fig1.update_layout(plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Evolución del recorrido (% de Recorridos)
        if tipo_periodo == "Por Semana":
            df_g2 = df_filtered.groupby(["Dia_Semana_Num", "Dia_Nombre"]).apply(
                lambda x: pd.Series({'Eficiencia': (x['Real_Rec'].sum() / x['Meta_Rec'].sum() * 100) if x['Meta_Rec'].sum() > 0 else 0})
            ).reset_index().sort_values("Dia_Semana_Num")
            eje_x_g2 = "Dia_Nombre"
            titulo_g2 = "Evolución % de Recorridos por Día"
        else:
            df_g2 = df_filtered.groupby("Semana").apply(
                lambda x: pd.Series({'Eficiencia': (x['Real_Rec'].sum() / x['Meta_Rec'].sum() * 100) if x['Meta_Rec'].sum() > 0 else 0})
            ).reset_index()
            eje_x_g2 = "Semana"
            titulo_g2 = "Evolución % de Recorridos por Semana"

        fig2 = px.line(df_g2, x=eje_x_g2, y="Eficiencia", title=titulo_g2,
                      color_discrete_sequence=['#E6007E'], markers=True)
        fig2.update_layout(plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    with col_g2:
        # Gráfico 3: Composición de Desglose de Ingresos
        df_g3 = df_filtered.groupby("Tienda")[["Sis_Aduana", "Muertos", "Cajas"]].sum().reset_index()
        fig3 = px.bar(df_g3, x="Tienda", y=["Sis_Aduana", "Muertos", "Cajas"], title="Composición de Ingresos por Tienda",
                     color_discrete_sequence=['#1F497D', '#E6007E', '#7F7F7F'])
        fig3.update_layout(barmode='stack', plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig3, use_container_width=True)
        
        # Gráfico 4: % Habilitado vs Ingreso Total
        if tipo_periodo == "Por Semana":
            df_g4 = df_filtered.groupby(["Dia_Semana_Num", "Dia_Nombre"]).apply(
                lambda x: pd.Series({
                    'Porcentaje_Habilitado': (x['Habilitadas'].sum() / x['Total_Ingresos'].sum() * 100) if x['Total_Ingresos'].sum() > 0 else 0,
                    'Porcentaje_Ubicado': (x['Ubicadas'].sum() / x['Total_Ingresos'].sum() * 100) if x['Total_Ingresos'].sum() > 0 else 0
                })
            ).reset_index().sort_values("Dia_Semana_Num")
            eje_x_g4 = "Dia_Nombre"
            titulo_g4 = "% Habilitado vs Ubicado por Día"
        else:
            df_g4 = df_filtered.groupby("Semana").apply(
                lambda x: pd.Series({
                    'Porcentaje_Habilitado': (x['Habilitadas'].sum() / x['Total_Ingresos'].sum() * 100) if x['Total_Ingresos'].sum() > 0 else 0,
                    'Porcentaje_Ubicado': (x['Ubicadas'].sum() / x['Total_Ingresos'].sum() * 100) if x['Total_Ingresos'].sum() > 0 else 0
                })
            ).reset_index()
            eje_x_g4 = "Semana"
            titulo_g4 = "% Habilitado vs Ubicado por Semana"

        fig4 = px.bar(df_g4, x=eje_x_g4, y=["Porcentaje_Habilitado", "Porcentaje_Ubicado"], title=titulo_g4,
                     barmode='group', color_discrete_sequence=['#1F497D', '#555555'])
        fig4.update_layout(plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig4, use_container_width=True)

    # =========================================================================
    # --- SECCIÓN 3: MATRIZ GENERAL DE AUDITORÍA OPERATIVA ---
    # =========================================================================
    st.markdown(f'<p class="graph-title">🔍 Matriz General de Auditoría Operativa {label_corte}</p>', unsafe_allow_html=True)

    html_table = """
    <table style="width:100%; border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; border: 1px solid #D9D9D9;">
        <thead>
            <tr style="background-color: #1F497D !important; color: #FFFFFF !important; font-weight: bold;">
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Clasificación</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Tienda</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Aduana Sist.</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Aduana Fís.</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Muertos</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Cajas</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Total Ingresos</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Piezas Habilitadas</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">% Recorridos</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">% Habilitado</th>
                <th style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; color: white;">Ubicado %</th>
            </tr>
        </thead>
        <tbody>
    """
    
    if tipo_periodo == "Por Semana":
        df_table = df_filtered.sort_values(by=["Dia_Semana_Num", "Tienda"]).copy()
        grouped_matrix = df_table.groupby("Dia_Nombre", sort=False)
    else:
        df_table = df_filtered.sort_values(by=["Semana", "Tienda"]).copy()
        grouped_matrix = df_table.groupby("Semana", sort=False)
    
    for bloque_id, sub_grupo in grouped_matrix:
        limite_filas = len(sub_grupo)
        es_primera_fila = True
        
        for index, row in sub_grupo.iterrows():
            html_table += '<tr style="border-bottom: 1px solid #EFEFEF;">'
            
            if es_primera_fila:
                html_table += f'<td rowspan="{limite_filas}" style="padding: 10px; border: 1px solid #D9D9D9; font-weight: bold; text-align: center; background-color: #F9FBFD; color: #1F497D; vertical-align: middle;">{bloque_id}</td>'
                es_primera_fila = False
                
            total_ing_fila = row["Total_Ingresos"]
            
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: 500;">{row["Tienda"]}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Sis_Aduana"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Fis_Aduana"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Muertos"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Cajas"]):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right; font-weight: bold; background-color: #F9F9F9;">{int(total_ing_fila):,}</td>'
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: right;">{int(row["Habilitadas"]):,}</td>'
            
            # Semáforos analíticos
            val_ef = (row["Real_Rec"] / row["Meta_Rec"] * 100) if row["Meta_Rec"] > 0 else 0
            bg_ef = "#FADBD8" if val_ef < 85.0 else ("#D4E6F1" if val_ef >= 100.0 else "#FFFFFF")
            tx_ef = "#78281F" if val_ef < 85.0 else ("#1B4F72" if val_ef >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_ef}; color: {tx_ef};">{val_ef:.1f}%</td>'
            
            val_hab = (row["Habilitadas"] / total_ing_fila * 100) if total_ing_fila > 0 else 0
            bg_hab = "#FADBD8" if val_hab < 85.0 else ("#D4E6F1" if val_hab >= 100.0 else "#FFFFFF")
            tx_hab = "#78281F" if val_hab < 85.0 else ("#1B4F72" if val_hab >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_hab}; color: {tx_hab};">{val_hab:.1f}%</td>'
            
            val_ub = (row["Ubicadas"] / total_ing_fila * 100) if total_ing_fila > 0 else 0
            bg_ub = "#FADBD8" if val_ub < 85.0 else ("#D4E6F1" if val_ub >= 100.0 else "#FFFFFF")
            tx_ub = "#78281F" if val_ub < 85.0 else ("#1B4F72" if val_ub >= 100.0 else "#000000")
            html_table += f'<td style="padding: 10px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold; background-color: {bg_ub}; color: {tx_ub};">{val_ub:.1f}%</td>'
            
            html_table += '</tr>'
            
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.warning("No se encontraron registros de operaciones de ropa con los filtros aplicados.")

st.markdown("<br><p style='font-size:11px; color:#999999; text-align: center;'>REPORTES DE DIRECCIÓN DE OPERACIONES • PRICE SHOES ROPA • CONFIDENCIAL</p>", unsafe_allow_html=True)
