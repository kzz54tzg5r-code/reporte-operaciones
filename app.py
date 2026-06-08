import streamlit as st
import pandas as pd
import numpy as np

# =========================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS CORPORATIVOS
# =========================================================================
st.set_page_config(
    page_title="Dashboard de Operaciones - Ropa",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS para la estética corporativa (Azul Énfasis, Fondo Gris Oscuro)
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E24;
        color: #E0E0E0;
    }
    .kpi-container {
        background-color: #25252D;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #1F3D63;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 13px;
        color: #A0A0A5;
        text-transform: uppercase;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
    }
    .graph-title {
        font-size: 16px;
        font-weight: bold;
        color: #6BE0FF;
        margin-top: 15px;
        margin-bottom: 10px;
        border-bottom: 1px solid #33333A;
        padding-bottom: 5px;
    }
    .tabla-auditoria {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        background-color: #25252D;
        color: #E0E0E0;
        border-radius: 6px;
        overflow: hidden;
    }
    .tabla-auditoria th {
        background-color: #1F3D63;
        color: #FFFFFF;
        font-weight: bold;
        font-size: 13px;
        padding: 12px;
        border: 1px solid #3A3A42;
        text-align: center;
    }
    .tabla-auditoria td {
        padding: 10px 12px;
        border: 1px solid #3A3A42;
        text-align: left;
    }
    .cell-center { text-align: center !important; }
    .cell-td { text-align: right !important; }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 2. GENERACIÓN DE DATOS DE PRUEBA (SIMULACIÓN MASTER)
# =========================================================================
@st.cache_data
def cargar_datos_master():
    semanas = ["Semana 19", "Semana 20", "Semana 21", "Semana 22"]
    tiendas = ["Tienda Centro", "Tienda Norte", "Tienda Sur", "Tienda Oeste"]
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    data = []
    np.random.seed(42)
    
    for sem in semanas:
        for tienda in tiendas:
            for dia in dias_semana:
                ingreso_aduana = np.random.randint(40000, 90000)
                muertos = np.random.randint(5000, 15000)
                cajas = np.random.randint(2000, 8000)
                
                # Regla de Negocio: Total Ingreso = Aduana Sistema + Muertos + Cajas
                total_ingresos = ingreso_aduana + muertos + cajas
                
                piezas_habilitadas = int(total_ingresos * np.random.uniform(0.70, 0.92))
                ubicadas = int(piezas_habilitadas * np.random.uniform(0.95, 1.0))
                
                meta_recorridos = np.random.randint(30, 50)
                real_recorridos = int(meta_recorridos * np.random.uniform(0.80, 1.02))
                
                data.append({
                    "Semana": sem,
                    "Tienda": tienda,
                    "Dia_Semana": dia,
                    "Ingreso_Aduana_Sistema": ingreso_aduana,
                    "Muertos": muertos,
                    "Cajas": cajas,
                    "Total_Ingresos": total_ingresos,
                    "Habilitadas": piezas_habilitadas,
                    "Ubicadas": ubicadas,
                    "Meta_Rec": meta_recorridos,
                    "Real_Rec": real_recorridos
                })
                
    return pd.DataFrame(data), semanas

df_master, ultimas_4_semanas = cargar_datos_master()

# =========================================================================
# 3. CONTROLADORES Y FILTROS (SIDEBAR)
# =========================================================================
st.sidebar.markdown("<h2 style='color: #6BE0FF; font-size: 20px;'>Filtros Operaciones Ropa</h2>", unsafe_allow_html=True)

lista_tiendas = ["Todas las Tiendas"] + list(df_master['Tienda'].unique())
tienda = st.sidebar.selectbox("Selecciona Tienda para el Análisis:", lista_tiendas)

if tienda != "Todas las Tiendas":
    df_filtrado = df_master[df_master['Tienda'] == tienda]
else:
    df_filtrado = df_master.copy()

