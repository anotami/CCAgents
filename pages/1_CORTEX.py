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

# Definicion de perfiles por PCRC
perfiles = {
    "Ventas": {
        "peso_volumen": 0.25,
        "tmo_base": 450, "tmo_std": 100, # Largas por negociacion
        "qa_promedio": 82, "qa_std": 8,    # Calidad media por presion comercial
        "csat_prob": [0.1, 0.2, 0.3, 0.3, 0.1], # CSAT variable
        "curva_arribo": "comercial" # Pico al mediodia
    },
    "Atencion": {
        "peso_volumen": 0.45,
        "tmo_base": 280, "tmo_std": 50,  # Cortas y rapidas
        "qa_promedio": 92, "qa_std": 4,    # Muy procedimentado y alta nota
        "csat_prob": [0.05, 0.05, 0.1, 0.4, 0.4], # CSAT alto
        "curva_arribo": "plana"      # Flujo constante todo el dia
    },
    "Soporte": {
        "peso_volumen": 0.20,
        "tmo_base": 720, "tmo_std": 200, # Muy largas por complejidad
        "qa_promedio": 78, "qa_std": 10,   # Notas bajas por dificultad tecnica
        "csat_prob": [0.3, 0.3, 0.2, 0.1, 0.1], # CSAT bajo por frustracion tecnica
        "curva_arribo": "tarde"      # Mas llamadas al final del dia
    },
    "Retenciones": {
        "peso_volumen": 0.10,
        "tmo_base": 500, "tmo_std": 120, # Tiempo para convencer al cliente
        "qa_promedio": 88, "qa_std": 5,    # Calidad alta (agentes senior)
        "csat_prob": [0.1, 0.1, 0.2, 0.3, 0.3], # CSAT bueno si se retiene
        "curva_arribo": "comercial"
    }
}

if st.button("Generar Ecosistema Diferenciado (60 Dias)"):
    st.session_state.usando_datos_ejemplo = True
    dias = 60
    total_registros = 6000
    fecha_fin = datetime.now()
    fecha_ini = fecha_fin - timedelta(days=dias)
    
    data_acd = []
    
    for i in range(total_registros):
        # 1. Seleccionar PCRC segun su peso en el negocio
        p_nombres = list(perfiles.keys())
        p_pesos = [perfiles[p]["peso_volumen"] for p in p_nombres]
        pcrc_act = np.random.choice(p_nombres, p=p_pesos)
        perf = perfiles[pcrc_act]
        
        # 2. Fecha con curva de arribo especifica
        random_day = fecha_ini + timedelta(days=np.random.randint(0, dias))
        if perf["curva_arribo"] == "comercial":
            h = np.random.choice(range(24), p=[0.01]*8 + [0.1, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.02]*1 + [0.01]*6)
        elif perf["curva_arribo"] == "tarde":
            h = np.random.choice(range(24), p=[0.01]*12 + [0.05, 0.05, 0.1, 0.15, 0.2, 0.2, 0.1, 0.05, 0.05, 0.02, 0.01, 0.01])
        else: # plana
            h = np.random.randint(8, 20)
            
        fecha_full = random_day.replace(hour=h, minute=np.random.randint(0, 60))
        
        # 3. TMO diferenciado (Distribucion Gamma para evitar negativos)
        shape = (perf["tmo_base"] / perf["tmo_std"])**2
        scale = perf["tmo_std"]**2 / perf["tmo_base"]
        tmo = np.random.gamma(shape, scale)
        
        data_acd.append({
            'fecha': fecha_full,
            'id_llamada': f"LL-{200000+i}",
            'pcrc': pcrc_act,
            'site': np.random.choice(["Lima", "Cordoba", "Remoto"]),
            'tmo_segundos': int(tmo),
            'abandono': np.random.choice([0, 1], p=[0.92, 0.08])
        })

    df_acd = pd.DataFrame(data_acd).sort_values('fecha')
    
    # 4. Generar QA diferenciado por PCRC
    qa_list = []
    indices_qa = np.random.choice(df_acd.index, int(len(df_acd)*0.1), replace=False)
    for idx in indices_qa:
        row = df_acd.loc[idx]
        perf = perfiles[row['pcrc']]
        nota = np.random.normal(perf["qa_promedio"], perf["qa_std"])
        qa_list.append({
            'id_llamada': row['id_llamada'],
            'nota_final': max(0, min(100, nota)),
            'error_critico': np.random.choice(['No', 'Si'], p=[0.95, 0.05])
        })
    df_qa = pd.DataFrame(qa_list)

    # 5. Generar CX diferenciado por PCRC
    cx_list = []
    indices_cx = np.random.choice(df_acd.index, int(len(df_acd)*0.15), replace=False)
    for idx in indices_cx:
        row = df_acd.loc[idx]
        perf = perfiles[row['pcrc']]
        cx_list.append({
            'id_llamada': row['id_llamada'],
            'csat': np.random.choice([1, 2, 3, 4, 5], p=perf["csat_prob"]),
            'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'])
        })
    df_cx = pd.DataFrame(cx_list)

    st.session_state['data_acd'] = df_acd
    st.session_state['data_qa'] = df_qa
    st.session_state['data_cx'] = df_cx
    st.success("Ecosistema diferenciado generado exitosamente.")

st.divider()
if 'data_acd' in st.session_state:
    st.write("Vista previa de datos por PCRC:")
    st.dataframe(st.session_state['data_acd'].groupby('pcrc').agg({'tmo_segundos': 'mean', 'id_llamada': 'count'}), width='stretch')
