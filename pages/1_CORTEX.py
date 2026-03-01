import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="NEXUS | Capacidad", layout="wide")

# Banner de estado
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("NEXUS: Dimensionamiento y Capacidad")

# Recuperar datos de CORTEX
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # Preparacion de datos
    df_acd['fecha'] = pd.to_datetime(df_acd['fecha'])
    
    # --- SELECCION DE PCRC (ARRIBA) ---
    pcrcs = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.selectbox("Seleccione el PCRC a analizar:", pcrcs)
    
    if pcrc_sel != "Todos":
        df = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    else:
        df = df_acd.copy()

    st.divider()

    # --- FILAS DE GRAFICAS ---
    # Fila 1: Mensual y Semanal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vista Mensual")
        df_mensual = df.resample('M', on='fecha').size().reset_index(name='Llamadas')
        df_mensual['Mes'] = df_mensual['fecha'].dt.strftime('%b %Y')
        fig_mes = px.bar(df_mensual, x='Mes', y='Llamadas', color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_mes, use_container_width=True)

    with col2:
        st.subheader("Vista Semanal")
        df_semanal = df.resample('W', on='fecha').size().reset_index(name='Llamadas')
        df_semanal['Semana'] = df_semanal['fecha'].dt.strftime('Sem %U')
        fig_sem = px.line(df_semanal, x='Semana', y='Llamadas', markers=True)
        st.plotly_chart(fig_sem, use_container_width=True)

    # Fila 2: Diaria e Intervalo
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Vista Diaria (Ultimos 30 dias)")
        df_diario = df.resample('D', on='fecha').size().reset_index(name='Llamadas')
        fig_dia = px.area(df_diario.tail(30), x='fecha', y='Llamadas')
        st.plotly_chart(fig_dia, use_container_width=True)

    with col4:
        st.subheader("Distribucion por Intervalo (Hora)")
        # Agrupamos por hora del dia para ver el comportamiento promedio del intervalo
        df['Hora'] = df['fecha'].dt.hour
        df_intervalo = df.groupby('Hora').size().reset_index(name='Llamadas')
        fig_int = px.bar(df_intervalo, x='Hora', y='Llamadas', color='Llamadas', color_continuous_scale='Viridis')
        st.plotly_chart(fig_int, use_container_width=True)

    # --- ANALISIS DE CARGA ---
    st.divider()
    tmo_avg = df['tmo_segundos'].mean()
    workload_total = (len(df) * tmo_avg) / 3600
    
    st.info(f"Analisis Final: Para el PCRC {pcrc_sel}, el volumen procesado representa {workload_total:.1f} horas de conexion neta con un TMO promedio de {int(tmo_avg)} segundos.")

else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX y genera el entorno de 2 meses.")
