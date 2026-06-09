import streamlit as st
import pandas as pd

st.set_page_config(page_title="Price Shoes - Dashboard", layout="wide")

# URL de publicación en Excel (.xlsx)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSV6dtosg0Ydt0o3NMFezC--NjHfEW82onFeY2JR4PTYD3ylG4ZlRaQBquscFrCy_Lysrau9zTW6dkn/pub?output=xlsx"

@st.cache_data(ttl=300)
def load_data():
    try:
        # Cargamos el archivo y limpiamos nombres de columnas inmediatamente
        df_dict = pd.read_excel(SHEET_URL, sheet_name=None)
        frames = []
        for name, df in df_dict.items():
            if "Sem" in name:
                df.columns = df.columns.str.strip()
                df['Semana'] = name.strip()
                frames.append(df)
        return pd.concat(frames, ignore_index=True)
    except Exception:
        return pd.DataFrame()

# --- INTERFAZ ---
st.markdown("## 👚 Price Shoes • Control Operativo")
df = load_data()

if not df.empty:
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)
    
    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        
        # Función mejorada para limpiar y sumar
        def get_clean_val(keyword):
            for col in data.columns:
                if keyword.lower() in col.lower():
                    # Convertimos a string, quitamos '%', y convertimos a número
                    series = data[col].astype(str).str.replace('%', '').str.replace(',', '')
                    return pd.to_numeric(series, errors='coerce').sum()
            return 0

        # Obtener valores
        ti = get_clean_val('Total ingresos')
        th = get_clean_val('Pzas Habilitadas')
        tr = get_clean_val('Recorridos')
        tu = get_clean_val('Ubicado')

        with cols[i]:
            st.subheader(sem.upper())
            st.metric("Total Ingresos", f"{int(ti):,}")
            st.metric("Pzas Habilitadas", f"{int(th):,}")
            # Si el número es mayor a 1, asumimos que es porcentaje entero, si no, decimal
            st.metric("% Recorridos", f"{tr:.1f}%")
            st.metric("% Ubicado", f"{tu:.1f}%")
else:
    st.warning("No se encontraron datos. Asegúrate de que las hojas contengan 'Sem'.")
