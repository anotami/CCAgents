import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("CORTEX: Ingesta y Validacion")

# --- SECCION 1: DOCUMENTACION DE FUENTES ---
st.subheader("Fuentes de Informacion Requeridas")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.info("**1. ACD (Telefonia)**\n\nCampos: fecha, id_llamada, site, tmo_segundos, hold_segundos, abandono (0/1)")
with col_info2:
    st.info("**2. QA (Calidad)**\n\nCampos: id_llamada, evaluador, nota_final (0-100), error_critico (Si/No)")
with col_info3:
    st.info("**3. CX (Experiencia)**\n\nCampos: id_llamada, csat (1-5), sentimiento (Positivo/Negativo)")

st.divider()

# --- SECCION 2: GENERADOR E INGESTA ---
col_gen, col_up = st.columns(2)

with col_gen:
    st.subheader("Generar Casos de Ejemplo")
    fuente_gen = st.selectbox("Selecciona fuente a simular", ["ACD", "QA", "CX"])
    if st.button("Generar y Cargar Ejemplo"):
        st.session_state.usando_datos_ejemplo = True
        filas = 100
        inicio = datetime.now()
        
        if fuente_gen == "ACD":
            df = pd.DataFrame({
                'fecha': [(inicio - timedelta(minutes=i*30)).strftime('%Y-%m-%d %H:%M') for i in range(filas)],
                'id_llamada': [f"C-{1000+i}" for i in range(filas)],
                'site': np.random.choice(['Lima', 'Cordoba'], filas),
                'tmo_segundos': np.random.randint(200, 500, filas),
                'hold_segundos': np.random.randint(10, 50, filas),
                'abandono': np.random.choice([0, 1], filas, p=[0.9, 0.1])
            })
        elif fuente_gen == "QA":
            df = pd.DataFrame({
                'id_llamada': [f"C-{1000+i}" for i in range(filas)],
                'evaluador': np.random.choice(['Sup_1', 'Sup_2'], filas),
                'nota_final': np.random.randint(80, 100, filas),
                'error_critico': np.random.choice(['No', 'Si'], filas, p=[0.9, 0.1])
            })
        else:
            df = pd.DataFrame({
                'id_llamada': [f"C-{1000+i}" for i in range(filas)],
                'csat': np.random.randint(1, 6, filas),
                'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'], filas)
            })
        
        st.session_state[f'data_{fuente_gen.lower()}'] = df
        st.success(f"Datos de {fuente_gen} cargados en memoria")

with col_up:
    st.subheader("Cargar Datos Reales")
    archivo = st.file_uploader("Sube tu archivo .csv", type=['csv'])
    if archivo:
        st.session_state.usando_datos_ejemplo = False
        # Aqui podriamos agregar logica para detectar que fuente es segun columnas
        df_real = pd.read_csv(archivo)
        st.session_state['data_real'] = df_real
        st.success("Datos reales cargados")
        st.rerun()

# --- SECCION 3: VISUALIZACION DE DATOS CARGADOS ---
st.divider()
st.subheader("Vista Previa de Datos en Sistema")
fuentes_disponibles = [k for k in st.session_state.keys() if k.startswith('data_')]

if fuentes_disponibles:
    for f in fuentes_disponibles:
        st.write(f"Dataset: **{f.replace('data_', '').upper()}**")
        st.dataframe(st.session_state[f].head(5), use_container_width=True)
else:
    st.warning("No hay datos cargados todavia. Usa el generador o sube un archivo.")
