import streamlit as st
import pandas as pd

st.set_page_config(page_title="NEXUS | Capacidad", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("⚙️ NEXUS: Dimensionamiento y Capacidad")

# Recuperar datos de CORTEX (ACD)
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # Convertir fecha a datetime para análisis temporal
    df_acd['fecha'] = pd.to_datetime(df_acd['fecha'])
    
    # 1. KPIs de Capacidad
    total_llamadas = len(df_acd)
    tmo_promedio = df_acd['tmo_segundos'].mean()
    tasa_abandono = (df_acd['abandono'].sum() / total_llamadas) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Volumen Total", f"{total_llamadas} lls")
    col2.metric("TMO Promedio", f"{int(tmo_promedio)} seg")
    col3.metric("Tasa Abandono", f"{tasa_abandono:.1f}%")

    st.divider()

    # 2. Distribución de Carga (Workload)
    st.subheader("Distribución de Carga por Hora")
    df_acd['hora'] = df_acd['fecha'].dt.hour
    chart_data = df_acd.groupby('hora').size()
    st.bar_chart(chart_data)

    # 3. Calculadora de Staffing Teórico (Carga de Trabajo)
    st.subheader("Análisis de Staffing")
    # Carga de trabajo en horas = (Llamadas * TMO) / 3600
    workload_hours = (total_llamadas * tmo_promedio) / 3600
    
    st.write(f"Para procesar este volumen con el TMO actual, se requirieron aproximadamente **{workload_hours:.1f} horas productivas**.")
    
    st.info("Nota: Este cálculo representa la carga neta. En fases posteriores (FORGE), ajustaremos esto con ausentismo y adherencia.")

else:
    st.warning("No hay datos de ACD disponibles. Por favor, ve a CORTEX y genera o carga datos primero.")
    if st.button("Ir a CORTEX"):
        st.switch_page("pages/1_CORTEX.py")
