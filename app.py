import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")

# Función para cargar y limpiar datos
@st.cache_data(ttl=60)
def get_data():
    url = "https://docs.google.com/spreadsheets/d/18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI/export?format=xlsx"
    try:
        response = requests.get(url)
        excel_file = pd.ExcelFile(io.BytesIO(response.content))
        
        all_data = []
        for sheet_name in excel_file.sheet_names:
            if "Sem" in sheet_name:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                # Limpiar nombres de columnas
                df.columns = df.columns.str.strip()
                df['Semana'] = sheet_name.strip()
                all_data.append(df)
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando: {e}")
        return pd.DataFrame()

# Cargar datos
df = get_data()

st.title("Price Shoes • Operaciones Ropa")

if not df.empty:
    # --- DEBUG: Ver nombres de columnas ---
    with st.expander("Ver columnas detectadas (Ayuda para depuración)"):
        st.write(df.columns.tolist())

    # Seleccionar solo las últimas 4 semanas
    semanas = sorted(df['Semana'].unique())[-4:]
    cols = st.columns(4)

    for i, sem in enumerate(semanas):
        data = df[df['Semana'] == sem]
        
        # Mapeo flexible: intenta buscar varias formas de escribir la columna
        def get_val(opciones):
            for opt in opciones:
                if opt in data.columns:
                    # Convertir a numérico forzado
                    return pd.to_numeric(data[opt], errors='coerce').sum()
            return 0

        ti = get_val(['Total ingresos', 'Total Ingresos', 'Total ingresos '])
        th = get_val(['Pzas Habilitadas', 'Piezas habilitadas', 'Pzas habilitadas'])
        
        with cols[i]:
            st.metric(label=f"Semana {sem}", value=f"{int(ti):,}")
            st.write(f"Habilitadas: {int(th):,}")
else:
    st.warning("No se encontraron hojas con 'Sem' o el archivo está vacío.")
