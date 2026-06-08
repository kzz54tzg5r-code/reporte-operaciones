import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

@st.cache_data(ttl=60)
def get_operational_data():
    try:
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        response = requests.get(URL, timeout=30)
        excel_file = pd.ExcelFile(io.BytesIO(response.content), engine="openpyxl")
        
        lista_dataframes = []
        for nombre_pestana in [p for p in excel_file.sheet_names if p.strip().lower().startswith("sem")]:
            df_temp = pd.read_excel(excel_file, sheet_name=nombre_pestana, header=None)
            fila_cabecera = 0
            for idx in range(min(12, len(df_temp))):
                if "Tienda" in df_temp.iloc[idx].astype(str).values:
                    fila_cabecera = idx
                    break
            
            df = pd.read_excel(excel_file, sheet_name=nombre_pestana, skiprows=fila_cabecera)
            df.columns = df.columns.str.strip()
            
            if 'Tienda' in df.columns:
                df = df[df['Tienda'].notna()]
                df = df[~df['Tienda'].astype(str).str.contains('total|resumen', case=False, na=False)]
                df['Semana'] = nombre_pestana.strip()
                # Asignación manual de mes según semana
                df['Mes'] = 'Mayo' if 'sem 20' in nombre_pestana.lower() or 'sem 21' in nombre_pestana.lower() else 'Junio'
                
                cols_num = ['Pzas Habilitadas', 'Ingreso Aduana (sistema)']
                for c in cols_num:
                    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                lista_dataframes.append(df)
        
        return pd.concat(lista_dataframes, ignore_index=True) if lista_dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("👚 Dashboard de Operaciones")
df = get_operational_data()

if not df.empty:
    # 1. Menú Tiendas
    tiendas = ["Todas"] + sorted([str(t) for t in df['Tienda'].unique() if pd.notna(t)])
    filtro_tienda = st.sidebar.selectbox("Seleccionar Tienda", tiendas)
    
    # 2. Menú Meses
    meses = ["Todos", "Mayo", "Junio"]
    filtro_mes = st.sidebar.selectbox("Seleccionar Mes", meses)
    
    # 3. Menú Semanas
    semanas = ["Todas"] + sorted(df['Semana'].unique().tolist())
    filtro_sem = st.sidebar.selectbox("Seleccionar Semana", semanas)
    
    # Aplicar Filtros
    df_f = df.copy()
    if filtro_tienda != "Todas": df_f = df_f[df_f['Tienda'].astype(str) == filtro_tienda]
    if filtro_mes != "Todos": df_f = df_f[df_f['Mes'] == filtro_mes]
    if filtro_sem != "Todas": df_f = df_f[df_f['Semana'] == filtro_sem]
    
    st.write(f"### Visualizando: {filtro_tienda} | {filtro_mes} | {filtro_sem}")
    st.dataframe(df_f)
    
    # Gráfico simple
    fig = go.Figure(go.Bar(x=df_f['Tienda'], y=df_f['Pzas Habilitadas']))
    fig.update_layout(title="Piezas Habilitadas por Tienda")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Cargando o sin datos...")
