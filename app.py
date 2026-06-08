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
            
            # Asegurar columnas necesarias
            if 'Tienda' in df.columns:
                df = df[df['Tienda'].notna()]
                # Nombres de columnas mapeados a valores estándar
                cols_num = {
                    'Total ingresos': 'Total_Ing', 'Pzas Habilitadas': 'Hab', 
                    'Pzas Ubicadas': 'Ubi', 'No. Recorridos realizados': 'Rec_Real',
                    'No. Recorridos meta': 'Rec_Meta'
                }
                df.rename(columns=cols_num, inplace=True)
                for c in ['Total_Ing', 'Hab', 'Ubi', 'Rec_Real', 'Rec_Meta']:
                    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                
                df['Semana'] = nombre_pestana.strip()
                df['Mes'] = 'Mayo' if '20' in nombre_pestana or '21' in nombre_pestana else 'Junio'
                lista_dataframes.append(df)
        
        return pd.concat(lista_dataframes, ignore_index=True) if lista_dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("👚 Dashboard de Operaciones")
df = get_operational_data()

if not df.empty:
    # --- BLOQUE DE 4 SEMANAS RECIENTES ---
    st.subheader("Resumen 4 Semanas Recientes")
    semanas_ordenadas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(len(semanas_ordenadas))
    
    for i, sem in enumerate(semanas_ordenadas):
        df_sem = df[df['Semana'] == sem]
        tot_ing = df_sem['Total_Ing'].sum()
        hab = df_sem['Hab'].sum()
        ubi = df_sem['Ubi'].sum()
        rec_meta = df_sem['Rec_Meta'].sum()
        rec_real = df_sem['Rec_Real'].sum()
        
        with cols[i]:
            st.markdown(f"**{sem}**")
            st.metric("Total Ingresos", f"{int(tot_ing):,}")
            st.metric("Hab. (%)", f"{int(hab):,}", f"{(hab/tot_ing*100 if tot_ing>0 else 0):.1f}%")
            st.metric("Ubi. (%)", f"{int(ubi):,}", f"{(ubi/tot_ing*100 if tot_ing>0 else 0):.1f}%")
            st.metric("Recorridos (%)", f"{(rec_real/rec_meta*100 if rec_meta>0 else 0):.1f}%")

    # --- FILTROS Y TABLA ---
    st.divider()
    filtro_tienda = st.sidebar.selectbox("Sucursal", ["Todas"] + sorted([str(t) for t in df['Tienda'].unique()]))
    filtro_mes = st.sidebar.selectbox("Mes", ["Todos", "Mayo", "Junio"])
    filtro_sem = st.sidebar.selectbox("Semana", ["Todas"] + sorted(df['Semana'].unique().tolist()))
    
    # Lógica de filtrado
    df_f = df.copy()
    if filtro_tienda != "Todas": df_f = df_f[df_f['Tienda'].astype(str) == filtro_tienda]
    if filtro_mes != "Todos": df_f = df_f[df_f['Mes'] == filtro_mes]
    if filtro_sem != "Todas": df_f = df_f[df_f['Semana'] == filtro_sem]
    
    st.dataframe(df_f, use_container_width=True)
else:
    st.warning("Cargando datos...")
