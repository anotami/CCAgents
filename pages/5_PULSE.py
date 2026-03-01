import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PULSE | Experiencia", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("💓 PULSE: Medicion CX")

# Recuperar datos de CX desde CORTEX
df_cx = st.session_state.get('data_cx')

if df_cx is not None:
    # 1. Metricas Principales de Experiencia
    csat_medio = df_cx['csat'].mean()
    n_encuestas = len(df_cx)
    sentimiento_predominante = df_cx['sentimiento'].mode()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("CSAT Promedio", f"{csat_medio:.2f} / 5.0")
    col2.metric("Total Encuestas", n_encuestas)
    col3.metric("Sentimiento Principal", sentimiento_predominante)

    st.divider()

    # 2. Analisis Visual de Sentimiento y Satisfaccion
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Distribucion de Sentimiento")
        sentiment_counts = df_cx['sentimiento'].value_counts()
        st.bar_chart(sentiment_counts)

    with col_chart2:
        st.subheader("Distribucion de Notas CSAT")
        csat_dist = df_cx['csat'].value_counts().sort_index()
        st.line_chart(csat_dist)

    # 3. Interdependencia: PULSE -> BLUEPRINT
    st.subheader("Insights de Experiencia")
    top_negativos = df_cx[df_cx['sentimiento'] == 'Negativo']
    
    if not top_negativos.empty:
        st.warning(f"Se detectaron {len(top_negativos)} interacciones con sentimiento Negativo. Se recomienda revision de Journey en el modulo de PROCESOS.")
    else:
        st.success("La experiencia general se mantiene en niveles positivos.")

else:
    st.warning("No hay datos de CX disponibles. Ve a CORTEX para generar o cargar una muestra de Experiencia.")
    if st.button("Ir a CORTEX"):
        st.switch_page("pages/1_CORTEX.py")
