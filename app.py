import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE BI ---
st.set_page_config(page_title="BI - Cambios y Muertos", layout="wide", page_icon="📊")

# --- DATASET CONSOLIDADO DEL PDF ---
@st.cache_data
def get_operational_data():
    # Datos ordenados verticalmente para cumplir con los estándares de calidad de código (PEP 8)
    data = [
        # Lunes 25
        {
            "Fecha": "2026-05-25", "Tienda": "Vallejo", "Sis_Aduana": 293, "Fis_Aduana": 332,
            "Muertos": 32, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 229,
            "Habilitadas": 248, "Ubicadas": 356
        },
        {
            "Fecha": "2026-05-25", "Tienda": "Arco Norte", "Sis_Aduana": 109, "Fis_Aduana": 82,
            "Muertos": 36, "Cajas": 73, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 109,
            "Habilitadas": 409, "Ubicadas": 545
        },
        {
            "Fecha": "2026-05-25", "Tienda": "Puebla Sur", "Sis_Aduana": 79, "Fis_Aduana": 0,
            "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0,
            "Habilitadas": 185, "Ubicadas": 197
        },
        # Martes 26
        {
            "Fecha": "2026-05-26", "Tienda": "Vallejo", "Sis_Aduana": 441, "Fis_Aduana": 441,
            "Muertos": 0, "Cajas": 235, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 235,
            "Habilitadas": 595, "Ubicadas": 381
        },
        {
            "Fecha": "2026-05-26", "Tienda": "Arco Norte", "Sis_Aduana": 164, "Fis_Aduana": 75,
            "Muertos": 30, "Cajas": 144, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 174,
            "Habilitadas": 201, "Ubicadas": 309
        },
        {
            "Fecha": "2026-05-26", "Tienda": "Puebla Sur", "Sis_Aduana": 113, "Fis_Aduana": 108,
            "Muertos": 98, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 98,
            "Habilitadas": 116, "Ubicadas": 198
        },
        {
            "Fecha": "2026-05-26", "Tienda": "Miravalle", "Sis_Aduana": 47, "Fis_Aduana": 37,
            "Muertos": 39, "Cajas": 17, "Meta_Rec": 5, "Real_Rec": 2, "Recolectadas": 39,
            "Habilitadas": 81, "Ubicadas": 129
        },
        # Miércoles 27
        {
            "Fecha": "2026-05-27", "Tienda": "Vallejo", "Sis_Aduana": 436, "Fis_Aduana": 441,
            "Muertos": 0, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 3, "Recolectadas": 197,
            "Habilitadas": 478, "Ubicadas": 452
        },
        {
            "Fecha": "2026-05-27", "Tienda": "Puebla Sur", "Sis_Aduana": 67, "Fis_Aduana": 65,
            "Muertos": 160, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 160,
            "Habilitadas": 307, "Ubicadas": 617
        },
        # Jueves 28
        {
            "Fecha": "2026-05-28", "Tienda": "Vallejo", "Sis_Aduana": 550, "Fis_Aduana": 563,
            "Muertos": 168, "Cajas": 224, "Meta_Rec": 8, "Real_Rec": 8, "Recolectadas": 392,
            "Habilitadas": 755, "Ubicadas": 452
        },
        # Domingo 31
        {
            "Fecha": "2026-05-31", "Tienda": "Vallejo", "Sis_Aduana": 351, "Fis_Aduana": 351,
            "Muertos": 326, "Cajas": 488, "Meta_Rec": 8, "Real_Rec": 16, "Recolectadas": 884,
            "Habilitadas": 705, "Ubicadas": 2605
        },
        {
            "Fecha": "2026-05-31", "Tienda": "Arco Norte", "Sis_Aduana": 264, "Fis_Aduana": 107,
            "Muertos": 57, "Cajas": 78, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 135,
            "Habilitadas": 784, "Ubicadas": 482
        }
    ]
    df = pd.DataFrame(data)
    df
