import streamlit as st
import pandas as pd

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Mantener consistencia del banner
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("CORTEX: Ingesta y Validacion")

archivo = st.file_uploader("Sube el reporte del ACD (.csv)", type=['csv'])

if archivo:
    df = pd.read_csv(archivo)
    st.success("Archivo cargado correctamente")
    st.dataframe(df.head(5))
