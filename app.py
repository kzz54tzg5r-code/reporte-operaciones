import streamlit as st
import pandas as pd
import requests
import io

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Price Shoes - Dashboard", layout="wide")

# --- CSS PARA EL DISEÑO DE TARJETAS ---
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; font-size: 16px; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; box-shadow: 2px 2px 5px #ccc; margin-bottom: 20px; }
    .kpi-label { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    .kpi-value { color: #1F497D; font-size: 22px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
    response = requests.get(url)
    xls = pd.ExcelFile(io.BytesIO(response.content))
    
    # Lista para unir todas las semanas
    frames = []
    for sheet in xls.sheet_names:
        if "Sem" in sheet:
            df = pd.read_excel(xls, sheet_name=sheet)
            df.columns = df.columns.str.strip() # Limpiar nombres
            df['Semana'] = sheet
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# --- APP ---
st.markdown("## 👚 Price Shoes • Control Operativo")
df = load_data()

if not df.empty:
    # Obtener las últimas 4 semanas disponibles
    semanas = sorted(df['Semana'].unique(), reverse=True)[:4]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        
        # Cálculos de seguridad: si no existe la columna, pone 0
        def get_sum(col_name):
            return data[col_name].sum() if col_name in data.columns else 0
            
        ti = get_sum('Total ingresos')
        th = get_sum('Pzas Habilitadas')
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">Total Ingresos</p>
                    <p class="kpi-value">{int(ti):,}</p>
                    <p class="kpi-label">Pzas Habilitadas</p>
                    <p class="kpi-value">{int(th):,}</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.warning("No se detectaron datos. Asegúrate de que las hojas en Google Sheets se llamen 'Sem X'.")
