import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================================
# --- CONFIGURACIÓN DE INTERFAZ GENERAL Y ESTILOS CORPORATIVOS ---
# =========================================================================
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Reglas CSS Globales (Inyección del color Azul Énfasis 1 Oscuro 25%: #1F497D)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estructura de tarjetas semanales compactas */
    .semana-header { background-color: #1F497D; color: white !important; font-weight: bold; text-align: center; padding: 6px; border-radius: 4px 4px 0 0; font-size: 14px; text-transform: uppercase; margin-bottom: 0px; }
    .kpi-card-nested { background-color: #F8F9FA; border-left: 1px solid #D9D9D9; border-right: 1px solid #D9D9D9; border-bottom: 1px solid #D9D9D9; border-radius: 0 0 4px 4px; padding: 10px 14px; text-align: center; box-shadow: 0px 2px 4px rgba(0,0,0,0.03); margin-bottom: 15px; }
    .kpi-sub-block { border-bottom: 1px dashed #D9D9D9; padding: 8px 0; }
    .kpi-sub-block:last-child { border-bottom: none; }
    .kpi-label-nested { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .kpi-value-nested { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; }
    .kpi-value-inline { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; display: inline-block; }
    .kpi-pct-inline { color: #E6007E; font-size: 15px; font-weight: bold; margin-left: 8px; display: inline-block; }

    /* REGLAS CSS PARA TABLAS */
    .tabla-auditoria { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; border: 1px solid #D9D9D9 !important; }
    .tabla-auditoria tr:first-child { background-color: #1F497D !important; color: #FFFFFF !important; height: 42px; }
    .tabla-auditoria tr:first-child td { background-color: #1F497D !important; color: #FFFFFF !important; font-weight: bold !important; text-align: center !important; padding: 10px; border: 1px solid #D9D9D9 !important; }
    .cell-td { padding: 10px; border: 1px solid #D9D9D9; text-align: right; }
    .cell-center { padding: 10px; border: 1px solid #D9D9D9; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (ONEDRIVE PERSONAL) ---
# =========================================================================
@st.cache_data(ttl=300)  # El caché se actualizará automáticamente cada 5 minutos
def get_operational_data():
    try:
        # Enlace de descarga directa del binario limpio
        URL_ONEDRIVE = "https://onedrive.live.com/download?resid=11B83163-6E2D-4B29-A4C2-9D0A3BB17B97"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, */*"
        }
        
        # 1. Descarga del flujo binario crudo desde la nube
        response = requests.get(URL_ONEDRIVE, headers=headers, timeout=25)
        response.raise_for_status()
        excel_bytes = io.BytesIO(response.content)
        
        # 2. Lectura directa forzando el motor openpyxl para la pestaña transaccional
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        if df.empty:
            return pd.DataFrame()

        # --- LIMPIEZA DE ESPACIOS OCULTOS EN ENCABEZADOS ---
        df.columns = df.columns.str.strip()
        
        # --- RE-MAPEO DE COLUMNAS SEGÚN TU EXCEL REAL ---
        df.rename(columns={
            'Fecha s': 'Fecha_Corte',
            'Ubicación': 'Tienda',
            'Motivo de ingreso': 'Motivo_Ingreso',
            'Número de Piezas': 'Piezas'
        }, inplace=True)
        
        # 3. Validar la columna de tiempo (usamos la fecha de registro limpia)
        df['Fecha'] = pd.to_datetime(df['Fecha_Corte'], errors='coerce')
        df = df.dropna(subset=['Fecha'])
        
        # 4. Forzar que las piezas sean numéricas puras (evita caídas por celdas vacías)
        df['Piezas'] = pd.to_numeric(df['Piezas'], errors='coerce').fillna(0)
        
        # 5. Pivotación Dinámica: Mapear filas según las reglas de tu negocio de ropa
        df['Sis_Aduana'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Aduana' else 0, axis=1)
        df['Muertos'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Muertos' else 0, axis=1)
        df['Cajas'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Cajas' else 0, axis=1)
        
        # Búsqueda parcial e insensible a mayúsculas para las actividades realizadas
        df['Habilitadas'] = df.apply(lambda r: r['Piezas'] if 'habilitad' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        df['Ubicadas'] = df.apply(lambda r: r['Piezas'] if 'ubica' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        
        # Control de recorridos de validación por sucursal
        df['Meta_Rec'] = 8.0  
        df['Real_Rec'] = df.apply(lambda r: 1.0 if 'recorrido' in str(r.get('Tabla', '')).lower() else 0, axis=1)
        
        # Regla de negocio: El ingreso total consolida sistema, muertos y cajas
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # 6. Agrupación por días de la semana en español evitando duplicados
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "
