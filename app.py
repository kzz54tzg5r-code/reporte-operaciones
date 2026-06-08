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
# --- FUENTE DE DATOS CONSOLIDADA MULTI-PESTAÑA ---
# =========================================================================
@st.cache_data(ttl=60)
def get_operational_data():
    try:
        ID_DOCUMENTO = "18jY8e9houYYTgX2TqWwS-clbzGAjbQzi4tjW7wOR2vI"
        URL_EXCEL_NUBE = f"https://docs.google.com/spreadsheets/d/{ID_DOCUMENTO}/export?format=xlsx"
        
        response = requests.get(URL_EXCEL_NUBE, timeout=30)
        response.raise_for_status()
        
        excel_bytes = io.BytesIO(response.content)
        
        # Leemos todas las pestañas disponibles en el archivo
        excel_file = pd.ExcelFile(excel_bytes, engine="openpyxl")
        todas_las_pestanas = excel_file.sheet_names
        
        # Filtramos para quedarnos únicamente con las que empiezan con "Sem"
        pestanas_semanas = [p for p in todas_las_pestanas if p.strip().lower().startswith("sem")]
        
        if not pestanas_semanas:
            st.sidebar.error("No se encontraron pestañas que inicien con 'Sem' en el archivo.")
            return pd.DataFrame()
            
        lista_dataframes = []
        
        # Mapeo de meses en español
        meses_espanol = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        
        # Iteramos y procesamos cada pestaña de semana
        for nombre_pestana in pestanas_semanas:
            # Saltamos la fila de encabezados decorativos superiores y leemos la matriz limpia
            df_sem = pd.read_excel(excel_file, sheet_name=nombre_pestana, skiprows=1, engine="openpyxl")
            
            if df_sem.empty:
                continue
                
            # Limpieza básica de nombres de columnas
            df_sem.columns = df_sem.columns.str.strip()
            
            # Buscamos las columnas requeridas según la estructura de la imagen
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
            
            # Filtrar columnas existentes en la hoja actual para evitar ValueErrors si hay variaciones
            columnas_a_renombrar = {k: v for k, v in renombres.items() if k in df_sem.columns}
            df_sem.rename(columns=columnas_a_renombrar, inplace=True)
            
            # Forzar tipos de datos numéricos en métricas críticas
            columnas_numericas = ['Sis_Aduana', 'Muertos', 'Cajas', 'Habilitadas', 'Ubicadas', 'Meta_Rec', 'Real_Rec']
            for col in columnas_numericas:
                if col in df_sem.columns:
                    df_sem[col] = pd.to_numeric(df_sem[col], errors='coerce').fillna(0)
                else:
                    df_sem[col] = 0
            
            # Descartar filas vacías, totales generales del excel o filas de separación
            df_sem = df_sem[df_sem['Tienda'].notna()]
            df_sem = df_sem[~df_sem['Tienda'].str.contains('total|resumen|fecha', case=False, na=False)]
            
            # Asignación de la dimensión temporal basada en la pestaña actual
            df_sem['Semana'] = nombre_pestana.strip()
            
            # Para el mes e histórico, si no viene la columna fecha fija por fila, asignamos un estimado base
            # (Puedes cambiar la lógica de fecha si agregas una columna limpia de fecha por fila)
            df_sem['Mes'] = "Mayo"  # Valor base de inicio según la imagen (Sem 20 - 4 de Mayo)
            
            # Regla de negocio: total de ingresos calculados por fórmula operativa
            df_sem['Total_Ingresos'] = df_sem['Sis_Aduana'] + df_sem['Muertos'] + df_sem['Cajas']
            
            lista_dataframes.append(df_sem)
            
        if not lista_dataframes:
            return pd.DataFrame()
            
        # Unificamos todas las semanas en un único DataFrame Maestro
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
    st.warning("⚠️ Extrayendo y unificando las pestañas semanales... Comprueba que las hojas mantengan el prefijo 'Sem ' en Google Sheets.")
