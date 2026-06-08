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
# --- FUENTE DE DATOS CONSOLIDADA MULTI-PESTAÑA CON RASTREO DINÁMICO ---
# =========================================================================
@st.cache_data(ttl=60)
def get_operational_data():
    try:
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL_EXCEL_NUBE = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        
        response = requests.get(URL_EXCEL_NUBE, timeout=30)
        response.raise_for_status()
        
        excel_bytes = io.BytesIO(response.content)
        excel_file = pd.ExcelFile(excel_bytes, engine="openpyxl")
        todas_las_pestanas = excel_file.sheet_names
        
        # Filtrar únicamente las pestañas semanales de interés
        pestanas_semanas = [p for p in todas_las_pestanas if p.strip().lower().startswith("sem")]
        
        if not pestanas_semanas:
            st.sidebar.error("No se encontraron pestañas que inicien con 'Sem' en el archivo.")
            return pd.DataFrame()
            
        lista_dataframes = []
        
        for nombre_pestana in pestanas_semanas:
            # Lectura preliminar cruda sin ignorar filas para ubicar los encabezados reales
            df_crudo = pd.read_excel(excel_file, sheet_name=nombre_pestana, header=None, engine="openpyxl")
            
            if df_crudo.empty:
                continue
            
            # --- LOCALIZADOR INTELIGENTE DE CABECERAS ---
            # Rastrea las primeras 12 filas de la pestaña para encontrar la coordenada exacta de "Tienda"
            fila_cabecera = 0
            for idx_fila in range(min(12, len(df_crudo))):
                valores_fila = df_crudo.iloc[idx_fila].astype(str).str.strip().tolist()
                if "Tienda" in valores_fila:
                    fila_cabecera = idx_fila
                    break
            
            # Re-procesamos la hoja saltando las filas superiores innecesarias
            df_sem = pd.read_excel(excel_file, sheet_name=nombre_pestana, skiprows=fila_cabecera, engine="openpyxl")
            df_sem.columns = df_sem.columns.str.strip()
            
            # Diccionario de homologación de nombres de columnas según tus especificaciones de KPI
            renombres = {
                'Tienda': 'Tienda',
                'Ingreso Aduana (sistema)': 'Sis_Aduana',
                'Ingresos Aduana': 'Ingresos_Aduana_Fis',
                'Ingresos Muertos': 'Muertos',
                'Ingresos Cajas': 'Cajas',
                'Total ingresos': 'Total_Ingresos_Col',
                'No. Recorridos meta': 'Meta_Rec',
                'No. Recorridos realizados': 'Real_Rec',
                'Pzas Habilitadas': 'Habilitadas',
                'Pzas Ubicadas': 'Ubicadas'
            }
            
            columnas_a_renombrar = {k: v for k, v in renombres.items() if k in df_sem.columns}
            df_sem.rename(columns=columnas_a_renombrar, inplace=True)
            
            # Si tras la corrección de fila la columna principal no existe, se descarta la hoja por inconsistencia
            if 'Tienda' not in df_sem.columns:
                continue
                
            # Forzar tipado numérico robusto para evitar errores de agregación (TypeErrors)
            columnas_numericas = ['Sis_Aduana', 'Muertos', 'Cajas', 'Habilitadas', 'Ubicadas', 'Meta_Rec', 'Real_Rec']
            for col in columnas_numericas:
                if col in df_sem.columns:
                    df_sem[col] = pd.to_numeric(df_sem[col], errors='coerce').fillna(0)
                else:
                    df_sem[col] = 0
            
            # Filtrado y limpieza profunda de registros basura o filas de separación de días repetidos
            df_sem = df_sem[df_sem['Tienda'].notna()]
            df_sem['Tienda_Str'] = df_sem['Tienda'].astype(str).str.strip().str.lower()
            df_sem = df_sem[~df_sem['Tienda_Str'].str.contains('total|resumen|fecha|tienda|ingresos|registros', na=False)]
            df_sem = df_sem[df_sem['Tienda_Str'] != '']
            
            # Inyección de las dimensiones analíticas fijas por pestaña
            df_sem['Semana'] = nombre_pestana.strip()
            df_sem['Mes'] = "Mayo"  # Valor base estimado de inicio del rango de datos actual
            
            # Lógica de negocio corregida: Sumatoria total del ingreso
            df_sem['Total_Ingresos'] = df_sem['Sis_Aduana'] + df_sem['Muertos'] + df_sem['Cajas']
            
            df_sem.drop(columns=['Tienda_Str'], errors='ignore', inplace=True)
            lista_dataframes.append(df_sem)
            
        if not lista_dataframes:
            st.sidebar.error("Estructura de columnas no reconocida en las pestañas procesadas.")
            return pd.DataFrame()
            
        # Consolidación final en la matriz maestra
        df_consolidado = pd.concat(lista_dataframes, ignore_index=True)
        return df_consolidado
        
    except Exception as e:
        st.sidebar.error(f"Error consolidando pestañas: {e}")
        return pd.DataFrame()

