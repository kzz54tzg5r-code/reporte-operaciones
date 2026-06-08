import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

# CSS para el estilo de tarjetas que buscas
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white !important; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; font-size: 14px; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; margin-bottom: 20px; }
    .kpi-label { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    .kpi-value { color: #1F497D; font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_operational_data():
    try:
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        response = requests.get(URL, timeout=30)
        excel_file = pd.ExcelFile(io.BytesIO(response.content), engine="openpyxl")
        
        lista_dataframes = []
        # Solo cargar pestañas que contengan "Sem" en el nombre
        for nombre in excel_file.sheet_names:
            if "Sem" in nombre:
                df = pd.read_excel(excel_file, sheet_name=nombre)
                df.columns = df.columns.str.strip() # Elimina espacios accidentales
                
                # Mapeo flexible de nombres de columnas
                mapeo = {
                    'Total ingresos': 'Total ingresos', 
                    'Pzas Habilitadas': 'Pzas Habilitadas',
                    'Pzas Ubicadas': 'Pzas Ubicadas',
                    'No. Recorridos realizados': 'Rec_Real',
                    'No. Recorridos meta': 'Rec_Meta'
                }
                df.rename(columns={c: mapeo.get(c, c) for c in df.columns}, inplace=True)
                
                # Asegurar que existan las columnas, si no, crear con 0
                for col in ['Total ingresos', 'Pzas Habilitadas', 'Pzas Ubicadas', 'Rec_Real', 'Rec_Meta']:
                    if col not in df.columns: df[col] = 0
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                df['Semana'] = nombre.strip()
                lista_dataframes.append(df)
        
        return pd.concat(lista_dataframes, ignore_index=True)
    except Exception as e:
        st.error(f"Error al procesar archivo: {e}")
        return pd.DataFrame()

# --- APP ---
df = get_operational_data()

if not df.empty:
    st.markdown("### 📋 DESGLOSE COMPARATIVO HISTÓRICO")
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        ti = data['Total ingresos'].sum()
        th = data['Pzas Habilitadas'].sum()
        tr = (data['Rec_Real'].sum() / data['Rec_Meta'].sum() * 100) if data['Rec_Meta'].sum() > 0 else 0
        tu = (data['Pzas Ubicadas'].sum() / ti * 100) if ti > 0 else 0
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">Total Ingresos</p><p class="kpi-value">{int(ti):,}</p>
                    <p class="kpi-label">Pzas Habilitadas</p><p class="kpi-value">{int(th):,}</p>
                    <p class="kpi-label">% Recorridos</p><p class="kpi-value">{tr:.1f}%</p>
                    <p class="kpi-label">% Ubicado</p><p class="kpi-value">{tu:.1f}%</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.info("Cargando datos o archivo sin pestañas 'Sem'...")
