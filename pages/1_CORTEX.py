import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("🧠 CORTEX: Ingesta y Validación")

# --- SECCION 1: DOCUMENTACION ---
st.subheader("Fuentes y PCRCs Soportados")
st.info("Este módulo procesa datos de: **Ventas, Atención, Soporte y Retenciones**.")

st.divider()

# --- SECCION 2: GENERADOR MASIVO (2 MESES) ---
st.subheader("Generador de Entorno de Pruebas (60 días)")

# Definición de PCRCs disponibles
pcrcs = ["Ventas", "Atencion", "Soporte", "Retenciones"]

if st.button("🚀 Generar Ecosistema de Datos Completo (2 Meses)"):
    st.session_state.usando_datos_ejemplo = True
    
    # Configuración: 60 días atrás
    dias_totales = 60
    fecha_inicio = datetime.now() - timedelta(days=dias_totales)
    total_registros = 2000 # Volumen representativo para 2 meses
    
    # 1. Generar ACD (Telefonía) con diferentes PCRCs
    df_acd = pd.DataFrame({
        'fecha': [(fecha_inicio + timedelta(minutes=i*45)).strftime('%Y-%m-%d %H:%M') for i in range(total_registros)],
        'id_llamada': [f"C-{5000+i}" for i in range(total_registros)],
        'pcrc': np.random.choice(pcrcs, total_registros),
        'site': np.random.choice(['Lima', 'Cordoba', 'Remoto'], total_registros),
        'tmo_segundos': np.random.randint(180, 650, total_registros),
        'hold_segundos': np.random.randint(5, 80, total_registros),
        'abandono': np.random.choice([0, 1], total_registros, p=[0.92, 0.08])
    })
    
    # 2. Generar QA (Calidad) - Muestra del 10% del ACD
    total_qa = int(total_registros * 0.1)
    ids_para_qa = np.random.choice(df_acd['id_llamada'], total_qa, replace=False)
    df_qa = pd.DataFrame({
        'id_llamada': ids_para_qa,
        'evaluador': np.random.choice(['Monitor_A', 'Monitor_B', 'Monitor_C'], total_qa),
        'nota_final': np.random.randint(75, 100, total_qa),
        'error_critico': np.random.choice(['No', 'Si'], total_qa, p=[0.94, 0.06])
    })
    
    # 3. Generar CX (Experiencia) - Muestra del 15% del ACD
    total_cx = int(total_registros * 0.15)
    ids_para_cx = np.random.choice(df_acd['id_llamada'], total_cx, replace=False)
    df_cx = pd.DataFrame({
        'id_llamada': ids_para_cx,
        'csat': np.random.randint(1, 6, total_cx),
        'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'], total_cx, p=[0.6, 0.2, 0.2])
    })

    # Guardar en Session State para que todos los módulos lo vean
    st.session_state['data_acd'] = df_acd
    st.session_state['data_qa'] = df_qa
    st.session_state['data_cx'] = df_cx
    
    st.success(f"Datos generados exitosamente: {total_registros} llamadas procesadas para {len(pcrcs)} PCRCs.")

st.divider()

# --- SECCION 3: VISTA PREVIA ---
if 'data_acd' in st.session_state:
    st.subheader("Datos Cargados en el Sistema")
    tab1, tab2, tab3 = st.tabs(["ACD (Telefonia)", "QA (Calidad)", "CX (Experiencia)"])
    
    with tab1:
        st.dataframe(st.session_state['data_acd'], use_container_width=True)
    with tab2:
        st.dataframe(st.session_state['data_qa'], use_container_width=True)
    with tab3:
        st.dataframe(st.session_state['data_cx'], use_container_width=True)
else:
    st.info("El sistema está vacío. Usa el botón superior para cargar el ecosistema de pruebas.")
