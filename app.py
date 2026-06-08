import streamlit as st
import pandas as pd
import requests
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Price Shoes - Operaciones", layout="wide")

# --- CSS PARA ESTILO TARJETAS CORPORATIVAS ---
st.markdown("""
    <style>
    .semana-header { background-color: #1F497D; color: white !important; font-weight: bold; text-align: center; padding: 10px; border-radius: 5px 5px 0 0; font-size: 16px; margin-bottom: 0px; }
    .kpi-card { background-color: #F8F9FA; border: 1px solid #D9D9D9; border-radius: 0 0 5px 5px; padding: 15px; text-align: center; box-shadow: 2px 2px 5px #ccc; margin-bottom: 20px; }
    .kpi-label { color: #555555; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-top: 10px; }
    .kpi-value { color: #1F497D; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_operational_data():
    try:
        # ID de tu archivo
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        response = requests.get(URL, timeout=30)
        excel_file = pd.ExcelFile(io.BytesIO(response.content), engine="openpyxl")
        
        lista_dataframes = []
        # Filtramos solo las pestañas que empiezan por 'Sem'
        for nombre_pestana in [p for p in excel_file.sheet_names if p.strip().lower().startswith("sem")]:
            df = pd.read_excel(excel_file, sheet_name=nombre_pestana)
            # Limpieza básica de nombres de columnas
            df.columns = df.columns.str.strip()
            
            # Forzar columnas numéricas (evita el TypeError)
            cols_num = ['Total ingresos', 'Pzas Habilitadas', 'Pzas Ubicadas']
            for c in cols_num:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            
            df['Semana'] = nombre_pestana.strip()
            lista_dataframes.append(df)
            
        return pd.concat(lista_dataframes, ignore_index=True)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# --- APP ---
st.markdown("# 👚 PRICE SHOES • Operaciones Ropa")
st.markdown("### CONTROL DE ACONDICIONAMIENTO, SEGUIMIENTO DE RECORRIDOS Y MATRIZ DE PISO")
df = get_operational_data()

if not df.empty:
    st.markdown("---")
    st.markdown("📋 **DESGLOSE COMPARATIVO HISTÓRICO (ÚLTIMAS 4 SEMANAS)**")
    
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        # Cálculos de resumen
        total_ing = data['Total ingresos'].sum()
        total_hab = data['Pzas Habilitadas'].sum()
        pct_hab = (total_hab / total_ing * 100) if total_ing > 0 else 0
        
        with cols[i]:
            st.markdown(f'<p class="semana-header">{sem}</p>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="kpi-card">
                    <p class="kpi-label">Total Ingresos</p>
                    <p class="kpi-value">{int(total_ing):,}</p>
                    <p class="kpi-label">Piezas Habilitadas</p>
                    <p class="kpi-value">{int(total_hab):,} ({pct_hab:.1f}%)</p>
                </div>
            ''', unsafe_allow_html=True)
    
    st.subheader("Detalle Operativo")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Verifica que las pestañas en tu Google Sheet empiecen con el prefijo 'Sem' y que los datos sean numéricos.")
