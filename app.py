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
        
        # Función segura para obtener sumas
        def get_safe_sum(keyword):
            for col in data.columns:
                if keyword.lower() in col.lower():
                    return pd.to_numeric(data[col], errors='coerce').sum()
            return 0

        # Obtener valores
        ti = get_safe_sum('Total ingresos')
        th = get_safe_sum('Pzas Habilitadas')
        tr = get_safe_sum('Recorridos')
        tu = get_safe_sum('Ubicado')

        with cols[i]:
            st.markdown(f"### {sem.upper()}")
            st.metric("Total Ingresos", f"{int(ti):,}")
            st.metric("Pzas Habilitadas", f"{int(th):,}")
            # Mostrar porcentajes como números simples si son mayores a 1, o formatear si son decimales
            st.metric("% Recorridos", f"{tr:.1f}%" if tr <= 100 else f"{tr:.0f}%")
            st.metric("% Ubicado", f"{tu:.1f}%" if tu <= 100 else f"{tu:.0f}%")
else:
    st.warning("No se encontraron datos o el archivo no es accesible. Verifica que la publicación esté activa.")
