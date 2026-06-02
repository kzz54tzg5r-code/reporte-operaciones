import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE BI ---
st.set_page_config(page_title="BI - Control de Operaciones", layout="wide", page_icon="📊")

# --- DATASET CONSOLIDADO DEL PDF ---
@st.cache_data
def get_operational_data():
    data = [
        # Lunes 25
        {"Fecha": "2026-05-25", "Tienda": "Vallejo", "Sis_Aduana": 293, "Fis_Aduana": 332, "Muertos": 32, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 229, "Habilitadas": 248, "Ubicadas": 356},
        {"Fecha": "2026-05-25", "Tienda": "Arco Norte", "Sis_Aduana": 109, "Fis_Aduana": 82, "Muertos": 36, "Cajas": 73, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 109, "Habilitadas": 409, "Ubicadas": 545},
        {"Fecha": "2026-05-25", "Tienda": "Puebla Sur", "Sis_Aduana": 79, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 185, "Ubicadas": 197},
        {"Fecha": "2026-05-25", "Tienda": "Miravalle", "Sis_Aduana": 44, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Martes 26
        {"Fecha": "2026-05-26", "Tienda": "Vallejo", "Sis_Aduana": 441, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 235, "Meta_Rec": 5, "Real_Rec": 5, "Recolectadas": 235, "Habilitadas": 595, "Ubicadas": 381},
        {"Fecha": "2026-05-26", "Tienda": "Arco Norte", "Sis_Aduana": 164, "Fis_Aduana": 75, "Muertos": 30, "Cajas": 144, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 174, "Habilitadas": 201, "Ubicadas": 309},
        {"Fecha": "2026-05-26", "Tienda": "Puebla Sur", "Sis_Aduana": 113, "Fis_Aduana": 108, "Muertos": 98, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 4, "Recolectadas": 98, "Habilitadas": 116, "Ubicadas": 198},
        {"Fecha": "2026-05-26", "Tienda": "Miravalle", "Sis_Aduana": 47, "Fis_Aduana": 37, "Muertos": 39, "Cajas": 17, "Meta_Rec": 5, "Real_Rec": 2, "Recolectadas": 39, "Habilitadas": 81, "Ubicadas": 129},
        
        # Miércoles 27
        {"Fecha": "2026-05-27", "Tienda": "Vallejo", "Sis_Aduana": 436, "Fis_Aduana": 441, "Muertos": 0, "Cajas": 197, "Meta_Rec": 5, "Real_Rec": 3, "Recolectadas": 197, "Habilitadas": 478, "Ubicadas": 452},
        {"Fecha": "2026-05-27", "Tienda": "Arco Norte", "Sis_Aduana": 170, "Fis_Aduana": 47, "Muertos": 51, "Cajas": 51, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 102, "Habilitadas": 171, "Ubicadas": 350},
        {"Fecha": "2026-05-27", "Tienda": "Puebla Sur", "Sis_Aduana": 67, "Fis_Aduana": 65, "Muertos": 160, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 6, "Recolectadas": 160, "Habilitadas": 307, "Ubicadas": 617},
        {"Fecha": "2026-05-27", "Tienda": "Miravalle", "Sis_Aduana": 64, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Jueves 28
        {"Fecha": "2026-05-28", "Tienda": "Vallejo", "Sis_Aduana": 550, "Fis_Aduana": 563, "Muertos": 168, "Cajas": 224, "Meta_Rec": 8, "Real_Rec": 8, "Recolectadas": 392, "Habilitadas": 755, "Ubicadas": 452},
        {"Fecha": "2026-05-28", "Tienda": "Arco Norte", "Sis_Aduana": 200, "Fis_Aduana": 134, "Muertos": 103, "Cajas": 75, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 178, "Habilitadas": 84, "Ubicadas": 350},
        {"Fecha": "2026-05-28", "Tienda": "Puebla Sur", "Sis_Aduana": 131, "Fis_Aduana": 146, "Muertos": 103, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 103, "Habilitadas": 32, "Ubicadas": 617},
        {"Fecha": "2026-05-28", "Tienda": "Miravalle", "Sis_Aduana": 57, "Fis_Aduana": 4, "Muertos": 31, "Cajas": 6, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 37, "Habilitadas": 0, "Ubicadas": 0},
        
        # Viernes 29
        {"Fecha": "2026-05-29", "Tienda": "Vallejo", "Sis_Aduana": 571, "Fis_Aduana": 596, "Muertos": 282, "Cajas": 196, "Meta_Rec": 5, "Real_Rec": 14, "Recolectadas": 503, "Habilitadas": 1017, "Ubicadas": 2099},
        {"Fecha": "2026-05-29", "Tienda": "Arco Norte", "Sis_Aduana": 260, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 22, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 22, "Habilitadas": 0, "Ubicadas": 0},
        {"Fecha": "2026-05-29", "Tienda": "Puebla Sur", "Sis_Aduana": 160, "Fis_Aduana": 152, "Muertos": 39, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 39, "Habilitadas": 226, "Ubicadas": 384},
        {"Fecha": "2026-05-29", "Tienda": "Miravalle", "Sis_Aduana": 55, "Fis_Aduana": 7, "Muertos": 14, "Cajas": 0, "Meta_Rec": 5, "Real_Rec": 1, "Recolectadas": 14, "Habilitadas": 58, "Ubicadas": 105},
        
        # Sábado 30
        {"Fecha": "2026-05-30", "Tienda": "Vallejo", "Sis_Aduana": 513, "Fis_Aduana": 0, "Muertos": 68, "Cajas": 363, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 431, "Habilitadas": 624, "Ubicadas": 611},
        {"Fecha": "2026-05-30", "Tienda": "Arco Norte", "Sis_Aduana": 240, "Fis_Aduana": 246, "Muertos": 60, "Cajas": 115, "Meta_Rec": 8, "Real_Rec": 4, "Recolectadas": 175, "Habilitadas": 206, "Ubicadas": 1083},
        {"Fecha": "2026-05-30", "Tienda": "Puebla Sur", "Sis_Aduana": 85, "Fis_Aduana": 70, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 70, "Ubicadas": 70},
        {"Fecha": "2026-05-30", "Tienda": "Miravalle", "Sis_Aduana": 88, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0},
        
        # Domingo 31
        {"Fecha": "2026-05-31", "Tienda": "Vallejo", "Sis_Aduana": 351, "Fis_Aduana": 351, "Muertos": 326, "Cajas": 488, "Meta_Rec": 8, "Real_Rec": 16, "Recolectadas": 884, "Habilitadas": 705, "Ubicadas": 2605},
        {"Fecha": "2026-05-31", "Tienda": "Arco Norte", "Sis_Aduana": 264, "Fis_Aduana": 107, "Muertos": 57, "Cajas": 78, "Meta_Rec": 8, "Real_Rec": 3, "Recolectadas": 135, "Habilitadas": 784, "Ubicadas": 482},
        {"Fecha": "2026-05-31", "Tienda": "Puebla Sur", "Sis_Aduana": 104, "Fis_Aduana": 110, "Muertos": 198, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 2, "Recolectadas": 198, "Habilitadas": 340, "Ubicadas": 440},
        {"Fecha": "2026-05-31", "Tienda": "Miravalle", "Sis_Aduana": 41, "Fis_Aduana": 0, "Muertos": 0, "Cajas": 0, "Meta_Rec": 8, "Real_Rec": 0, "Recolectadas": 0, "Habilitadas": 0, "Ubicadas": 0}
    ]
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Métricas estándar calculadas del reporte de origen
    df['Total_Ingresos'] = df['Fis_Aduana'] + df['Muertos'] + df['Cajas']
    df['Eficiencia_Recorridos'] = (df['Real_Rec'] / df['Meta_Rec']) * 100
    df['Utilizacion_Habilitado'] = (
        (df['Habilitadas'] / df['Recolectadas'])
        .replace([float('inf'), -float('inf')], 0)
        .fillna(0) * 100
    )
    # NUEVA COLUMNA: % Ubicado calculado vectorialmente para evitar divisiones entre cero
    df['Porcentaje_Ubicado'] = (
        (df['Ubicadas'] / df['Recolectadas'])
        .replace([float('inf'), -float('inf')], 0)
        .fillna(0) * 100
    )
    return df

df = get_operational_data()

# --- INTERFAZ ---
st.title("📊 Panel Control Operativo de Cambios y Muertos")
st.markdown("**Periodo:** *Semana 21 (25 al 31 de Mayo de 2026)*")

# Sidebar
st.sidebar.markdown("### 🎛️ Filtros de Control")
tienda = st.sidebar.selectbox("Seleccionar Sucursal", ["Todas las Tiendas"] + list(df['Tienda'].unique()))

min_date = df['Fecha'].min().date()
max_date = df['Fecha'].max().date()
fecha_rango = st.sidebar.date_input("Rango Temporal", [min_date, max_date])

# Filtrado Dinámico
df_filtered = df.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]

if len(fecha_rango) == 2:
    start_date, end_date = fecha_rango
    df_filtered = df_filtered[(df_filtered['Fecha'].dt.date >= start_date) & (df_filtered['Fecha'].dt.date <= end_date)]

# --- TARJETAS KPI CON COLORIZACIÓN DINÁMICA ---
if not df_filtered.empty:
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown("<div style='padding:15px; border-radius:10px; background-color:#EBF5FB; border-left: 5px solid #2980B9;'><strong>Total Ingresos</strong><br><span style='font-size:24px; font-weight:bold; color:#1F618D;'>{:,}</span></div>".format(df_filtered['Total_Ingresos'].sum()), unsafe_allow_html=True)
    with kpi_col2:
        st.markdown("<div style='padding:15px; border-radius:10px; background-color:#E8F8F5; border-left: 5px solid #117A65;'><strong>Promedio Eficiencia Rec.</strong><br><span style='font-size:24px; font-weight:bold; color:#117A65;'>{:.1f}%</span></div>".format(df_filtered['Eficiencia_Recorridos'].mean()), unsafe_allow_html=True)
    with kpi_col3:
        st.markdown("<div style='padding:15px; border-radius:10px; background-color:#FEF9E7; border-left: 5px solid #F1C40F;'><strong>Piezas en Piso (Ubicadas)</strong><br><span style='font-size:24px; font-weight:bold; color:#9A7D0A;'>{:,}</span></div>".format(df_filtered['Ubicadas'].sum()), unsafe_allow_html=True)
    with kpi_col4:
        diff_aduana = df_filtered['Fis_Aduana'].sum() - df_filtered['Sis_Aduana'].sum()
        bg_color = "#FDEDEC" if diff_aduana < 0 else "#E8F8F5"
        border_color = "#C0392B" if diff_aduana < 0 else "#27AE60"
        text_color = "#7B241C" if diff_aduana < 0 else "#1E8449"
        st.markdown(f"<div style='padding:15px; border-radius:10px; background-color:{bg_color}; border-left: 5px solid {border_color};'><strong>Desviación Aduana (Fís vs Sis)</strong><br><span style='font-size:24px; font-weight:bold; color:{text_color};'>{diff_aduana:+,}</span></div>", unsafe_allow_html=True)

    st.write("")

    # --- SECCIÓN GRÁFICA ALTO CONTRASTE ---
    col_izq, col_der = st.columns([3, 2])

    with col_izq:
        st.markdown("#### 📈 Carga Operativa Temporal (Ingreso Diario vs Ubicación)")
        df_trend = df_filtered.groupby("Fecha").sum().reset_index()
        
        fig_dual = go.Figure()
        # Barras de ingresos en azul eléctrico para resaltar volumen
        fig_dual.add_trace(go.Bar(
            x=df_trend['Fecha'], y=df_trend['Total_Ingresos'],
            name='Total Ingresos', marker_color='#2471A3', opacity=0.85
        ))
        # Línea de ubicación en verde vibrante para resaltar efectividad de meta
        fig_dual.add_trace(go.Scatter(
            x=df_trend['Fecha'], y=df_trend['Ubicadas'],
            name='Piezas Ubicadas', mode='lines+markers',
            line=dict(color='#2ECC71', width=4), marker=dict(size=8)
        ))
        fig_dual.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=30, b=10), hovermode="x unified", height=380
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    with col_der:
        st.markdown("#### 🏆 KPIs de Productividad Promedio por Sucursal")
        df_tienda = df_filtered.groupby("Tienda").mean().reset_index()
        
        fig_bar = go.Figure()
        # Barras de eficiencia de recorridos en coral encendido
        fig_bar.add_trace(go.Bar(
            y=df_tienda['Tienda'], x=df_tienda['Eficiencia_Recorridos'],
            name='% Eficiencia Recorridos', orientation='h', marker_color='#E74C3C'
        ))
        # Barras de ubicación porcentual en morado operativo
        fig_bar.add_trace(go.Bar(
            y=df_tienda['Tienda'], x=df_tienda['Porcentaje_Ubicado'],
            name='% Promedio Ubicado', orientation='h', marker_color='#8E44AD'
        ))
        fig_bar.update_layout(
            barmode='group', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=30, b=10), height=380
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- TABLA DE AUDITORÍA CON MATRIZ DE COLOR EN LOS PORCENTAJES ---
    st.markdown("#### 🔍 Matriz de Auditoría Operativa con Indicadores")
    
    # Formateamos la visualización final agregando barras de progreso de color directo a la tabla
    st.dataframe(
        df_filtered.sort_values("Fecha", ascending=False),
        column_config={
            "Fecha": st.column_config.DateColumn("Día de Operación"),
            "Tienda": "Sucursal",
            "Sis_Aduana": "Aduana (Sistema)",
            "Fis_Aduana": "Aduana (Físico)",
            "Muertos": "Muertos",
            "Cajas": "Cajas",
            "Total_Ingresos": "Ingresos Totales",
            "Eficiencia_Recorridos": st.column_config.ProgressColumn(
                "Eficiencia Recorridos", format="%.0f%%", min_value=0, max_value=280
            ),
            "Utilizacion_Habilitado": st.column_config.NumberColumn(
                "Utilización Habilitado", format="%.1f%%"
            ),
            # NUEVA COLUMNA VISUALIZADA: % Ubicado mapeado como una barra de progreso morada/azul
            "Porcentaje_Ubicado": st.column_config.ProgressColumn(
                "% Ubicado (Salida)", format="%.0f%%", min_value=0, max_value=260
            ),
            "Ubicadas": "Unidades en Piso"
        }, hide_index=True, use_container_width=True
    )
else:
    st.warning("No hay registros disponibles para los filtros seleccionados actualmente.")

st.info("Nota de BI: Las eficiencias superiores al 100% reflejan el procesamiento de rezagos acumulados de turnos anteriores.")