# --- HEADER GENERAL DEL CONTROL DE OPERACIONES ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CONTROL DE OPERACIONES ROPA • MATRIZ MULTI-SEMANAL</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

df_master = get_operational_data()

if df_master.empty:
    st.warning("⚠️ Leyendo la información del libro analítico... Valida los permisos de compartición en Google Sheets de ser necesario.")
else:
    # =========================================================================
    # --- FILTROS LATERALES (SIDEBAR) ---
    # =========================================================================
    st.sidebar.markdown("### 🎛️ Filtros de Operación")
    
    semanas_disponibles = sorted(list(df_master['Semana'].unique()))
    periodo_seleccionado = st.sidebar.selectbox("Selecciona la Semana Operativa:", ["Ver Histórico Conectado"] + semanas_disponibles)
    
    if periodo_seleccionado == "Ver Histórico Conectado":
        df_filtered = df_master.copy()
        label_corte = "(CONSOLIDADO HISTÓRICO)"
    else:
        df_filtered = df_master[df_master['Semana'] == periodo_seleccionado]
        label_corte = f"({periodo_seleccionado.upper()})"

    tiendas_disponibles = sorted(list(df_master['Tienda'].dropna().unique()))
    tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + tiendas_disponibles)

    if tienda != "Todas las Tiendas":
        df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

    # =========================================================================
    # --- RENDERIZADO PRINCIPAL DEL DASHBOARD ---
    # =========================================================================
    if not df_filtered.empty:
        
        st.markdown('<p style="color: #555555; font-weight: bold; font-size: 14px; margin-bottom: 10px; letter-spacing: 0.5px;">📋 DESGLOSE COMPARATIVO INTERSEMANAL DE CONTROL</p>', unsafe_allow_html=True)
        
        # Despliegue de bloques horizontales de resumen para las últimas 4 semanas de la lista
        ultimas_semanas_bloque = semanas_disponibles[-4:]
        cols_semanas = st.columns(len(ultimas_semanas_bloque))
        
        for i, sem in enumerate(ultimas_semanas_bloque):
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

        tab_auditoria, tab_evolutivo = st.tabs(["🔍 Matriz Operativa de Auditoría", "📈 Reporte de Evolución Intersemanal"])

        with tab_auditoria:
            st.markdown(f'<p class="graph-title">📊 Gráficos de Distribución Operativa por Sucursal {label_corte}</p>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            eje_x_dinamico = "Semana" if periodo_seleccionado == "Ver Histórico Conectado" else "Tienda"

            with col_g1:
                df_g1 = df_filtered.groupby(eje_x_dinamico, as_index=False)[["Sis_Aduana", "Muertos", "Cajas"]].sum()
                df_g1["Total_Fila"] = (df_g1["Sis_Aduana"] + df_g1["Muertos"] + df_g1["Cajas"]).replace(0, 1)
                
                pct_sis = (df_g1["Sis_Aduana"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()
                pct_mue = (df_g1["Muertos"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()
                pct_caj = (df_g1["Cajas"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()

                fig1 = go.Figure()
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Sis_Aduana"], name="Aduana Sistema", marker_color='#1F497D', text=pct_sis, textposition='inside'))
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Muertos"], name="
