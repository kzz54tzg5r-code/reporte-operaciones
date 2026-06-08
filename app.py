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
    .tabla-auditoria td {
        padding: 10px 12px;
        border: 1px solid #3A3A42;
        text-align: left;
    }
    .tabla-auditoria tr:first-child {
        background-color: #1F3D63;
        color: #FFFFFF;
        font-weight: bold;
        font-size: 13px;
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
