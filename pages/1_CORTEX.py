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

st.title("CORTEX: Generacion de Ecosistema Telco")

# Configuracion de la simulacion
pcrcs = ["Ventas", "Atencion", "Soporte", "Retenciones"]
sites = ["Lima", "Cordoba", "Remoto"]

if st.button("Generar Datos Reales (60 Dias)"):
    st.session_state.usando_datos_ejemplo = True
    
    # 1. Definir volumen base con estacionalidad horaria
    dias = 60
    registros_aprox = 5000 
    fecha_fin = datetime.now()
    fecha_ini = fecha_fin - timedelta(days=dias)
    
    # Curva de arribo tipica de Telco (pesada entre 9am y 7pm)
    pesos_hora = [0.01, 0.005, 0.005, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 0.9, 0.8, 0.8, 0.9, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05]
    
    data_list = []
    for i in range(registros_aprox):
        # Seleccion de fecha y hora aleatoria con peso
        random_day = fecha_ini + timedelta(days=np.random.randint(0, dias))
        hora = np.random.choice(range(24), p=np.array(pesos_hora)/sum(pesos_hora))
        fecha_completa = random_day.replace(hour=hora, minute=np.random.randint(0, 60))
        
        # Logica de TMO por PCRC (Distribucion Gamma para realismo)
        # Ventas y Soporte suelen ser mas largos que Atencion
        pcrc_actual = np.random.choice(pcrcs)
        if pcrc_actual == "Atencion":
            tmo = np.random.gamma(shape=10, scale=30) # Promedio ~300s
        elif pcrc_actual == "Soporte":
            tmo = np.random.gamma(shape=15, scale=40) # Promedio ~600s
        else:
            tmo = np.random.gamma(shape=12, scale=35) # Promedio ~420s
            
        data_list.append({
            'fecha': fecha_completa,
            'id_llamada': f"TEL-{100000+i}",
            'pcrc': pcrc_actual,
            'site': np.random.choice(sites),
            'tmo_segundos': int(tmo),
            'hold_segundos': int(np.random.exponential(scale=30)), # Muchos holds cortos, pocos largos
            'abandono': np.random.choice([0, 1], p=[0.93, 0.07])
        })
    
    df_acd = pd.DataFrame(data_list).sort_values('fecha')
    
    # 2. Generar QA (Calidad) con Distribucion Beta (mas realista que uniforme)
    total_qa = int(len(df_acd) * 0.08)
    indices_qa = np.random.choice(df_acd.index, total_qa, replace=False)
    
    # Calidad suele concentrarse entre 80 y 95
    notas_qa = np.random.beta(a=8, b=2, size=total_qa) * 100
    
    df_qa = pd.DataFrame({
        'id_llamada': df_acd.loc[indices_qa, 'id_llamada'],
        'evaluador': np.random.choice(['Auditor_1', 'Auditor_2', 'Auditor_3'], total_qa),
        'nota_final': notas_qa.round(2),
        'error_critico': np.random.choice(['No', 'Si'], total_qa, p=[0.96, 0.04])
    })
    
    # 3. Generar CX (Experiencia) correlacionado con TMO
    # Si el TMO es muy alto, el CSAT tiende a bajar
    total_cx = int(len(df_acd) * 0.12)
    indices_cx = np.random.choice(df_acd.index, total_cx, replace=False)
    df_cx_base = df_acd.loc[indices_cx].copy()
    
    def calcular_csat(tmo):
        if tmo > 600: return np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        return np.random.choice([3, 4, 5], p=[0.2, 0.3, 0.5])

    df_cx = pd.DataFrame({
        'id_llamada': df_cx_base['id_llamada'],
        'csat': df_cx_base['tmo_segundos'].apply(calcular_csat),
        'sentimiento': np.random.choice(['Positivo', 'Neutral', 'Negativo'], total_cx, p=[0.5, 0.3, 0.2])
    })

    # Guardar en Session State
    st.session_state['data_acd'] = df_acd
    st.session_state['data_qa'] = df_qa
    st.session_state['data_cx'] = df_cx
    
    st.success(f"Ecosistema Telco generado: {len(df_acd)} registros con curvas de arribo y TMO variables.")

st.divider()

if 'data_acd' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["ACD (Telefonía)", "QA (Calidad)", "CX (Experiencia)"])
    with tab1:
        st.dataframe(st.session_state['data_acd'].head(10), width='stretch')
    with tab2:
        st.dataframe(st.session_state['data_qa'].head(10), width='stretch')
    with tab3:
        st.dataframe(st.session_state['data_cx'].head(10), width='stretch')
