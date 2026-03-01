import streamlit as st
import pandas as pd

st.set_page_config(page_title="NEXUS | Capacidad", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("⚙️ NEXUS: Dimensionamiento y Capacidad")

# Recuperar datos de CORTEX
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # Asegurar formato de fecha
    df_acd['fecha'] = pd.to_datetime(df_acd['fecha'])
    
    # --- FILTROS LATERALES ---
    st.sidebar.header("Filtros de Análisis")
    
    # Filtro por PCRC
    lista_pcrc = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_seleccionado = st.sidebar.selectbox("Selecciona PCRC", lista_pcrc)
    
    # Aplicar Filtro
    if pcrc_seleccionado != "Todos":
        df_filtrado = df_acd[df_acd['pcrc'] == pcrc_seleccionado].copy()
    else:
        df_filtrado = df_acd.copy()

    # 1. KPIs de Capacidad Segmentados
    total_lls = len(df_filtrado)
    tmo_avg = df_filtrado['tmo_segundos'].mean()
    abandono_pct = (df_filtrado['abandono'].sum() / total_lls) * 100 if total_lls > 0 else 0
    
    st.subheader(f"Análisis para: {pcrc_seleccionado}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Volumen", f"{total_lls} lls")
    c2.metric("TMO Promedio", f"{int(tmo_avg)} seg")
    c3.metric("Abandono", f"{abandono_pct:.1f}%")

    st.divider()

    # 2. Distribución de Carga Horaria
    
    st.subheader("Curva de Arribo por Hora")
    df_filtrado['hora'] = df_filtrado['fecha'].dt.hour
    chart_data = df_filtrado.groupby('hora').size()
    st.area_chart(chart_data)

    # 3. Cálculo de Staffing (Carga de Trabajo)
    st.subheader("Carga de Trabajo (Workload)")
    workload_hrs = (total_lls * tmo_avg) / 3600
    
    st.info(f"Para el PCRC **{pcrc_seleccionado}**, se requiere cubrir un total de **{workload_hrs:.1f} horas** netas de atención.")
    
    # Tabla resumen por Site dentro del PCRC seleccionado
    st.write("Distribución por Site:")
    resumen_site = df_filtrado.groupby('site').agg({
        'id_llamada': 'count',
        'tmo_segundos': 'mean'
    }).rename(columns={'id_llamada': 'Llamadas', 'tmo_segundos': 'TMO Avg'})
    st.dataframe(resumen_site, use_container_width=True)

else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX y genera el ecosistema de 2 meses.")
    if st.button("Ir a CORTEX"):
        st.switch_page("pages/1_CORTEX.py")