semana_actual = ultimas_4_semanas[-1]
df_actual = df_filtrado[df_filtrado['Semana'] == semana_actual]

# =========================================================================
# 4. VISTA DE PANELES (TABS PRINCIPALES)
# =========================================================================
st.markdown(f"<h1 style='color: #FFFFFF; font-size: 26px; font-weight: 800; margin-bottom:5px;'>Reporte de Operaciones — Distribución Ropa</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #A0A0A5; font-size: 14px; margin-bottom: 25px;'>Monitoreo de flujo, eficiencias y procesamiento en piso de venta • <b>{semana_actual}</b></p>", unsafe_allow_html=True)

tab_resumen, tab_evolutivo = st.tabs(["📊 Resumen de la Semana Actual", "📈 Evolución Intersemanal"])

# -------------------------------------------------------------------------
# TAB 1: RESUMEN DE LA SEMANA ACTUAL
# -------------------------------------------------------------------------
with tab_resumen:
    total_ing = df_actual['Total_Ingresos'].sum()
    total_hab = df_actual['Habilitadas'].sum()
    pct_habilitado = (total_hab / total_ing * 100) if total_ing > 0 else 0
    
    meta_r = df_actual['Meta_Rec'].sum()
    real_r = df_actual['Real_Rec'].sum()
    eficiencia_recorrido = (real_r / meta_r * 100) if meta_r > 0 else 0
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">📥 Total Ingresos (Ropa)</div>
                <div class="kpi-value">{total_ing:,} <span style="font-size:13px; color:#A0A0A5;">uds</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">✨ Piezas Habilitadas</div>
                <div class="kpi-value">{total_hab:,} <span style="font-size:13px; color:#A0A0A5;">uds</span></div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">🧩 % Habilitado sobre Ingreso</div>
                <div class="kpi-value"><b>{pct_habilitado:.1f}%</b></div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi4:
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-title">🎯 Eficiencia del Recorrido</div>
                <div class="kpi-value"><b>{eficiencia_recorrido:.1f}%</b></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="graph-title">📅 Rendimiento Diario Agrupado de la Semana</p>', unsafe_allow_html=True)
    
    orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    df_diario = df_actual.groupby("Dia_Semana").agg({
        "Total_Ingresos": "sum",
        "Habilitadas": "sum",
        "Meta_Rec": "sum",
        "Real_Rec": "sum"
    }).reindex(orden_dias)
    
    chart_data = df_diario[['Total_Ingresos', 'Habilitadas']]
    st.bar_chart(chart_data, use_container_width=True)

