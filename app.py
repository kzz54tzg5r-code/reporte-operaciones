import streamlit as st
import pandas as pd
import requests
import io

# =========================================================================
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (ONEDRIVE) ---
# =========================================================================
@st.cache_data(ttl=600)  # Actualización automática cada 10 minutos
def get_operational_data():
    try:
        # Enlace de descarga directa del archivo en OneDrive
        URL_ONEDRIVE = "https://onedrive.live.com/download?resid=11B83163-6E2D-4B29-A4C2-9D0A3BB17B97"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
        # 1. Descarga segura del flujo de bytes independientes
        response = requests.get(URL_ONEDRIVE, headers=headers, timeout=20)
        response.raise_for_status()
        excel_bytes = io.BytesIO(response.content)
        
        # 2. Lectura explícita forzando el motor openpyxl para la pestaña transaccional
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        # --- LIMPIEZA Y HOMOLOGACIÓN DE COLUMNAS DE LA PESTAÑA CHECKLIST ---
        # Renombrar columnas si vienen con espacios o variantes de nombres de formulario
        mapeo_columnas = {
            'Fecha s': 'Fecha_Corte',
            'Ubicación': 'Tienda',
            'Motivo de ingreso': 'Clasificacion_Ingreso',
            'Número de Piezas': 'Piezas'
        }
        df.rename(columns=mapeo_columnas, inplace=True)
        
        # 3. Validar y parsear la columna de tiempo principal
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=['Fecha']) # Eliminar registros sin estampa de tiempo válida
        
        # 4. Reconstrucción dinámica de métricas basada en las transacciones de auditoría
        # Aseguramos que los valores numéricos no tengan textos vacíos
        df['Piezas'] = pd.to_numeric(df['Piezas'], errors='coerce').fillna(0)
        
        # Mapeo y pivote dinámico de la estructura transaccional para extraer las columnas requeridas
        # (Esto mapea dinámicamente si es ingreso por Aduana Sistema, Muertos o Cajas)
        df['Sis_Aduana'] = df.apply(lambda r: r['Piezas'] if r['Clasificacion_Ingreso'] == 'Aduana' else 0, axis=1)
        df['Muertos'] = df.apply(lambda r: r['Piezas'] if r['Clasificacion_Ingreso'] == 'Muertos' else 0, axis=1)
        df['Cajas'] = df.apply(lambda r: r['Piezas'] if r['Clasificacion_Ingreso'] == 'Cajas' else 0, axis=1)
        
        # Mapeo de actividades de destino (Habilitadas / Ubicadas)
        df['Habilitadas'] = df.apply(lambda r: r['Piezas'] if 'Habilitad' in str(r['Actividad Realizada']) else 0, axis=1)
        df['Ubicadas'] = df.apply(lambda r: r['Piezas'] if 'Ubica' in str(r['Actividad Realizada']) else 0, axis=1)
        
        # Metas fijas operativas de recorridos por asignación diaria
        df['Meta_Rec'] = 8.0 
        df['Real_Rec'] = df.apply(lambda r: 1.0 if r['Tabla'] == 'Recorrido' else 0, axis=1)
        
        # 5. Regla de negocio mandataria: Consolidar Ingresos Totales
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # 6. Agrupación limpia por días de la semana (Evita repetición de filas por horas idénticas)
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
        df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
        
        # Construcción de la columna macro de Semana Operativa basada en el año-semana fiscal
        df['Semana'] = "Semana " + df['Fecha'].dt.isocalendar().week.astype(str)
        df['Mes'] = df['Fecha'].dt.strftime('%B').replace({
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': '
