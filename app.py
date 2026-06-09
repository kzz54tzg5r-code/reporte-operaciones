import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Sustituye esta URL con la que obtuviste siguiendo los 4 pasos anteriores
URL_PUBLICADA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSV6dtosg0Ydt0o3NMFezC--NjHfEW82onFeY2JR4PTYD3ylG4ZlRaQBquscFrCy_Lysrau9zTW6dkn/pub?output=xlsx"

@st.cache_data(ttl=300)
def load_data():
    try:
        # Lectura directa del archivo publicado
        df = pd.read_excel(URL_PUBLICADA, sheet_name=None)
        
        frames = []
        for name, sheet in df.items():
            if "Sem" in name:
                sheet.columns = sheet.columns.str.strip()
                sheet['Semana'] = name
                frames.append(sheet)
        return pd.concat(frames, ignore_index=True)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.title("📊 Dashboard Price Shoes")
    cols = st.columns(4)
    semanas = sorted(df['Semana'].unique())[-4:]
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        ti = data['Total ingresos'].sum() if 'Total ingresos' in data.columns else 0
        th = data['Pzas Habilitadas'].sum() if 'Pzas Habilitadas' in data.columns else 0
        
        with cols[i]:
            st.metric(sem, f"{int(ti):,}", f"Hab: {int(th):,}")
else:
    st.warning("No se pudo leer el archivo. Verifica que el formato de publicación sea .xlsx")
