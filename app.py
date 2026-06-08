import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================================
# --- CONFIGURACIÓN DE INTERFAZ GENERAL Y ESTILOS CORPORATIVOS ---
# =========================================================================
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Inyección de CSS para un entorno corporativo limpio con fondos y tipografías específicas
st.markdown("""
    <style>
    .reportview-container { background-color: #F4F6F7; }
    .main-title { color: #1F497D !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estructura de tarjetas semanales compactas */
    .semana-header { background-color: #1F497D; color: white !important; font-weight: bold; text-align: center; padding: 8px; border-radius: 4px 4px 0 0; font-size: 14px; text-transform: uppercase; margin-bottom: 0px; }
    .kpi-card-nested { background-color: #FFFFFF; border-left: 1px solid #D9D9D9; border-right: 1px solid #D9D9D9; border-bottom: 1px solid #D9D9D9; border-radius: 0 0 4px 4px; padding: 10px 14px; text-align: center; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .kpi-sub-block { border-bottom: 1px dashed #E5E7E9; padding: 8px 0; }
    .kpi-sub-block:last-child { border-bottom: none; }
    .kpi-label-nested { color: #5D6D7E; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .kpi-value-nested { color: #1F497D; font-size: 20px; font-weight: bold; margin: 0; }
    .kpi-value-inline { color: #1F497D; font-size: 20px; font-weight: bold;
