import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SENTINEL | Calidad", layout="wide")

# Banner de estado
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("SENTINEL: Auditoria de Calidad")

df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')

if df_acd is not None and df_qa is not None:
    # FILTRO MAESTRO DE PCRC
    pcrcs = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.selectbox("Seleccione PCRC para analizar Calidad:", pcrcs)

    if pcrc_sel != "Todos":
        ids_pcrc = df_acd[df_acd['pcrc'] == pcrc_sel]['id_llamada']
        df_qa_f = df_qa[df_qa['id_llamada'].isin(ids_pcrc)].copy()
    else:
        df_qa_f = df_qa.copy()

    st.divider()
    
    # METRICAS DEL PCRC SELECCIONADO
    c1, c2, c3 = st.columns(3)
    nota_avg = df_qa_f['nota_final'].mean()
    c1.metric(f"Nota Avg {pcrc_sel}", f"{nota_avg:.1f}%")
    c2.metric("Muestra Auditada", len(df_qa_f))
    c3.metric("Errores Criticos", len(df_qa_f[df_qa_f['error_critico'] == 'Si']))

    st.subheader("Detalle de Evaluaciones")
    st.dataframe(df_qa_f, width='stretch')
else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX.")