else:
    # =========================================================================
    # --- FILTROS LATERALES (SIDEBAR) ---
    # =========================================================================
    st.sidebar.markdown("### 🎛️ Filtros de Operación")
    
    # Selector de periodos dinámico basado en las pestañas reales que vayas agregando
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
        
        # Mostramos las últimas 4 semanas agregadas en tarjetas ejecutivas de KPI
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
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Muertos"], name="Muertos", marker_color='#E6007E', text=pct_mue, textposition='inside'))
                fig1.add_trace(go.Bar(x=df_g1[eje_x_dinamico], y=df_g1["Cajas"], name="Cajas", marker_color='#7F7F7F', text=pct_caj, textposition='inside'))
                fig1.update_layout(title="<b>Composición Porcentual de Ingresos por Tipo</b>", barmode='stack', barnorm='percent', plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig1, use_container_width=True)

            with col_g2:
                df_g2 = df_filtered.groupby(eje_x_dinamico, as_index=False).agg(Total_Ingresos=('Total_Ingresos', 'sum'), Habilitadas=('Habilitadas', 'sum'))
                df_g2['Porcentaje_Habilitado'] = (df_g2['Habilitadas'] / df_g2['Total_Ingresos'] * 100).fillna(0)
                
                fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                fig2.add_trace(go.Bar(x=df_g2[eje_x_dinamico], y=df_g2['Porcentaje_Habilitado'], name="% Habilitado", marker_color='#1F497D', text=df_g2['Porcentaje_Habilitado'].map('{:.1f}%'.format), textposition='inside'), secondary_y=False)
                fig2.add_trace(go.Scatter(x=df_g2[eje_x_dinamico], y=df_g2['Total_Ingresos'], name="Total Ingresos", mode='lines+markers', line=dict(color='#E6007E', width=3)), secondary_y=True)
                fig2.update_layout(title_text="<b>Rendimiento Operativo: % Habilitado vs Volumen Total</b>", plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20))
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown(f'<p class="graph-title">🔍 Matriz General de Auditoría Unificada {label_corte}</p>', unsafe_allow_html=True)

            html_table = """
            <table class="tabla-auditoria">
                <tbody>
                    <tr>
                        <td>Clasificación</td><td>Tienda</td><td>Aduana Sist.</td>
                        <td>Muertos</td><td>Cajas</td><td>Total Ingresos</td><td>Piezas Habilitadas</td>
                        <td>% Recorridos</td><td>% Habilitado</td><td>Ubicado %</td>
                    </tr>
            """
            
            df_table = df_filtered.groupby(["Semana", "Tienda"], as_index=False).agg({
                "Sis_Aduana": "sum", "Muertos": "sum", "Cajas": "sum",
                "Total_Ingresos": "sum", "Habilitadas": "sum", "Ubicadas": "sum", "Meta_Rec": "sum", "Real_Rec": "sum"
            }).sort_values(by=["Semana", "Tienda"])
            
            grouped_matrix = df_table.groupby("Semana", sort=False)
            
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
            st.markdown('<p class="graph-title">📈 Análisis de Tendencia de Productividad Anual</p>', unsafe_allow_html=True)

            df_metrics_sem = df_master.groupby("Semana").agg({"Total_Ingresos": "sum", "Habilitadas": "sum", "Ubicadas": "sum", "Meta_Rec": "sum", "Real_Rec": "sum"}).reindex(semanas_disponibles)
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
                    delta_ing = '<span style="color:#7F7F7F; font-size:11px;">Línea Base</span>'
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
            fig_trend.update_layout(title="<b>Línea de Tendencia Histórica e Incremental</b>", plot_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_trend, use_container_width=True)

    else:
        st.warning("No se encontraron registros válidos.")

st.markdown("<br><p style='font-size:11px; color:#999999; text-align: center;'>REPORTES DE DIRECCIÓN DE OPERACIONES • PRICE SHOES ROPA • CONFIDENCIAL</p>", unsafe_allow_html=True)
