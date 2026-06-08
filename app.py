import streamlit as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página estilo corporativo y ancho total
st.set_page_config(
    page_title="Reporte de Operaciones - Ropa",
    page_icon="👕",
    layout="wide"
)

# Estilos CSS para entorno corporativo (Fondo gris claro/medio, énfasis azul)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    h1, h2, h3 {
        color: #1e3a8a; /* Azul énfasis corporativo */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal del Reporte
st.title("👕 Reporte de Operaciones — Procesos de Ropa")
st.markdown("Dashboard automatizado para el monitoreo de rendimiento de tiendas, procesamiento de inventario y KPIs logísticos.")

# -----------------------------------------------------------------------------
# Carga de datos y lógicas solicitadas
# -----------------------------------------------------------------------------

@st.cache_data
def cargar_datos():
    # Intenta cargar el archivo de checklist actualizado
    try:
        df = pd.read_csv("Indicadores Cambios y muertos.xlsx - Resultados por Checklist (2).csv")
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        # Mapeo de días en español para la agregación solicitada
        dias_espanol = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        # Crear columna de día de la semana para evitar fechas repetidas en las matrices
        df['Día Semana'] = df['Fecha'].dt.day_name().map(dias_espanol)
        
        # Asegurar orden cronológico de los días de la semana en las agrupaciones
        orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        df['Día Semana'] = pd.Categorical(df['Día Semana'], categories=orden_dias, ordered=True)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo de Checklist: {e}")
        return None

@st.cache_data
def cargar_resumen_semanal():
    # Intenta cargar la pestaña de resumen semanal (Sem 22)
    try:
        df_sem = pd.read_csv("Indicadores Cambios y muertos.xlsx - Sem 22.csv", skiprows=2)
        # Limpieza básica de filas vacías
        df_sem = df_sem.dropna(subset=['Tienda'])
        df_sem = df_sem[df_sem['Tienda'] != 'Subtotal']
        
        # Corrección de lógica solicitada: Total ingreso = Aduana Sistema + Muertos + Cajas
        # Aseguramos que las columnas sean numéricas antes de sumar
        for col in ['Ingreso Aduana (sistema)', 'Muertos', 'Ingresos Cajas']:
            if col in df_sem.columns:
                df_sem[col] = pd.to_numeric(df_sem[col], errors='coerce').fillna(0)
                
        df_sem['Total ingresos'] = df_sem['Ingreso Aduana (sistema)'] + df_sem['Muertos'] + df_sem['Ingresos Cajas']
        return df_sem
    except Exception as e:
        # Si falla por formato, creamos un set de datos de estructura dummy basada en tus requerimientos
        data_dummy = {
            'Tienda':
