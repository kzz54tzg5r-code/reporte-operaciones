import streamlit as st
import pandas as pd
import requests
import io

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Price Shoes - Dashboard", layout="wide")

# --- CSS PARA ESTILO TARJETAS ---
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; font-size: 14px; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; margin-bottom: 20px; box-shadow: 2px 2px 5px #ccc; }
    .kpi-label { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    .kpi-value { color: #1F497D; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# URL de publicación en Excel (.xlsx)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSV6dtosg0Ydt0o3NMFezC--NjHfEW82onFeY2JR4PTYD3ylG4ZlRaQBquscFrCy_Lysrau9zTW6dkn/pub?output=xlsx"

@st.cache_data(ttl=300)
def load_data():
    try:
        # Descarga el archivo publicado
        df_dict = pd.read_excel(SHEET_URL, sheet_name=None)
        frames = []
        for name, df in df_dict.items():
            if "Sem" in name:
                df.columns = df.columns.str.strip()  # Limpia espacios en nombres
                df['Semana'] = name.strip()
                frames.append(df)
        return pd.concat(frames, ignore_index=True)
    except Exception as e:
        return pd.DataFrame({'error': [str(e)]})

# --- INTERFAZ ---
st.markdown("## 👚 Price Shoes • Control Operativo")
df = load_data()

if 'error' in df.columns:
    st.error(f"Error cargando: {df['error'][0]}")
elif not df.empty:
    # Diagnóstico: muestra las columnas que encontró si quieres verificar
    # st.write("Columnas detectadas:", df.columns.tolist())
    
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        
        # Función para buscar columnas ignorando mayúsculas y espacios
        def get_col_val(keywords):
            for col in data.columns:
                if any(k.lower() in col.lower() for k in keywords):
                    return pd.to_numeric(data[col], errors='coerce').sum()
            return 0
        
        ti = get_col_val(['Total ingresos'])
        th = get_col_val(['Pzas Habilitadas'])
        tr = get_col_val(['% de recorridos', 'Recorridos'])
        tu = get_col_val(['% ubicado', 'Ubicado'])
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">Total Ingresos</p><p class="kpi-value">{int(ti):,}</p>
                    <p class="kpi-label">Pzas Habilitadas</p><p class="kpi-value">{int(th):,}</p>
                    <p class="kpi-label">% Recorridos</p><p class="kpi-value">{tr:.1% if tr > 1 else tr:.1%}</p>
                    <p class="kpi-label">% Ubicado</p><p class="kpi-value">{tu:.1% if tu > 1 else tu:.1%}</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.warning("No se encontraron hojas con 'Sem' o el formato de publicación no es válido.")
