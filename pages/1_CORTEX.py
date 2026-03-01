import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Banner de estado de datos
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("🧠 CORTEX: Ingesta y Validación")

# --- SECCIÓN 1: DOCUMENTACIÓN DE FUENTES ---
with st.expander("Requerimientos de Información por Fuente", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**1. ACD (Telefonía)**")
        st.write("- fecha (YYYY-MM-DD HH:MM)\n- id_llamada\n- site\n- tmo_segundos\n- hold_segundos\n- abandono (0/1)")
    with col_b:
        st.markdown("**2. QA (Calidad)**")
        st.write("- id_llamada\n- evaluador\n- nota_final (0-100)\n- error_critico (Si/No)\n- feedback_coaching (Texto)")
    with col_c:
        st.markdown("**3. CRM/CX (Experiencia)**")
        st.write("- id_llamada\n- csat (1-5)\n- motivo_contacto\n- sentimiento (Pos/Neu/Neg)")

# --- SECCIÓN 2: GENERADOR DE DATOS DE EJEMPLO ---
st.subheader("Generar Casos de Ejemplo")
col_gen1, col_gen2 = st.columns([1, 3])

with col_gen1:
    tipo_fuente = st.selectbox("Selecciona Fuente", ["ACD", "QA", "CX"])
    filas = st.slider("Número de filas", 10, 500, 100)
    
if st.button("Generar y Cargar Datos de Prueba"):
    st.session_state.usando_datos_ejemplo = True
    
    # Lógica de generación en memoria para Streamlit Cloud
    output = io.BytesIO()
    inicio = datetime.now() - timedelta(days=7)
    
    if tipo_fuente == "ACD":
        df_gen = pd.DataFrame({
            'fecha': [(inicio + timedelta(minutes=i*30)).strftime('%Y-%m-%d %H:%M') for i in range(filas)],
            'id_llamada': [f"CALL-{2000+i}" for i in range(filas)],
            'site': np.random.choice(['Lima', 'Cordoba', 'Remoto'], filas),
            'tmo_segundos': np.random.randint(180, 600, filas),
            'hold_segundos': np.random.randint(10, 60, filas),
            'abandono': np.random.choice([0, 1], filas, p=[0.9, 0.1])
        })
    elif tipo_fuente == "QA":
        df_gen = pd.DataFrame({
            'id_llamada': [f"CALL-{2000+i}" for i in range(filas)],
            'evaluador': np.random.choice(['Supervisor A', 'Supervisor B'], filas),
            'nota_final': np.random.randint(70, 100, filas),
            'error_critico': np.random.choice(['No', 'Si'], filas, p=[0.95, 0.05])
        })
    else: # CX
        df_gen = pd.DataFrame({
            'id_llamada': [f"CALL-{2000+i}" for i in range(filas)],
            'csat': np.random.randint(1, 6, filas),
            'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'], filas)
        })

    st.session_state[f'data_{tipo_fuente.lower()}'] = df_gen
    st.success(f"Datos de {tipo_fuente} generados y cargados en memoria.")
    st.dataframe(df_gen.head(5), use_container_width=True)

st.divider()

# --- SECCIÓN 3: CARGA DE ARCHIVOS REALES ---
st.subheader("Carga de Archivos Reales")
archivo_real = st.file_uploader("Sube tu archivo .csv", type=['csv'])

if archivo_real:
    st.session_state.usando_datos_ejemplo = False
    df_real = pd.read_csv(archivo_real)
    st.success("Tus datos han sido cargados. El banner ha cambiado a 'Tus Datos'.")
    st.dataframe(df_real.head(5), use_container_width=True)
    st.rerun()
