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
# --- FUENTE DE DATOS OPERATIVOS EN LA NUBE (GOOGLE SHEETS MULTI-PESTAÑA) ---
# =========================================================================
@st.cache_data(ttl=60)
def get_operational_data():
    try:
        # Tu ID de Google Sheets ya integrado
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        
        # URL que fuerza a Google a exportar el archivo completo como un .xlsx tradicional
        URL_EXCEL_NUBE = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        
        response = requests.get(URL_EXCEL_NUBE, timeout=30)
        response.raise_for_status()
        
        excel_bytes = io.BytesIO(response.content)
        
        # Carga la pestaña específica de tu libro (Ajusta 'Checklist' si es necesario)
        df = pd.read_excel(excel_bytes, sheet_name="Checklist", engine="openpyxl")
        
        if df.empty:
            return pd.DataFrame()

        df.columns = df.columns.str.strip()
        
        df.rename(columns={
            'Fecha s': 'Fecha_Corte',
            'Ubicación': 'Tienda',
            'Motivo de ingreso': 'Motivo_Ingreso',
            'Número de Piezas': 'Piezas'
        }, inplace=True)
        
        df['Fecha'] = pd.to_datetime(df['Fecha_Corte'], errors='coerce')
        df = df.dropna(subset=['Fecha'])
        
        df['Piezas'] = pd.to_numeric(df['Piezas'], errors='coerce').fillna(0)
        
        df['Sis_Aduana'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Aduana' else 0, axis=1)
        df['Muertos'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Muertos' else 0, axis=1)
        df['Cajas'] = df.apply(lambda r: r['Piezas'] if str(r.get('Motivo_Ingreso', '')).strip() == 'Cajas' else 0, axis=1)
        
        df['Habilitadas'] = df.apply(lambda r: r['Piezas'] if 'habilitad' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        df['Ubicadas'] = df.apply(lambda r: r['Piezas'] if 'ubica' in str(r.get('Actividad Realizada', '')).lower() else 0, axis=1)
        
        df['Meta_Rec'] = 8.0  
        df['Real_Rec'] = df.apply(lambda r: 1.0 if 'recorrido' in str(r.get('Tabla', '')).lower() else 0, axis=1)
        
        # Regla de negocio: Sumatoria total del ingreso
        df['Total_Ingresos'] = df['Sis_Aduana'] + df['Muertos'] + df['Cajas']
        
        # Mapeo de días de la semana para ordenación limpia y sin duplicar fechas
        dias_espanol = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        df['Dia_Semana_Num'] = df['Fecha'].dt.dayofweek
        df['Dia_Nombre'] = df['Dia_Semana_Num'].map(dias_espanol)
        
        df['Semana'] = "Semana " + df['Fecha'].dt.isocalendar().week.astype(str)
        df['Mes'] = df['Fecha'].dt.strftime('%B').replace({
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        })
        
        return df
        
    except Exception as e:
        st.sidebar.error(f"Error en la lectura de la nube: {e}")
        return pd.DataFrame()

# --- HEADER GENERAL DEL CONTROL DE OPERACIONES ---
st.markdown('<p class="main-title">👚 PRICE SHOES • Operaciones Ropa</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CONTROL DE OPERACIONES ROPA</p>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0; height: 1px; background: #D9D9D9; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)

df_master = get_operational_data()

if df_master.empty:
    st.warning("⚠️ Cargando datos desde Google Sheets... Si el error persiste, comprueba que el archivo esté compartido en modo 'Cualquier persona con el enlace'.")
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

        tab_auditoria, tab_evolutivo = st.tabs(["🔍 Matriz Operativa de Auditoría", "📈 Reporte de Evolución Intersemanal"])

        with tab_auditoria:
            st.markdown(f'<p class="graph-title">📊 Gráficos de Distribución Operativa por Sucursal {label_corte}</p>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            eje_x_dinamico = "Tienda" if tienda == "Todas las Tiendas" else ("Semana" if tipo_periodo == "Por Semana" else "Dia_Nombre")

            with col_g1:
                df_g1 = df_filtered.groupby(eje_x_dinamico, as_index=False)[["Sis_Aduana", "Muertos", "Cajas"]].sum()
                df_g1["Total_Fila"] = (df_g1["Sis_Aduana"] + df_g1["Muertos"] + df_g1["Cajas"]).replace(0, 1)
                
                pct_sis = (df_g1["Sis_Aduana"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()
                pct_mue = (df_g1["Muertos"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()
                pct_caj = (df_g1["Cajas"] / df_g1["Total_Fila"] * 100).map('{:.1f}%'.format).tolist()
                
                if eje_x_dinamico == "Dia_Nombre":
                    orden_dias = {"Lunes":0, "Martes":1, "Miércoles":2, "Jueves":3, "Viernes":4, "Sábado":5, "Domingo":6}
                    df_g1['orden'] = df_g1['Dia_Nombre'].map(orden_dias)
                    df_g1 = df_g1.sort_values('orden').drop(columns=['orden'])

                fig1 = go.Figure()
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Sis_Aduana"], name="Sis_Aduana", marker_color='#1F497D', text=pct_sis, textposition='inside'))
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Muertos"], name="Muertos", marker_color='#E6007E', text=pct_mue, textposition='inside'))
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Cajas"], name="Cajas", marker_color='#7F7F7F', text=pct_caj, textposition='inside'))
                fig1.update_layout(title="<b>Distribución y % de Composición de Ingresos</b>", barmode='stack', barnorm='percent', plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig1, use_container_width=True)

            with col_g2:
                if eje_x_dinamico in ["Semana", "Tienda"]:
                    df_g2 = df_filtered.groupby(eje_x_dinamico, as_index=False).agg(Total_Ingresos=('Total_Ingresos', 'sum'), Habilitadas=('Habilitadas', 'sum'))
                else:
                    df_g2 = df_filtered.groupby(["Dia_Semana_Num", "Dia_Nombre"], as_index=False).agg(Total_Ingresos=('Total_Ingresos', 'sum'), Habilitadas=('Habilitadas', 'sum')).sort_values("Dia_Semana_Num")

                df_g2['Porcentaje_Habilitado'] = (df_g2['Habilitadas'] / df_g2['Total_Ingresos'] * 100).fillna(0)
                
                fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                fig2.add_trace(go.Bar(x=df_g2[eje_x_dinamico], y=df_g2['Porcentaje_Habilitado'], name="% Habilitado", marker_color='#1F497D', text=df_g2['Porcentaje_Habilitado'].map('{:.1f}%'.format), textposition='inside'), secondary_y=False)
                fig2.add_trace(go.Scatter(x=df_g2[eje_x_dinamico], y=df_g2['Total_Ingresos'], name="Total Ingresos", mode='lines+markers', line=dict(color='#E6007E', width=3)), secondary_y=True)
                fig2.update_layout(title_text="<b>Rendimiento: % Habilitado vs Volumen</b>", plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown(f'<p class="graph-title">🔍 Matriz General de Auditoría Operativa {label_corte}</p>', unsafe_allow_html=True)

            html_table = """
            <table class="tabla-auditoria">
                <tbody>
                    <tr>
                        <td>Clasificación</td><td>Tienda</td><td>Aduana Sist.</td><td>Aduana Fís.</td>
                        <td>Muertos</td><td>Cajas</td><td>Total Ingresos</td><td>Piezas Habilitadas</td>
                        <td>% Recorridos</td><td>% Habilitado</td><td>Ubicado %</td>
                    </tr>
            """
            
            agrupadores = ["Semana", "Tienda"] if (tipo_periodo == "Por Semana" or periodo_seleccionado == "Todos los Meses") else ["Dia_Nombre", "Dia_Semana_Num", "Tienda"]
            df_table = df_filtered.groupby(agrupadores, as_index=False).agg({
                "Sis_Aduana": "sum", "Muertos": "sum", "Cajas": "sum",
                "Total_Ingresos": "sum", "Habilitadas": "sum", "Ubicadas": "sum", "Meta_Rec": "sum", "Real_Rec": "sum"
            })
            df_table["Fis_Aduana"] = 0
            
            if tipo_periodo == "Por Semana" or periodo_seleccionado == "Todos los Meses":
                df_table = df_table.sort_values(by=["Semana", "Tienda"])
                grouped_matrix = df_table.groupby("Semana", sort=False)
            else:
                df_table = df_table.sort_values(by=["Dia_Semana_Num", "Tienda"])
                grouped_matrix = df_table.groupby("Dia_Nombre", sort=False)
            
            for bloque_id, sub_grupo in grouped_matrix:
                limite_filas = len(sub_grupo)
                es_primera_fila = True
                
                for index, row in sub_grupo.iterrows():
                    html_table += '<tr style="border-bottom: 1px solid #EFEFEF;">'
                    if es_primera_fila:
                        html_table += f'<td rowspan="{limite_filas}" style="padding: 10px; border: 1px solid #D9D9D9; font-weight: bold; text-align: center; background-color: #F9FBFD; color: #1F497D; vertical-align: middle;">{bloque_id}</td>'
                        es_primera_fila = False
                        
                    tot_ing = row["Total_Ingresos"]
                    html_table += f'<td class="cell-center" style="font-weight: bold;">{row["Tienda"]}</td>'
                    html_table += f'<td class="cell-td">{int(row["Sis_Aduana"]):,}</td>'
                    html_table += f'<td class="cell-td">{int(row["Fis_Aduana"]):,}</td>'
                    html_table += f'<td class="cell-td">{int(row["Muertos"]):,}</td>'
                    html_table += f'<td class="cell-td">{int(row["Cajas"]):,}</td>'
                    html_table += f'<td class="cell-td" style="font-weight: bold; background-color: #F9F9F9;">{int(tot_ing):,}</td>'
                    html_table += f'<td class="cell-td">{int(row["Habilitadas"]):,}</td>'
                    
                    v_ef = (row["Real_Rec"] / row["Meta_Rec"] * 100) if row["Meta_Rec"] > 0 else 0
                    bg_ef = "#FADBD8" if v_ef < 85.0 else ("#D4E6F1" if v_ef >= 100.0 else "#FFFFFF")
                    tx_ef = "#78281F" if v_ef < 85.0 else ("#1B4F72" if v_ef >= 100.0 else "#000000")
                    html_table += f'<td class="cell-center" style="font-weight: bold; background-color: {bg_ef}; color: {tx_ef};">{v_ef:.1f}%</td>'
                    
                    v_hab = (row["Habilitadas"] / tot_ing * 100) if tot_ing > 0 else 0
                    bg_hab = "#FADBD8" if v_hab < 85.0 else ("#D4E6F1" if v_hab >= 100.0 else "#FFFFFF")
                    tx_hab = "#78281F" if v_hab < 85.0 else ("#1B4F72" if v_hab >= 100.0 else "#000000")
                    html_table += f'<td class="cell-center" style="font-weight: bold; background-color: {bg_hab}; color: {tx_hab};">{v_hab:.1f}%</td>'
                    
                    v_ub = (row["Ubicadas"] / tot_ing * 100) if tot_ing > 0 else 0
                    bg_ub = "#FADBD8" if v_ub < 85.0 else ("#D4E6F1" if v_ub >= 100.0 else "#FFFFFF")
                    tx_ub = "#78281F" if v_ub < 85.0 else ("#1B4F72" if v_ub >= 100.0 else "#000000")
                    html_table += f'<td class="cell-center" style="font-weight: bold; background-color: {bg_ub}; color: {tx_ub};">{v_ub:.1f}%</td>'
                    html_table += '</tr>'
                    
            html_table += "</tbody></table>"
            st.markdown(html_table, unsafe_allow_html=True)

        with tab_evolutivo:
            st.markdown('<p class="graph-title">📈 Análisis de Tendencia y Variación Intersemanal</p>', unsafe_allow_html=True)

            df_evolutivo = df_master[df_master['Semana'].isin(ultimas_4_semanas)].copy()
            if tienda != "Todas las Tiendas":
                df_evolutivo = df_evolutivo[df_evolutivo['Tienda'] == tienda]

            df_metrics_sem = df_evolutivo.groupby("Semana").agg({"Total_Ingresos": "sum", "Habilitadas": "sum", "Ubicadas": "sum", "Meta_Rec": "sum", "Real_Rec": "sum"}).reindex(ultimas_4_semanas)
            df_metrics_sem['% Habilitado'] = (df_metrics_sem['Habilitadas'] / df_metrics_sem['Total_Ingresos'] * 100).fillna(0)
            df_metrics_sem['% Recorridos'] = (df_metrics_sem['Real_Rec'] / df_metrics_sem['Meta_Rec'] * 100).fillna(0)

            df_metrics_sem['Var_Ing_Abs'] = df_metrics_sem['Total_Ingresos'].diff()
            df_metrics_sem['Var_Ing_Pct'] = df_metrics_sem['Total_Ingresos'].pct_change() * 100
            df_metrics_sem['Var_Hab_Abs'] = df_metrics_sem['Habilitadas'].diff()
            df_metrics_sem['Var_Hab_Pct'] = df_metrics_sem['Habilitadas'].pct_change() * 100
            df_metrics_sem['Var_Delta_Recorridos'] = df_metrics_sem['% Recorridos'].diff()

            html_comparativo = """
            <table class="tabla-auditoria">
                <tbody>
                    <tr>
                        <td>Dimensión Temporal</td><td>📥 Vol. Ingresos Total</td><td>Δ Vs. Sem Anterior</td>
                        <td>✨ Piezas Habilitadas</td><td>Δ Vs. Sem Anterior</td>
                        <td>🎯 % Rendimiento Recorridos</td><td>Δ Eficiencia Recorridos</td>
                    </tr>
            """

            for idx, (sem, row) in enumerate(df_metrics_sem.iterrows()):
                if idx == 0:
                    delta_ing = '<span style="color:#7F7F7F; font-size:11px;">N/A (Línea Base)</span>'
                    delta_hab = '<span style="color:#7F7F7F; font-size:11px;">N/A</span>'
                    delta_rec = '<span style="color:#7F7F7F; font-size:11px;">N/A</span>'
                else:
                    c_ing = "#E6007E" if row['Var_Ing_Abs'] < 0 else "#1F497D"
                    signo_ing = "" if row['Var_Ing_Abs'] < 0 else "+"
                    delta_ing = f'<b style="color:{c_ing};">{signo_ing}{int(row["Var_Ing_Abs"]):,} u. ({signo_ing}{row["Var_Ing_Pct"]:.1f}%)</b>'
                    
                    c_hab = "#E6007E" if row['Var_Hab_Abs'] < 0 else "#1F497D"
                    signo_hab = "" if row['Var_Hab_Abs'] < 0 else "+"
                    delta_hab = f'<b style="color:{c_hab};">{signo_hab}{int(row["Var_Hab_Abs"]):,} u. ({signo_hab}{row["Var_Hab_Pct"]:.1f}%)</b>'
                    
                    c_rec = "#E6007E" if row['Var_Delta_Recorridos'] < 0 else "#229954"
                    signo_rec = "" if row['Var_Delta_Recorridos'] < 0 else "+"
                    delta_rec = f'<span style="color:{c_rec}; font-weight:bold;">{signo_rec}{row["Var_Delta_Recorridos"]:.1f} pp</span>'

                html_comparativo += f"""
                <tr style="border-bottom: 1px solid #EFEFEF; height:38px;">
                    <td class="cell-center" style="font-weight: bold; background-color: #F9FBFD; color: #1F497D;">{sem}</td>
                    <td class="cell-td" style="font-weight: bold;">{int(row['Total_Ingresos']):,}</td>
                    <td class="cell-center" style="font-size:12px;">{delta_ing}</td>
                    <td class="cell-td" style="font-weight: bold;">{int(row['Habilitadas']):,} <small style="color:#555;">({row['% Habilitado']:.1f}%)</small></td>
                    <td class="cell-center" style="font-size:12px;">{delta_hab}</td>
                    <td class="cell-center" style="font-weight: bold;">{row['% Recorridos']:.1f}%</td>
                    <td class="cell-center" style="font-size:12px;">{delta_rec}</td>
                </tr>
                """

            html_comparativo += "</tbody></table>"
            st.markdown(html_comparativo, unsafe_allow_html=True)

            fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
            fig_trend.add_trace(go.Scatter(x=df_metrics_sem.index, y=df_metrics_sem['% Habilitado'], name="Evolución % Habilitado", mode='lines+markers+text', text=df_metrics_sem['% Habilitado'].map('{:.1f}%'.format), textposition="top center", line=dict(color='#1F497D', width=3)), secondary_y=False)
            fig_trend.add_trace(go.Scatter(x=df_metrics_sem.index, y=df_metrics_sem['% Recorridos'], name="Evolución % Recorridos", mode='lines+markers+text', text=df_metrics_sem['% Recorridos'].map('{:.1f}%'.format), textposition="bottom center", line=dict(color='#E6007E', width=3, dash='dash')), secondary_y=False)
            fig_trend.add_trace(go.Bar(x=df_metrics_sem.index, y=df_metrics_sem['Total_Ingresos'], name="Volumen Total Ingresos", marker_color='#7F7F7F', opacity=0.12), secondary_y=True)
            fig_trend.update_layout(title="<b>Línea de Tendencia: Desempeño Operativo vs Volumen de Entrada</b>", plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_trend, use_container_width=True)

    else:
        st.warning("No se encontraron registros con los filtros aplicados.")

st.markdown("<br><p style='font-size:11px; color:#999999; text-align: center;'>REPORTES DE DIRECCIÓN DE OPERACIONES • PRICE SHOES ROPA • CONFIDENCIAL</p>", unsafe_allow_html=True)
