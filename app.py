import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

# Estilos CSS para el look de infografía
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 5px solid #1F497D; box-shadow: 2px 2px 5px #ccc; }
    .title-text { font-size: 20px; font-weight: bold; color: #1F497D; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_operational_data():
    # ... (Se mantiene la lógica de carga de datos anterior) ...
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
                df['Semana'] = nombre_pestana.strip()
                lista_dataframes.append(df)
        return pd.concat(lista_dataframes, ignore_index=True) if lista_dataframes else pd.DataFrame()
    except: return pd.DataFrame()

# Interfaz Principal
st.markdown("# 👚 PRICE SHOES • Reporte de Operaciones")
df = get_operational_data()

if not df.empty:
    # FILTROS LATERALES
    st.sidebar.header("Filtros de Operación")
    t = st.sidebar.selectbox("Sucursal", ["Todas"] + sorted([str(x) for x in df['Tienda'].unique()]))
    s = st.sidebar.selectbox("Semana", ["Todas"] + sorted(df['Semana'].unique().tolist()))
    
    df_f = df.copy()
    if t != "Todas": df_f = df_f[df_f['Tienda'] == t]
    if s != "Todas": df_f = df_f[df_f['Semana'] == s]

    # INFOGRAFÍA DE 4 SEMANAS (Resumen arriba)
    st.subheader("📊 Resumen Ejecutivo: Últimas 4 Semanas")
    semanas_recientes = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas_recientes):
        data = df[df['Semana'] == sem]
        # Aquí calculamos los indicadores solicitados
        ing = data['Ingreso Aduana (sistema)'].sum()
        hab = data['Pzas Habilitadas'].sum()
        porc_hab = (hab/ing*100) if ing > 0 else 0
        
        with cols[i]:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="title-text">{sem}</p>', unsafe_allow_html=True)
            st.metric("Ingresos", f"{int(ing):,}")
            st.metric("Habilitadas", f"{int(hab):,}", f"{porc_hab:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    # TABLA DE DATOS
    st.write("### Detalle Operativo")
    st.dataframe(df_f, use_container_width=True)
else:
    st.warning("Conectando con la base de datos...")
