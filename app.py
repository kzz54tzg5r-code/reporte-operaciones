import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURACIÓN DE INTERFAZ GENERAL ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Estilos corporativos globales (Azul Énfasis 1 Oscuro y Gris)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estructura optimizada de tarjetas semanales compactas */
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
        padding: 10px 14px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    .kpi-sub-block {
        border-bottom: 1px dashed #D9D9D9;
        padding: 8px 0;
    }
    .kpi-sub-block:last-child {
        border-bottom: none;
    }
    .kpi-label-nested { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .kpi-value-nested { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; }
    .kpi-value-inline { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; display: inline-block; }
    .kpi-pct-inline { color: #E6007E; font-size: 15px; font-weight: bold; margin-left: 8px; display: inline-block; }
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
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Vallejo", "Sis_Aduana": 2891, "Fis_Aduana": 2891, "Muertos": 869, "Cajas": 3144, "Meta_Rec": 47, "Real_Rec": 67, "Recolectadas": 4022, "Habilitadas": 5156, "Ubicadas": 513},
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Arco Norte", "Sis_Aduana": 511, "Fis_Aduana": 511, "Muertos": 1366, "Cajas": 471, "Meta_Rec": 47, "Real_Rec": 21, "Recolectadas": 1837, "Habilitadas": 1866, "Ubicadas": 2994},
        {"Mes": "Mayo", "Semana": "Semana 19", "Fecha": "2026-05-10", "Tienda": "Puebla Sur", "Sis_Aduana": 501, "Fis_Aduana": 501,
