import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

# --- CSS PARA EL DISEÑO DE TARJETAS ---
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; font-size: 16px; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; box-shadow: 2px 2px 5px #ccc; }
    .kpi-label { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    .kpi-value { color: #1F497D; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_data():
    url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
    response = requests.get(url)
    xls = pd.ExcelFile(io.BytesIO(response.content))
    
    frames = []
    for sheet_name in xls.sheet_names:
        if "Sem" in sheet_name:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Limpiar nombres de columnas: eliminar espacios, minúsculas
            df.columns = df.columns.str.strip()
            df['Semana'] = sheet_name
            frames.append(df)
    
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# --- APP ---
st.markdown("# 👚 PRICE SHOES • Operaciones Ropa")
df = get_data()

if not df.empty:
    # Mapeo de nombres flexibles
    # Ajusta los nombres de la derecha si en tu Excel se llaman distinto
    mapeo = {
        'total ingresos': 'Total ingresos',
        'pzas habilitadas': 'Pzas Habilitadas',
        'pzas ubicadas': 'Pzas Ubicadas',
        'no. recorridos realizados': 'No. Recorridos realizados',
        'no. recorridos meta': 'No. Recorridos meta'
    }
    
    # Crear un diccionario de columnas normalizadas
    cols_norm = {c.lower(): c for c in df.columns}
    
    # Asegurar que las columnas existan o llenar con 0
    def get_col(name):
        return df[cols_norm.get(name.lower())] if name.lower() in cols_norm else 0

    st.markdown("---")
    st.markdown("### 📋 DESGLOSE COMPARATIVO HISTÓRICO")
    
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        
        ti = data[cols_norm.get('total ingresos')].sum() if 'total ingresos' in cols_norm else 0
        th = data[cols_norm.get('pzas habilitadas')].sum() if 'pzas habilitadas' in cols_norm else 0
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">TOTAL INGRESOS</p><p class="kpi-value">{int(ti):,}</p>
                    <p class="kpi-label">PIEZAS HABILITADAS</p><p class="kpi-value">{int(th):,}</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.warning("No se encontraron datos. Asegúrate de que las hojas contengan 'Sem'.")
