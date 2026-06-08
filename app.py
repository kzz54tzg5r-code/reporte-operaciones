import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Price Shoes - Dashboard Ejecutivo", layout="wide")

# Estilos CSS Infográficos
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 5px solid #1F497D; box-shadow: 2px 2px 5px #ccc; margin-bottom: 10px; }
    .title-text { font-size: 16px; font-weight: bold; color: #1F497D; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_operational_data():
    try:
        # Aquí irá el ID de tu Google Sheet
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
            
            # Limpieza forzada de columnas numéricas
            cols_num = ['Pzas Habilitadas', 'Pzas Ubicadas', 'Ingreso Aduana (sistema)', 'No. Recorridos meta', 'No. Recorridos realizados']
            for c in cols_num:
                if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            
            if 'Tienda' in df.columns:
                df = df[df['Tienda'].notna()]
                df['Semana'] = nombre_pestana.strip()
                df['Mes'] = 'Mayo' if '20' in nombre_pestana or '21' in nombre_pestana else 'Junio'
                lista_dataframes.append(df)
        
        return pd.concat(lista_dataframes, ignore_index=True) if lista_dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.markdown("# 👚 PRICE SHOES • Dashboard Ejecutivo")
df = get_operational_data()

if not df.empty:
    # FILTROS LATERALES
    st.sidebar.header("Filtros de Análisis")
    filtro_tienda = st.sidebar.selectbox("Sucursal", ["Todas"] + sorted([str(t) for t in df['Tienda'].unique()]))
    filtro_mes = st.sidebar.selectbox("Mes", ["Todos", "Mayo", "Junio"])
    filtro_sem = st.sidebar.selectbox("Semana", ["Todas"] + sorted(df['Semana'].unique().tolist()))
    
    # 1. INFOGRAFÍA SUPERIOR (Últimas 4 semanas)
    st.subheader("📊 Resumen Ejecutivo: Últimas 4 Semanas")
    semanas_ordenadas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas_ordenadas):
        data = df[df['Semana'] == sem]
        ing = data['Ingreso Aduana (sistema)'].sum()
        hab = data['Pzas Habilitadas'].sum()
        ubi = data['Pzas Ubicadas'].sum()
        rec_m = data['No. Recorridos meta'].sum()
        rec_r = data['No. Recorridos realizados'].sum()
        
        with cols[i]:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="title-text">{sem}</p>', unsafe_allow_html=True)
            st.metric("Total Ingresos", f"{int(ing):,}")
            st.metric("Hab. (%)", f"{int(hab):,}", f"{(hab/ing*100 if ing>0 else 0):.1f}%")
            st.metric("Ubi. (%)", f"{int(ubi):,}", f"{(ubi/ing*100 if ing>0 else 0):.1f}%")
            st.metric("Recorrido", f"{(rec_r/rec_m*100 if rec_m>0 else 0):.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. FILTRADO Y TABLA DE DATOS
    df_f = df.copy()
    if filtro_tienda != "Todas": df_f = df_f[df_f['Tienda'].astype(str) == filtro_tienda]
    if filtro_mes != "Todos": df_f = df_f[df_f['Mes'] == filtro_mes]
    if filtro_sem != "Todas": df_f = df_f[df_f['Semana'] == filtro_sem]
    
    st.divider()
    st.subheader("Detalle Operativo Filtrado")
    st.dataframe(df_f, use_container_width=True)

else:
    st.warning("Verificando conexión con Google Sheets...")
