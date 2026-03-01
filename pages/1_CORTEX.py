import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("CORTEX: Generador de Ecosistema con Emocion Segmentada")

# Definición de perfiles con Pesos de Volumen y Probabilidades de Sentimiento
# sent_prob: [Positivo, Neutral, Negativo]
perfiles = {
    "Atencion": {
        "p_vol": 0.55, "tmo": 280, "tmo_std": 40, "qa": 92, 
        "csat": [0.05, 0.05, 0.1, 0.4, 0.4], "curva": "plana",
        "sent_prob": [0.60, 0.30, 0.10] # Mas bueno
    },
    "Ventas": {
        "p_vol": 0.20, "tmo": 420, "tmo_std": 90, "qa": 84, 
        "csat": [0.1, 0.2, 0.3, 0.3, 0.1], "curva": "comercial",
        "sent_prob": [0.70, 0.20, 0.10] # Mas bueno
    },
    "Soporte": {
        "p_vol": 0.15, "tmo": 750, "tmo_std": 180, "qa": 76, 
        "csat": [0.3, 0.3, 0.2, 0.1, 0.1], "curva": "tarde",
        "sent_prob": [0.10, 0.30, 0.60] # Mas malo
    },
    "Retenciones": {
        "p_vol": 0.10, "tmo": 520, "tmo_std": 110, "qa": 89, 
        "csat": [0.1, 0.1, 0.2, 0.3, 0.3], "curva": "comercial",
        "sent_prob": [0.10, 0.20, 0.70] # Mas malo
    }
}

if st.button("Generar Ecosistema de 180 Dias"):
    st.session_state.usando_datos_ejemplo = True
    dias = 180 
    total_registros = 15000 
    fecha_ini = datetime.now() - timedelta(days=dias)
    
    data_acd = []
    p_nombres = list(perfiles.keys())
    p_pesos = [perfiles[p]["p_vol"] for p in p_nombres]
    
    for i in range(total_registros):
        pcrc_act = np.random.choice(p_nombres, p=p_pesos)
        perf = perfiles[pcrc_act]
        
        # Curva de arribo
        if perf["curva"] == "comercial":
            dist = np.array([0.01]*8 + [0.1, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.02] + [0.01]*6)
        elif perf["curva"] == "tarde":
            dist = np.array([0.01]*12 + [0.05, 0.05, 0.1, 0.15, 0.2, 0.2, 0.1, 0.05, 0.05, 0.02, 0.01, 0.01])
        else:
            dist = np.ones(24)
        
        h = np.random.choice(range(24), p=dist/dist.sum())
        f = (fecha_ini + timedelta(days=np.random.randint(0, dias))).replace(hour=h, minute=np.random.randint(0,60))
        
        # TMO Gamma
        shape = (perf["tmo"] / perf["tmo_std"])**2
        scale = perf["tmo_std"]**2 / perf["tmo"]
        
        data_acd.append({
            'fecha': f, 'id_llamada': f"TEL-{400000+i}", 'pcrc': pcrc_act,
            'site': np.random.choice(["Lima", "Cordoba", "Remoto"]),
            'tmo_segundos': int(np.random.gamma(shape, scale)),
            'abandono': np.random.choice([0, 1], p=[0.93, 0.07])
        })

    df_acd = pd.DataFrame(data_acd).sort_values('fecha')
    
    # QA
    indices_qa = np.random.choice(df_acd.index, int(len(df_acd)*0.1), replace=False)
    qa_list = [{'id_llamada': df_acd.loc[idx, 'id_llamada'], 
                'nota_final': max(0, min(100, np.random.normal(perfiles[df_acd.loc[idx, 'pcrc']]["qa"], 6))), 
                'error_critico': np.random.choice(['No', 'Si'], p=[0.96, 0.04])} for idx in indices_qa]
    
    # CX (Sentimiento dependiente del PCRC)
    cx_list = []
    indices_cx = np.random.choice(df_acd.index, int(len(df_acd)*0.15), replace=False)
    for idx in indices_cx:
        row = df_acd.loc[idx]
        perf = perfiles[row['pcrc']]
        cx_list.append({
            'id_llamada': row['id_llamada'], 
            'csat': np.random.choice([1, 2, 3, 4, 5], p=perf["csat"]), 
            'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'], p=perf["sent_prob"])
        })

    st.session_state['data_acd'], st.session_state['data_qa'], st.session_state['data_cx'] = df_acd, pd.DataFrame(qa_list), pd.DataFrame(cx_list)
    st.success(f"Historial de 6 meses generado con sentimientos diferenciados.")

st.divider()

if 'data_acd' in st.session_state:
    st.subheader("Analisis de Generacion: Los 3 Frentes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Frente Operativo (Volumen)**")
        mix_data = st.session_state['data_acd']['pcrc'].value_counts().reset_index()
        fig_vol = px.pie(mix_data, names='pcrc', values='count', hole=0.5, title="Mix de Negocio")
        st.plotly_chart(fig_vol, use_container_width=True)

    with col2:
        st.write("**Frente Calidad (Distribucion)**")
        df_qa_v = st.session_state['data_qa'].merge(st.session_state['data_acd'][['id_llamada', 'pcrc']], on='id_llamada')
        fig_qa = px.box(df_qa_v, x='pcrc', y='nota_final', color='pcrc', title="Notas por PCRC")
        st.plotly_chart(fig_qa, use_container_width=True)

    with col3:
        st.write("**Frente Experiencia (Sentimiento)**")
        df_cx_v = st.session_state['data_cx'].merge(st.session_state['data_acd'][['id_llamada', 'pcrc']], on='id_llamada')
        # Mostrar el sentimiento por PCRC para validar la logica
        fig_cx = px.histogram(df_cx_v, x='pcrc', color='sentimiento', barmode='group', title="Sentimiento por Negocio")
        st.plotly_chart(fig_cx, use_container_width=True)
