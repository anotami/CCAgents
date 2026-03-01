import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PULSE | Experiencia", layout="wide")

# Banner de estado
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)

st.title("PULSE: Voz del Cliente")

df_acd = st.session_state.get('data_acd')
df_cx = st.session_state.get('data_cx')

if df_acd is not None and df_cx is not None:
    pcrc_sel = st.selectbox("Seleccione PCRC para Experiencia:", ["Todos"] + list(df_acd['pcrc'].unique()))

    if pcrc_sel != "Todos":
        ids_pcrc = df_acd[df_acd['pcrc'] == pcrc_sel]['id_llamada']
        df_cx_f = df_cx[df_cx['id_llamada'].isin(ids_pcrc)].copy()
    else:
        df_cx_f = df_cx.copy()

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_csat = px.histogram(df_cx_f, x="csat", title=f"Distribucion CSAT: {pcrc_sel}", color_discrete_sequence=['#2ca02c'])
        st.plotly_chart(fig_csat, use_container_width=True)
    
    with col_b:
        fig_sent = px.pie(df_cx_f, names="sentimiento", title=f"Sentimiento: {pcrc_sel}")
        st.plotly_chart(fig_sent, use_container_width=True)
else:
    st.warning("No hay datos de experiencia. Generalos en CORTEX.")
