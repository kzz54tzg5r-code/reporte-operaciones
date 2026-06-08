import streamlit as st
import pandas as pd
import requests
import io

# =========================================================================
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (ONEDRIVE) ---
# =========================================================================
# El ttl=600 asegura que los datos se refresquen automáticamente cada 10 minutos
@st.cache_data(ttl=600)
def get_operational_data():
    try:
        # 1. Enlace de descarga directa de tu archivo en OneDrive
        URL_ONEDRIVE = "https://onedrive.live.com/download?resid=11B83163-6E2D-4B29-A4C2-9D0A3BB17B97"
        
        # Cabeceras estándar para simular peticiones de un navegador web y evitar bloqueos
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
        # 2. Descargar el contenido binario del archivo usando requests
        response = requests.get(URL_ONEDRIVE, headers=headers, timeout=15)
        response.raise_for_status()  # Lanza un error si la descarga falla
        
        # 3. Convertir los bytes descargados en un buffer de memoria
        excel_bytes = io.BytesIO(response.content)
        
        # 4. Leer la pestaña específica apuntando explícitamente al motor 'openpyxl'
        # Nota: Asegúrate de que el nombre 'Checklist' coincida exactamente con tu pestaña (mayúsculas/minúsculas)
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        # --- PROCESAMIENTO Y REGLAS DE NEGOCIO ---
        # Asegurar formato de fecha (ajusta el nombre exacto de tu columna si es necesario)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        # Regla de negocio: El ingreso total consolida el sistema, los muertos y las cajas
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # Agrupación y mapeo por días de la semana evitando repetición de fechas limpias
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
        df['Dia_Nombre'] = df['Fecha'].dt.dayofweek.map(dias_espanol)
        
        return df
        
    except Exception as e:
        st.error(f"⚠️ Error al conectar con la pestaña Checklist de OneDrive: {e}")
        return pd.DataFrame()
