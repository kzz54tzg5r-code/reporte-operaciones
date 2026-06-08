import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
    # Cargamos todas las hojas para ver qué tenemos
    all_sheets = pd.read_excel(url, sheet_name=None)
    
    # Debug: Mostrar nombres de hojas y columnas para identificar la causa del error
    st.write("### Diagnóstico de Datos:")
    for name, df in all_sheets.items():
        st.write(f"Hoja '{name}' tiene columnas: {df.columns.tolist()}")
    
    return all_sheets

st.title("Price Shoes - Reparación de Dashboard")
data_sheets = load_data()

# Instrucción para el usuario
st.info("""
1. Observa la lista de columnas de arriba.
2. Busca si las columnas que necesitas (como 'Total ingresos', 'Pzas Habilitadas', etc.) aparecen ahí exactamente con ese nombre.
3. Si los nombres son diferentes (ejemplo: 'Total ingresos ' con un espacio extra al final), por favor **dímelo aquí** para ajustar el código exactamente a tus nombres reales.
""")
