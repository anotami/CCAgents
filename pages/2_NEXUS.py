import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="NEXUS | Capacidad", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("NEXUS: Dimensionamiento y Capacidad")

# Recuperar datos de CORTEX
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # 1. Preparacion de base temporal
    df_acd['fecha'] = pd.to_datetime(df_acd['fecha'])
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = {'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mie', 'Thursday': 'Jue', 'Friday': 'Vie', 'Saturday': 'Sab', 'Sunday': 'Dom'}
    
    # --- SELECCION DE PCRC (FILTRO MAESTRO) ---
    lista_pcrc = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.selectbox("Seleccione el PCRC a analizar:", lista_pcrc)
    
    # Aplicacion del filtro maestro a todo el modulo
    if pcrc_sel != "Todos":
        df = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    else:
        df = df_acd.copy()

    st.divider()

    # --- FILA 1: VOLUMEN MENSUAL Y SEMANAL ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Volumen Mensual: {pcrc_sel}")
        df_mensual = df.resample('M', on='fecha').size().reset_index(name='Llamadas')
        df_mensual['Mes'] = df_mensual['fecha'].dt.strftime('%b %Y')
        fig_mes = px.bar(df_mensual, x='Mes', y='Llamadas', color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_mes, use_container_width=True)

    with col2:
        st.subheader(f"Volumen Semanal: {pcrc_sel}")
        df_semanal = df.resample('W', on='fecha').size().reset_index(name='Llamadas')
        df_semanal['Semana'] = df_semanal['fecha'].dt.strftime('Sem %U')
        fig_sem = px.line(df_semanal, x='Semana', y='Llamadas', markers=True)
        st.plotly_chart(fig_sem, use_container_width=True)

    # --- FILA 2: VOLUMEN POR DIA Y TMO POR DIA ---
    col3, col4 = st.columns(2)
    with col3:
        st.subheader(f"Volumen por Dia de Semana: {pcrc_sel}")
        df['Dia_Nombre'] = df['fecha'].dt.day_name()
        df_vol_dia = df.groupby('Dia_Nombre').size().reindex(dias_orden).reset_index(name='Llamadas')
        df_vol_dia['Dia'] = df_vol_dia['Dia_Nombre'].map(dias_es)
        fig_vol_dia = px.bar(df_vol_dia, x='Dia', y='Llamadas', color='Llamadas', color_continuous_scale='Blues')
        st.plotly_chart(fig_vol_dia, use_container_width=True)

    with col4:
        st.subheader(f"TMO Promedio por Dia: {pcrc_sel}")
        df_tmo_dia = df.groupby('Dia_Nombre')['tmo_segundos'].mean().reindex(dias_orden).reset_index(name='TMO')
        df_tmo_dia['Dia'] = df_tmo_dia['Dia_Nombre'].map(dias_es)
        fig_tmo_dia = px.line(df_tmo_dia, x='Dia', y='TMO', markers=True, color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_tmo_dia, use_container_width=True)

    # --- FILA 3: CURVA DE ARRIBO E INFO ---
    st.subheader(f"Curva de Arribo por Intervalo: {pcrc_sel}")
    df['Hora'] = df['fecha'].dt.hour
    df_intervalo = df.groupby('Hora').size().reset_index(name='Llamadas')
    fig_int = px.bar(df_intervalo, x='Hora', y='Llamadas', color='Llamadas', color_continuous_scale='Viridis')
    st.plotly_chart(fig_int, use_container_width=True)

    # --- RESUMEN FINAL ---
    st.divider()
    tmo_avg = df['tmo_segundos'].mean()
    workload_hrs = (len(df) * tmo_avg) / 3600
    st.info(f"Analisis de Capacidad ({pcrc_sel}): Carga total de {workload_hrs:.1f} horas netas. TMO promedio de {int(tmo_avg)} segundos.")

else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX y genera el ecosistema de 2 meses.")
