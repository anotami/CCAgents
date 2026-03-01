import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="CORTEX | Ingesta", layout="wide")

# Banner de estado
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("CORTEX: Generador de Ecosistema Multinegocio")

# Perfiles con logica Telco real
perfiles = {
    "Ventas": {"vol": 0.25, "tmo": 450, "tmo_std": 100, "qa": 82, "csat": [0.1, 0.2, 0.3, 0.3, 0.1], "curva": "comercial"},
    "Atencion": {"vol": 0.45, "tmo": 280, "tmo_std": 50, "qa": 92, "csat": [0.05, 0.05, 0.1, 0.4, 0.4], "curva": "plana"},
    "Soporte": {"vol": 0.20, "tmo": 720, "tmo_std": 200, "qa": 78, "csat": [0.3, 0.3, 0.2, 0.1, 0.1], "curva": "tarde"},
    "Retenciones": {"vol": 0.10, "tmo": 500, "tmo_std": 120, "qa": 88, "csat": [0.1, 0.1, 0.2, 0.3, 0.3], "curva": "comercial"}
}

if st.button("Generar Ecosistema Diferenciado (60 Dias)"):
    st.session_state.usando_datos_ejemplo = True
    dias = 60
    total_registros = 6000
    fecha_ini = datetime.now() - timedelta(days=dias)
    
    data_acd = []
    
    for i in range(total_registros):
        pcrc_act = np.random.choice(list(perfiles.keys()), p=[p["vol"] for p in perfiles.values()])
        p = perfiles[pcrc_act]
        
        # Logica de horas (Normalizacion de probabilidad para evitar ValueErrors)
        if p["curva"] == "comercial":
            dist = np.array([0.01]*8 + [0.1, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.02] + [0.01]*6)
        elif p["curva"] == "tarde":
            dist = np.array([0.01]*12 + [0.05, 0.05, 0.1, 0.15, 0.2, 0.2, 0.1, 0.05, 0.05, 0.02, 0.01, 0.01])
        else:
            dist = np.ones(24)
        
        h = np.random.choice(range(24), p=dist/dist.sum())
        f = (fecha_ini + timedelta(days=np.random.randint(0, dias))).replace(hour=h, minute=np.random.randint(0,60))
        
        # TMO Gamma para evitar negativos y dar realismo
        shape = (p["tmo"] / p["tmo_std"])**2
        scale = p["tmo_std"]**2 / p["tmo"]
        
        data_acd.append({
            'fecha': f, 'id_llamada': f"TEL-{200000+i}", 'pcrc': pcrc_act,
            'site': np.random.choice(["Lima", "Cordoba", "Remoto"]),
            'tmo_segundos': int(np.random.gamma(shape, scale)),
            'abandono': np.random.choice([0, 1], p=[0.92, 0.08])
        })

    df_acd = pd.DataFrame(data_acd).sort_values('fecha')
    
    # QA y CX Diferenciados
    qa_list = []
    indices_qa = np.random.choice(df_acd.index, int(len(df_acd)*0.1), replace=False)
    for idx in indices_qa:
        row = df_acd.loc[idx]
        qa_list.append({'id_llamada': row['id_llamada'], 'nota_final': max(0, min(100, np.random.normal(perfiles[row['pcrc']]["qa"], 5))), 'error_critico': 'No'})
    
    cx_list = []
    indices_cx = np.random.choice(df_acd.index, int(len(df_acd)*0.15), replace=False)
    for idx in indices_cx:
        row = df_acd.loc[idx]
        cx_list.append({'id_llamada': row['id_llamada'], 'csat': np.random.choice([1, 2, 3, 4, 5], p=perfiles[row['pcrc']]["csat"]), 'sentimiento': 'Neutral'})

    st.session_state['data_acd'], st.session_state['data_qa'], st.session_state['data_cx'] = df_acd, pd.DataFrame(qa_list), pd.DataFrame(cx_list)
    st.success("Ecosistema Telco Diferenciado generado correctamente.")