# -------------------------------------------------------------------------
# TAB 2: EVOLUCIÓN INTERSEMANAL
# -------------------------------------------------------------------------
with tab_evolutivo:
    st.markdown('<p class="graph-title">📈 Análisis de Tendencia y Variación Intersemanal</p>', unsafe_allow_html=True)

    df_evolutivo = df_master[df_master['Semana'].isin(ultimas_4_semanas)].copy()
    if tienda != "Todas las Tiendas":
        df_evolutivo = df_evolutivo[df_evolutivo['Tienda'] == tienda]

    df_metrics_sem = df_evolutivo.groupby("Semana").agg({
        "Total_Ingresos": "sum", 
        "Habilitadas": "sum", 
        "Meta_Rec": "sum", 
        "Real_Rec": "sum"
    }).reindex(ultimas_4_semanas)

    df_metrics_sem['% Habilitado'] = (df_metrics_sem['Habilitadas'] / df_metrics_sem['Total_Ingresos'] * 100).fillna(0)
    df_metrics_sem['% Recorridos'] = (df_metrics_sem['Real_Rec'] / df_metrics_sem['Meta_Rec'] * 100).fillna(0)

    # Variaciones inter-semanales
    df_metrics_sem['Var_Ing_Abs'] = df_metrics_sem['Total_Ingresos'].diff()
    df_metrics_sem['Var_Ing_Pct'] = df_metrics_sem['Total_Ingresos'].pct_change() * 100
    df_metrics_sem['Var_Hab_Abs'] = df_metrics_sem['Habilitadas'].diff()
    df_metrics_sem['Var_Hab_Pct'] = df_metrics_sem['Habilitadas'].pct_change() * 100
    df_metrics_sem['Var_Delta_Recorridos'] = df_metrics_sem['% Recorridos'].diff()

    # Creación de la estructura HTML
    html_comparativo = """
    <table class="tabla-auditoria">
        <thead>
            <tr>
                <th>Dimensión Temporal</th>
                <th>📥 Vol. Ingresos Total</th>
                <th>Δ Vs. Sem Anterior</th>
                <th>✨ Piezas Habilitadas</th>
                <th>Δ Vs. Sem Anterior</th>
                <th>🎯 % Rendimiento Recorridos</th>
                <th>Δ Eficiencia Recorridos</th>
            </tr>
        </thead>
        <tbody>
    """

    for idx, (sem, row) in enumerate(df_metrics_sem.iterrows()):
        if idx == 0:
            delta_ing = '<span style="color:#888888; font-size:11px;">N/A (Base)</span>'
            delta_hab = '<span style="color:#888888; font-size:11px;">N/A</span>'
            delta_rec = '<span style="color:#888888; font-size:11px;">N/A</span>'
        else:
            c_ing = "#FF6B6B" if row['Var_Ing_Abs'] < 0 else "#6BE0FF"
            s_ing = "" if row['Var_Ing_Abs'] < 0 else "+"
            delta_ing = f'<b style="color:{c_ing};">{s_ing}{int(row["Var_Ing_Abs"]):,} u. ({s_ing}{row["Var_Ing_Pct"]:.1f}%)</b>'
            
            c_hab = "#FF6B6B" if row['Var_Hab_Abs'] < 0 else "#6BE0FF"
            s_hab = "" if row['Var_Hab_Abs'] < 0 else "+"
            delta_hab = f'<b style="color:{c_hab};">{s_hab}{int(row["Var_Hab_Abs"]):,} u. ({s_hab}{row["Var_Hab_Pct"]:.1f}%)</b>'
            
            c_rec = "#FF6B6B" if row['Var_Delta_Recorridos'] < 0 else "#2ECC71"
            s_rec = "" if row['Var_Delta_Recorridos'] < 0 else "+"
            delta_rec = f'<span style="color:{c_rec}; font-weight:bold;">{s_rec}{row["Var_Delta_Recorridos"]:.1f} pp</span>'

        html_comparativo += f"""
        <tr style="border-bottom: 1px solid #4A4A4A; height:38px;">
            <td class="cell-center" style="font-weight: bold; background-color: #1F3D63; color: #FFFFFF;">{sem}</td>
            <td class="cell-td" style="font-weight: bold;">{int(row['Total_Ingresos']):,}</td>
            <td class="cell-center" style="font-size:12px;">{delta_ing}</td>
            <td class="cell-td" style="font-weight: bold;">{int(row['Habilitadas']):,} <small style="color:#A0A0A5;">({row['% Habilitado']:.1f}%)</small></td>
            <td class="cell-center" style="font-size:12px;">{delta_hab}</td>
            <td class="cell-center" style="font-weight: bold; color: #FFFFFF;">{row['% Recorridos']:.1f}%</td>
            <td class="cell-center" style="font-size:12px;">{delta_rec}</td>
        </tr>
        """

    html_comparativo += "</tbody></table>"
    
    # Despliegue de la tabla HTML sin errores de cierre
    st.markdown(html_comparativo, unsafe_allow_html=True)
    
    # Gráfica lineal complementaria abajo
    st.markdown('<p class="graph-title">📈 Línea de Tendencia: Desempeño Operativo vs Volumen de Entrada</p>', unsafe_allow_html=True)
    df_chart = df_metrics_sem[['% Habilitado', '% Recorridos']]
    st.line_chart(df_chart, use_container_width=True)
