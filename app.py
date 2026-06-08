import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================================
# --- CONFIGURACIÓN DE INTERFAZ GENERAL Y ESTILOS CORPORATIVOS ---
# =========================================================================
st.set_page_config(page_title="Price Shoes - Operaciones Ropa", layout="wide", page_icon="👚")

# Reglas CSS Globales (Inyección del color Azul Énfasis 1 Oscuro 25%: #1F497D)
st.markdown("""
    <style>
    .reportview-container { background-color: #FFFFFF; }
    .main-title { color: #000000 !important; font-family: 'Arial', sans-serif; font-size: 34px !important; font-weight: 800; margin-bottom: 0px; }
    .sub-title { color: #E6007E !important; font-family: 'Arial', sans-serif; font-size: 15px !important; font-weight: bold; margin-top: -5px; letter-spacing: 0.5px; text-transform: uppercase; }
    .graph-title { color: #1F497D !important; font-weight: bold; font-size: 18px; margin-top: 35px; margin-bottom: 15px; border-left: 5px solid #1F497D; padding-left: 10px; }
    
    /* Estructura de tarjetas semanales compactas */
    .semana-header { background-color: #1F497D; color: white !important; font-weight: bold; text-align: center; padding: 6px; border-radius: 4px 4px 0 0; font-size: 14px; text-transform: uppercase; margin-bottom: 0px; }
    .kpi-card-nested { background-color: #F8F9FA; border-left: 1px solid #D9D9D9; border-right: 1px solid #D9D9D9; border-bottom: 1px solid #D9D9D9; border-radius: 0 0 4px 4px; padding: 10px 14px; text-align: center; box-shadow: 0px 2px 4px rgba(0,0,0,0.03); margin-bottom: 15px; }
    .kpi-sub-block { border-bottom: 1px dashed #D9D9D9; padding: 8px 0; }
    .kpi-sub-block:last-child { border-bottom: none; }
    .kpi-label-nested { color: #555555; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .kpi-value-nested { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; }
    .kpi-value-inline { color: #1F497D; font-size: 18px; font-weight: bold; margin: 0; display: inline-block; }
    .kpi-pct-inline { color: #E6007E; font-size: 15px; font-weight: bold; margin-left: 8px; display: inline-block; }

    /* REGLAS CSS PARA TABLAS */
    .tabla-auditoria { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; border: 1px solid #D9D9D9 !important; }
    .tabla-auditoria tr:first-child { background-color: #1F497D !important; color: #FFFFFF !important; height: 42px; }
    .tabla-auditoria tr:first-child td { background-color: #1F497D !important; color: #FFFFFF !important; font-weight: bold !important; text-align: center !important; padding: 10px; border: 1px solid #D9D9D9 !important; }
    .cell-td { padding: 10px; border: 1px solid #D9D9D9; text-align: right; }
    .cell-center { padding: 10px; border: 1px solid #D9D9D9; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (ONEDRIVE PERSONAL) ---
# =========================================================================
@st.cache_data(ttl=300)  # Bajamos a 5 minutos el caché para asegurar pruebas rápidas
def get_operational_data():
    try:
        # URL de descarga forzada del binario original de Excel
        URL_ONEDRIVE = "https://onedrive.live.com/download?resid=11B83163-6E2D-4B29-A4C2-9D0A3BB17B97"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, */*"
        }
        
        response = requests.get(URL_ONEDRIVE, headers=headers, timeout=30)
        response.raise_for_status()
        excel_bytes = io.BytesIO(response.content)
        
        # Lectura directa apuntando explícitamente a la pestaña transaccional
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        if df.empty:
            return pd.DataFrame()

        # Limpiar espacios fantasmas en los encabezados (Solución al error oculto de "Fecha ")
        df.columns = df.columns.str.strip()
        
        # Homologación estricta de nombres según tu formulario real
        df.rename(columns={
            'Fecha s': 'Fecha_Corte',
            'Ubicación': 'Tienda',
            'Motivo de ingreso': 'Motivo_Ingreso',
            'Número de Piezas': 'Piezas'
        }, inplace=True)
        
        # Validación y parsing de fechas seguras
        df['Fecha'] = pd.to_datetime(df['Fecha_Corte'], errors='coerce')
        df = df.dropna(subset=['Fecha'])
        
        # Asegurar tipo numérico en el conteo de ropa
        df['Piezas'] = pd.to_numeric(df['Piezas'], errors='coerce').fillna(0)
        
        # --- PROCESAMIENTO OPERATIVO DE FILAS (PIVOTACIÓN EN CALIENTE) ---
        df['Sis_Aduana'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Aduana' else 0, axis=1)
        df['Muertos'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Muertos' else 0, axis=1)
        df['Cajas'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Cajas' else 0, axis=1)
        
        # Búsqueda parcial de actividades para blindar si escriben "habilitada" o "Habilitadas"
        df['Habilitadas'] = df.apply(lambda r: r['Piezas'] if 'habilitad' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        df['Ubicadas'] = df.apply(lambda r: r['Piezas'] if 'ubica' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        
        # Recorridos
        df['Meta_Rec'] = 8.0  
        df['Real_Rec'] = df.apply(lambda r: 1.0 if 'recorrido' in str(r.get('Tabla', '')).lower() else 0, axis=1)
        
        # Regla mandataria: Ingreso total es la suma de aduana sistema, muertos y cajas
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # Agrupación por días de la semana (Lunes, Martes...)
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
        df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
        
        # Marcadores temporales
        df['Semana'] = "Semana " + df['Fecha'].dt.isocalendar().week.astype(str)
        df['Mes'] = df['Fecha'].dt.strftime('%B').replace({
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        })
        
        return df
    except Exception as e:
        # Almacenamos el error en un contenedor controlado para que no rompa la pantalla completa
        st.sidebar.error(f"Error interno en base de datos: {e}")
        return pd.DataFrame()

# --- MARCA CORPORATIVA GENERAL ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CONTROL DE OPERACIONES ROPA</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

# Inicialización segura de la matriz de la nube
df_master = get_operational_data()

# --- VALIDACIÓN CRÍTICA PARA EVITAR LA PANTALLA BLANCA ---
if df_master.empty:
    st.warning("⚠️ No se pudieron procesar los datos de la pestaña 'Checklist' de OneDrive.")
    st.info("💡 Por favor, verifica que las columnas de la hoja se llamen exactamente: 'Fecha s', 'Ubicación', 'Motivo de ingreso', 'Número de Piezas', 'Actividad Realizada' y 'Tabla'.")
else:
    # =========================================================================
    # --- FILTROS LATERALES (SIDEBAR) ---
    # =========================================================================
    st.sidebar.markdown("### 🎛️ Filtros de Operación")
    tipo_periodo = st.sidebar.radio("Agrupar Reporte por:", ["Por Semana", "Por Mes"])

    if tipo_periodo == "Por Semana":
        semanas_disponibles = sorted(list(df_master['Semana'].unique()))
        periodo_seleccionado = st.sidebar.selectbox("Selecciona la Semana Operativa:", semanas_disponibles)
        df_filtrado_periodo = df_master[df_master['Semana'] == periodo_seleccionado]
        label_corte = f"({periodo_seleccionado.upper()})"
    else:
        meses_disponibles = sorted(list(df_master['Mes'].unique()))
        periodo_seleccionado = st.sidebar.selectbox("Selecciona el Mes Operativo:", ["Todos los Meses"] + meses_disponibles)
        if periodo_seleccionado == "Todos los Meses":
            df_filtrado_periodo = df_master.copy()
            label_corte = "(HISTÓRICO CONSOLIDADO)"
        else:
            df_filtrado_periodo = df_master[df_master['Mes'] == periodo_seleccionado]
            label_corte = f"(MES DE {periodo_seleccionado.upper()})"

    tiendas_disponibles = sorted(list(df_master['Tienda'].dropna().unique()))
    tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + tiendas_disponibles)

    df_filtered = df_filtrado_periodo.copy()
    if tienda != "Todas las Tiendas":
        df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

    # =========================================================================
    # --- RENDERIZADO PRINCIPAL DEL DASHBOARD ---
    # =========================================================================
    if not df_filtered.empty:
        
        # --- BLOQUE 1: RESUMEN COMPARATIVO HISTÓRICO (ÚLTIMAS 4 SEMANAS) ---
        st.markdown('<p style="color: #555555; font-weight: bold; font-size: 14px; margin-bottom: 10px; letter-spacing: 0.5px;">📋 DESGLOSE COMPARATIVO HISTÓRICO (ÚLTIMAS 4 SEMANAS)</p>', unsafe_allow_html=True)
        
        ultimas_4_semanas = sorted(list(df_master['Semana'].unique()))[-4:]
        cols_semanas = st.columns(len(ultimas_4_semanas))
        
        for i, sem in enumerate(ultimas_4_semanas):
            df_sem = df_master[df_master['Semana'] == sem].copy()
            if tienda != "Todas las Tiendas":
                df_sem = df_sem[df_sem['Tienda'] == tienda]
                
            t_ing, t_hab, t_ub = df_sem['Total_Ingresos'].sum(), df_sem['Habilitadas'].sum(), df_sem['Ubicadas'].sum()
            m_rec, r_rec = df_sem['Meta_Rec'].sum(), df_sem['Real_Rec'].sum()
            
            pct_hab = (t_hab / t_ing * 100) if t_ing > 0 else 0.0
            pct_ub = (t_ub / t_ing * 100) if t_ing > 0 else 0.0
            ef_rec = (r_rec / m_rec * 100) if m_rec > 0 else 0.0
            
            with cols_semanas[i]:
                st.markdown(f'<p class="semana-header">{sem}</p>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="kpi-card-nested">
                        <div class="kpi-sub-block"><p class="kpi-label-nested">📥 Total Ingresos</p><p class="kpi-value-nested">{t_ing:,}</p></div>
                        <div class="kpi-sub-block"><p class="kpi-label-nested">✨ Piezas Habilitadas</p><div class="kpi-value-inline">{t_hab:,}</div><div class="kpi-pct-inline">({pct_hab:.1f}%)</div></div>
                        <div class="kpi-sub-block"><p class="kpi-label-nested">📍 Piezas Ubicadas</p><div class="kpi-value-inline">{t_ub:,}</div><div class="kpi-pct-inline">({pct_ub:.1f}%)</div></div>
                        <div class="kpi-sub-block"><p class="kpi-label-nested">🎯 % de Recorridos</p><p class="kpi-value-nested">{ef_rec:.1f}%</p></div>
                    </div>
                    """, unsafe_allow_html=True)

        # --- SISTEMA DE PESTAÑAS (TABS) PARA AUDITORÍA Y ANÁLISIS ---
        tab_auditoria, tab_evolutivo = st.tabs(
