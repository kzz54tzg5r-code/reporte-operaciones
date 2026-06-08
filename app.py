import streamlit as st
import pandas as pd
import requests
import io

# =========================================================================
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (ONEDRIVE PERSONAL) ---
# =========================================================================
@st.cache_data(ttl=600)  # El tablero se actualizará automáticamente cada 10 minutos
def get_operational_data():
    try:
        # Enlace de descarga directa del binario limpio
        URL_ONEDRIVE = "https://onedrive.live.com/download?resid=11B83163-6E2D-4B29-A4C2-9D0A3BB17B97"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, */*"
        }
        
        # 1. Descarga del flujo binario crudo desde la nube
        response = requests.get(URL_ONEDRIVE, headers=headers, timeout=25)
        response.raise_for_status()
        excel_bytes = io.BytesIO(response.content)
        
        # 2. Lectura directa forzando el motor openpyxl para la pestaña transaccional
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        # --- SOLUCIÓN CRÍTICA: LIMPIEZA DE ESPACIOS OCULTOS EN ENCABEZADOS ---
        # Esto elimina espacios al inicio/final de los nombres (como "Fecha " o "Ubicación ")
        df.columns = df.columns.str.strip()
        
        # --- RE-MAPEO DE COLUMNAS SEGÚN TU EXCEL REAL ---
        df.rename(columns={
            'Fecha s': 'Fecha_Corte',
            'Ubicación': 'Tienda',
            'Motivo de ingreso': 'Motivo_Ingreso',
            'Número de Piezas': 'Piezas'
        }, inplace=True)
        
        # 3. Validar la columna de tiempo (usamos la fecha de registro limpia)
        df['Fecha'] = pd.to_datetime(df['Fecha_Corte'], errors='coerce')
        df = df.dropna(subset=['Fecha'])
        
        # 4. Forzar que las piezas sean numéricas puras (evita caídas por celdas vacías)
        df['Piezas'] = pd.to_numeric(df['Piezas'], errors='coerce').fillna(0)
        
        # 5. Pivotación Dinámica: Mapear filas según las reglas de tu negocio de ropa
        # Distribución de ingresos
        df['Sis_Aduana'] = df.apply(lambda r: r['Piezas'] if str(r['Motivo_Ingreso']).strip() == 'Aduana' else 0, axis=1)
        df['Muertos'] = df.apply(lambda r: r['Piezas'] if str(r['Motivo_Ingreso']).strip() == 'Muertos' else 0, axis=1)
        df['Cajas'] = df.apply(lambda r: r['Piezas'] if str(r['Motivo_Ingreso']).strip() == 'Cajas' else 0, axis=1)
        
        # Clasificación del flujo de acondicionamiento de ropa
        df['Habilitadas'] = df.apply(lambda r: r['Piezas'] if 'Habilitad' in str(r.get('Actividad Realizada', '')) else 0, axis=1)
        df['Ubicadas'] = df.apply(lambda r: r['Piezas'] if 'Ubica' in str(r.get('Actividad Realizada', '')) else 0, axis=1)
        
        # Control analítico de recorridos de validación por sucursal
        df['Meta_Rec'] = 8.0  
        df['Real_Rec'] = df.apply(lambda r: 1.0 if str(r.get('Tabla', '')).strip() == 'Recorrido' else 0, axis=1)
        
        # Regla de negocio mandataria: Consolidar el ingreso total
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # 6. Agrupación por días de la semana en español evitando repetición de renglones redundantes
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
        df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
        
        # 7. Formatear indicadores temporales corporativos (Semanas y Meses)
        df['Semana'] = "Semana " + df['Fecha'].dt.isocalendar().week.astype(str)
        df['Mes'] = df['Fecha'].dt.strftime('%B').replace({
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        })
        
        return df
        
    except Exception as e:
        st.error(f"⚠️ Error al conectar o procesar la pestaña Checklist de OneDrive: {e}")
        return pd.DataFrame()
