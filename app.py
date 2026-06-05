# --- PANEL DE CONTROL (BARRA LATERAL) ---
st.sidebar.markdown("### 🎛️ Filtros de Operación")
tipo_periodo = st.sidebar.radio("Agrupar Reporte por:", ["Por Semana", "Por Mes"])

if tipo_periodo == "Por Semana":
    periodo_seleccionado = st.sidebar.selectbox("Selecciona la Semana Operativa:", sorted(list(df_master['Semana'].unique())))
    df_filtrado_periodo = df_master[df_master['Semana'] == periodo_seleccionado]
    label_corte = f"({periodo_seleccionado.upper()})"
else:
    # Opción añadida para consolidar todo el histórico mensual
    periodo_seleccionado = st.sidebar.selectbox("Selecciona el Mes Operativo:", ["Todos los Meses", "Mayo", "Junio"])
    if periodo_seleccionado == "Todos los Meses":
        df_filtrado_periodo = df_master.copy()
        label_corte = "(HISTÓRICO CONSOLIDADO)"
    else:
        df_filtrado_periodo = df_master[df_master['Mes'] == periodo_seleccionado]
        label_corte = f"(MES DE {periodo_seleccionado.upper()})"

tienda = st.sidebar.selectbox("Sucursal / Almacén Ropa", ["Todas las Tiendas"] + list(df_master['Tienda'].unique()))

df_filtered = df_filtrado_periodo.copy()
if tienda != "Todas las Tiendas":
    df_filtered = df_filtered[df_filtered['Tienda'] == tienda]
