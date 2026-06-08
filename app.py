import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

# --- CSS PARA ESTILO TARJETAS ---
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; margin-bottom: 20px; }
    .kpi-label { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .kpi-value { color: #1F497D; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
        df = pd.read_excel(url, sheet_name=None) # Lee todas las pestañas
        
        frames = []
        for nombre, sheet in df.items():
            if "Sem" in nombre:
                sheet.columns = sheet.columns.str.strip() # Limpia espacios en nombres de columnas
                sheet['Semana'] = nombre
                frames.append(sheet)
        
        master_df = pd.concat(frames, ignore_index=True)
        return master_df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

# --- CARGA Y FILTRO ---
df_master = get_data()

if not df_master.empty:
    # Asegurar que la columna Tienda existe (ajusta según tu archivo real)
    col_tienda = [c for c in df_master.columns if 'Tienda' in c]
    if col_tienda:
        df_master.rename(columns={col_tienda[0]: 'Tienda'}, inplace=True)
        tiendas = sorted([t for t in df_master['Tienda'].unique() if pd.notna(t)])
        
        # Menú desplegable
        seleccion = st.sidebar.selectbox("Selecciona Tienda:", ["Todas"] + tiendas)
        if seleccion != "Todas":
            df_master = df_master[df_master['Tienda'] == seleccion]

    st.markdown("### 📋 DESGLOSE COMPARATIVO HISTÓRICO")
    
    # Identificar columnas numéricas dinámicamente
    cols = st.columns(4)
    semanas = sorted(df_master['Semana'].unique())[-4:]
    
    for i, sem in enumerate(semanas):
        data = df_master[df_master['Semana'] == sem]
        
        # Extracción segura de valores
        ti = data.get('Total ingresos', pd.Series([0])).sum()
        th = data.get('Pzas Habilitadas', pd.Series([0])).sum()
        tr = (data.get('No. Recorridos realizados', pd.Series([0])).sum() / 
              data.get('No. Recorridos meta', pd.Series([1])).sum()) * 100
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">Total Ingresos</p><p class="kpi-value">{int(ti):,}</p>
                    <p class="kpi-label">Pzas Habilitadas</p><p class="kpi-value">{int(th):,}</p>
                    <p class="kpi-label">% Recorridos</p><p class="kpi-value">{tr:.1f}%</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.warning("No se encontraron pestañas con 'Sem'. Verifica el nombre en Google Sheets.")
