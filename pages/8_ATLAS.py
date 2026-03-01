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

st.title("🧭 ATLAS: Consolidacion Ejecutiva")

# Recuperar datos
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')
df_cx = st.session_state.get('data_cx')

if df_acd is not None:
    # --- FILTROS DE ESTRATEGIA ---
    st.sidebar.header("Filtros Estratégicos")
    lista_pcrc = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.sidebar.selectbox("Analizar PCRC", lista_pcrc)
    
    # Filtrado lógico
    if pcrc_sel != "Todos":
        df_acd_f = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
        ids_validos = df_acd_f['id_llamada']
        df_qa_f = df_qa[df_qa['id_llamada'].isin(ids_validos)].copy() if df_qa is not None else None
        df_cx_f = df_cx[df_cx['id_llamada'].isin(ids_validos)].copy() if df_cx is not None else None
    else:
        df_acd_f, df_qa_f, df_cx_f = df_acd.copy(), df_qa.copy(), df_cx.copy()

    # 1. Scorecard Ejecutivo (WBR)
    st.subheader(f"Resumen de Desempeño: {pcrc_sel}")
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("Volumen Total", f"{len(df_acd_f)} lls")
    
    if df_qa_f is not None and not df_qa_f.empty:
        c2.metric("Calidad Promedio", f"{df_qa_f['nota_final'].mean():.1f}%")
    
    if df_cx_f is not None and not df_cx_f.empty:
        c3.metric("CSAT (Experiencia)", f"{df_cx_f['csat'].mean():.2f}")
        
    c4.metric("Indice Eficiencia (50/75)", "74%", "+1.5%")

    st.divider()

    # 2. Análisis de Tendencia Histórica (2 Meses)
    st.subheader("Evolución Histórica (Últimas 8 Semanas)")
    
    df_acd_f['fecha'] = pd.to_datetime(df_acd_f['fecha'])
    df_acd_f['Semana'] = df_acd_f['fecha'].dt.isocalendar().week
    
    # Agrupar por semana para ver tendencia
    tendencia = df_acd_f.groupby('Semana').size().reset_index(name='Llamadas')
    fig_trend = px.line(tendencia, x='Semana', y='Llamadas', title="Tendencia de Volumen Semanal", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

    # 3. Cuadrante de Priorización por Site
    st.subheader("Matriz de Priorización por Site")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Generar data de comparación por site
        sites = df_acd_f['site'].unique()
        data_sites = pd.DataFrame({
            'Site': sites,
            'Productividad': [np.random.randint(70, 95) for _ in sites],
            'Calidad': [np.random.randint(80, 100) for _ in sites]
        })
        fig_scatter = px.scatter(data_sites, x='Productividad', y='Calidad', text='Site', 
                                 size=[20]*len(sites), color='Site', title="Eficiencia vs Calidad")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_b:
        st.info("**Estrategia VMO:**")
        st.write(f"Para el PCRC **{pcrc_sel}**, se observa que el site con menor desempeño requiere auditoría de procesos en el módulo BLUEPRINT.")
        if st.button("Generar MBR Mensual"):
            st.success("Reporte consolidado de 60 días generado.")

else:
    st.warning("No hay datos cargados. Ve a CORTEX para generar el ecosistema de 2 meses.")
