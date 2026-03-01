import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="ATLAS | Estrategia", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("ATLAS: Resumen Ejecutivo y Estrategia VMO")

# 1. Recuperar datos consolidados
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')
df_cx = st.session_state.get('data_cx')

if df_acd is not None:
    # --- FILTROS EJECUTIVOS EN SIDEBAR ---
    with st.sidebar:
        st.header("Filtros de Estrategia")
        
        # Filtro de PCRC (Multiselect)
        opciones_pcrc = list(df_acd['pcrc'].unique())
        pcrc_sel = st.multiselect("Seleccione PCRC(s):", opciones_pcrc, default=opciones_pcrc)
        
        # Filtro de Sitio (Multiselect)
        opciones_site = list(df_acd['site'].unique())
        site_sel = st.multiselect("Seleccione Sitio(s):", opciones_site, default=opciones_site)

    # Aplicacion de filtros cruzados
    df_f = df_acd[(df_acd['pcrc'].isin(pcrc_sel)) & (df_acd['site'].isin(site_sel))].copy()
    
    # Filtrar QA y CX basados en la seleccion de ACD
    ids_filtrados = df_f['id_llamada']
    df_qa_f = df_qa[df_qa['id_llamada'].isin(ids_filtrados)] if df_qa is not None else pd.DataFrame()
    df_cx_f = df_cx[df_cx['id_llamada'].isin(ids_filtrados)] if df_cx is not None else pd.DataFrame()

    # --- VISTA 1: METRICAS CLAVE (KPIs) ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    
    volumen = len(df_f)
    tmo_avg = df_f['tmo_segundos'].mean() if volumen > 0 else 0
    nota_qa = df_qa_f['nota_final'].mean() if not df_qa_f.empty else 0
    csat_avg = df_cx_f['csat'].mean() if not df_cx_f.empty else 0

    c1.metric("Volumen Total", f"{volumen:,}")
    c2.metric("TMO Promedio", f"{int(tmo_avg)}s")
    c3.metric("Calidad (QA)", f"{nota_qa:.1f}%")
    c4.metric("Satisfaccion (CSAT)", f"{csat_avg:.2f}/5")

    # --- VISTA 2: ANALISIS COMPARATIVO ---
    st.write("### Desempeño por Atributo")
    col_a, col_b = st.columns(2)

    with col_a:
        # Comparativa de Volumen por Sitio
        fig_site = px.bar(df_f.groupby('site').size().reset_index(name='Llamadas'), 
                          x='site', y='Llamadas', title="Distribucion de Carga por Sitio",
                          color='site', color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_site, use_container_width=True)

    with col_b:
        # Relacion Calidad vs TMO por PCRC
        if not df_qa_f.empty:
            df_merged = df_f.merge(df_qa_f, on='id_llamada')
            df_scatter = df_merged.groupby('pcrc').agg({'tmo_segundos':'mean', 'nota_final':'mean'}).reset_index()
            fig_scat = px.scatter(df_scatter, x='tmo_segundos', y='nota_final', text='pcrc', 
                                  size='tmo_segundos', color='pcrc',
                                  title="Matriz Eficiencia (TMO) vs Calidad (QA)")
            st.plotly_chart(fig_scat, use_container_width=True)

    # --- VISTA 3: TENDENCIA TEMPORAL ---
    st.write("### Evolucion del CSAT por PCRC")
    if not df_cx_f.empty:
        df_cx_trend = df_f.merge(df_cx_f, on='id_llamada')
        df_cx_trend['fecha_d'] = df_cx_trend['fecha'].dt.date
        trend_data = df_cx_trend.groupby(['fecha_d', 'pcrc'])['csat'].mean().reset_index()
        fig_trend = px.line(trend_data, x='fecha_d', y='csat', color='pcrc', markers=True,
                            title="Tendencia de Satisfaccion Diaria")
        st.plotly_chart(fig_trend, use_container_width=True)

    # --- VISTA 4: INSIGHTS ESTRATEGICOS ---
    st.divider()
    st.subheader("Sugerencias del Agente ATLAS")
    
    if nota_qa < 85:
        st.error(f"Alerta: La calidad general ({nota_qa:.1f}%) esta por debajo del target del 85%. Se recomienda revisar planes de coaching en los sitios seleccionados.")
    if tmo_avg > 500:
        st.warning(f"Atencion: El TMO actual de {int(tmo_avg)}s impacta la disponibilidad. Revisar procesos de soporte tecnico.")
    else:
        st.success("La operacion se mantiene dentro de los parametros de eficiencia esperados.")

else:
    st.error("Por favor, poblar el sistema en CORTEX para generar el analisis estrategico.")
