import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main-title { color: #000000; font-family: 'Arial', sans-serif; font-size: 34px; font-weight: 800; }
    .sub-title { color: #E6007E; font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; text-transform: uppercase; }
    .graph-title { color: #1F497D; font-weight: bold; font-size: 18px; border-left: 5px solid #1F497D; padding-left: 10px; margin-top: 25px; }
    .tabla-auditoria { width: 100%; border-collapse: collapse; font-size: 13px; }
    .tabla-auditoria tr:first-child { background-color: #1F497D; color: #FFFFFF; }
    .cell-td { padding: 10px; border: 1px solid #D9D9D9; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# --- LECTURA DE DATOS ---
@st.cache_data(ttl=60)
def get_operational_data():
    try:
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        response = requests.get(URL, timeout=30)
        excel_file = pd.ExcelFile(io.BytesIO(response.content), engine="openpyxl")
        
        lista_dataframes = []
        for nombre_pestana in [p for p in excel_file.sheet_names if p.strip().lower().startswith("sem")]:
            # Buscador inteligente de fila de cabecera
            df_temp = pd.read_excel(excel_file, sheet_name=nombre_pestana, header=None)
            fila_cabecera = 0
            for idx in range(min(12, len(df_temp))):
                if "Tienda" in df_temp.iloc[idx].astype(str).values:
                    fila_cabecera = idx
                    break
            
            df = pd.read_excel(excel_file, sheet_name=nombre_pestana, skiprows=fila_cabecera)
            df.columns = df.columns.str.strip()
            
            # Limpieza básica
            df = df[df['Tienda'].notna()]
            df = df[~df['Tienda'].astype(str).str.contains('total|resumen', case=False, na=False)]
            df['Semana'] = nombre_pestana
            
            # Asegurar columnas numéricas
            cols = ['Ingreso Aduana (sistema)', 'Ingresos Muertos', 'Ingresos Cajas', 'Pzas Habilitadas']
            for c in cols:
                if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            
            lista_dataframes.append(df)
            
        return pd.concat(lista_dataframes, ignore_index=True)
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- INTERFAZ PRINCIPAL ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
df_master = get_operational_data()

if not df_master.empty:
    tienda = st.sidebar.selectbox("Sucursal", ["Todas"] + sorted(df_master['Tienda'].unique().tolist()))
    df_f = df_master if tienda == "Todas" else df_master[df_master['Tienda'] == tienda]
    
    # Gráfico ejemplo corregido
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df_f['Tienda'], y=df_f['Pzas Habilitadas'], name="Habilitadas", marker_color='#1F497D'))
    fig1.update_layout(title="<b>Rendimiento Habilitación</b>", plot_bgcolor='white')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Cargando datos... asegúrate de que el documento esté compartido.")
