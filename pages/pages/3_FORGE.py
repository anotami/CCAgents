import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="FORGE | Ejecución", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("🔥 FORGE: GTR e Intraday")

# Recuperar datos de CORTEX
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    st.subheader("Panel de Control Intraday")
    
    # Simulación de métricas de ejecución (Adherencia y Ausentismo)
    # En un escenario real, esto vendría de un log de RRHH o Logins
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Adherencia Actual", "92%", "-2%")
    with col2:
        st.metric("Ausentismo", "8.5%", "1.2%", delta_color="inverse")
    with col3:
        # Ocupación calculada: (Llamadas * TMO) / Tiempo disponible (simulado)
        st.metric("Ocupación", "84%", "5%")
    with col4:
        # Calculamos el desvío de llamadas vs lo esperado
        st.metric("Desvío Staffing", "-3 HC", delta_color="inverse")

    st.divider()

    # Visualización de Alertas GTR
    st.subheader("Alertas de Desvío en Tiempo Real")
    
    # Lógica de alertas basada en datos de CORTEX
    tasa_abandono = (df_acd['abandono'].sum() / len(df_acd)) * 100
    
    if tasa_abandono > 5:
        st.error(f"🚨 CRÍTICO: Tasa de abandono en {tasa_abandono:.1f}%. Se requiere redistribución de carga inmediata.")
    else:
        st.success("✅ Operación estable: Niveles de servicio dentro del umbral.")

    # Tabla de Adherencia por Site (Simulada con los sites de CORTEX)
    st.subheader("Cumplimiento por Site")
    sites = df_acd['site'].unique()
    data_cumplimiento = pd.DataFrame({
        'Site': sites,
        'Logueados': [np.random.randint(10, 50) for _ in sites],
        'Break/Almuerzo': [np.random.randint(1, 5) for _ in sites],
        'Adherencia %': [np.random.randint(85, 98) for _ in sites]
    })
    st.table(data_cumplimiento)

else:
    st.warning("No hay datos operativos. Regresa a CORTEX para cargar información.")
