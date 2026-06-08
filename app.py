import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Price Shoes - Debug", layout="wide")

@st.cache_data(ttl=60)
def get_data_debug():
    try:
        url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
        # Leemos la primera pestaña para inspeccionar columnas
        df = pd.read_excel(url, sheet_name=0) 
        return df.columns.tolist()
    except Exception as e:
        return str(e)

st.title("Debug de Columnas")
columnas = get_data_debug()
st.write("Columnas encontradas en el archivo:", columnas)
