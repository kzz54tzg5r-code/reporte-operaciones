import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
    all_sheets = pd.read_excel(url, sheet_name=None)
    
    # Normalizamos nombres de columnas para evitar el KeyError
    clean_sheets = {}
    for name, df in all_sheets.items():
        # Limpiamos nombres: quitamos espacios extra y convertimos a minúsculas para comparar
        df.columns = df.columns.str.strip()
        clean_sheets[name] = df
    return clean_sheets

st.title("Price Shoes - Diagnóstico de Datos")
data = load_data()

# --- DIAGNÓSTICO ---
st.write("### Columnas encontradas por hoja:")
for name, df in data.items():
    st.write(f"**{name}**: {df.columns.tolist()}")

st.info("Revisa la lista de arriba. ¿Los nombres coinciden con lo que esperas?")

# --- INTENTO DE VISUALIZACIÓN ---
st.write("---")
st.header("Resumen de Semanas")

cols = st.columns(4)
for i, (name, df) in enumerate(data.items()):
    if "Sem" in name and i < 4:
        # Buscamos nombres de columnas ignorando mayúsculas/minúsculas
        cols_map = {c.lower(): c for c in df.columns}
        
        # Intentamos obtener valores
        try:
            total_ing = df[cols_map.get('total ingresos')].sum()
            pzas_hab = df[cols_map.get('pzas habilitadas')].sum()
            
            with cols[i]:
                st.metric(name, f"{int(total_ing):,}")
                st.write(f"Habilitadas: {int(pzas_hab):,}")
        except Exception as e:
            st.error(f"Error en {name}: No se encuentran columnas clave.")
