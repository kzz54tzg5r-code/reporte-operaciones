import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURACIÓN DE INTERFAZ GENERAL ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Estilos corporativos globales (Incluye la corrección definitiva para el encabezado de la tabla)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estructura de tarjetas semanales compactas */
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

    /* REGLAS CSS DEFINITIVAS PARA SOLUCIONAR LOS ENCABEZADOS EN BLANCO EN STREAMLIT */
    .tabla-auditoria {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        border: 1px solid #D9D9D9 !important;
    }
    /* Forzar el color de fondo en la primera fila (encabezado alternativo seguro) */
    .tabla-auditoria tr:first-child {
        background-color: #1F497D !important;
        color: #FFFFFF !important;
        height: 42px;
    }
    /* Forzar el color de fondo y de texto en cada celda del encabezado de forma estricta */
    .tabla-auditoria tr:first-child td {
        background-color: #1F497D !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 10px;
        border: 1px solid #D9D9D9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATASET CONSOLIDADO OPERATIVO HISTÓRICO ---
@st.cache_data
def get_
