import streamlit as st
import pandas as pd

st.set_page_config(page_title="SENTINEL | Calidad", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("🛡️ SENTINEL: Monitoreo y Errores")

# Recuperar datos de QA desde CORTEX
df_qa = st.session_state.get('data_qa')

if df_qa is not None:
    # 1. KPIs Globales de Calidad
    nota_promedio = df_qa['nota_final'].mean()
    conteo_rac = len(df_qa[df_qa['error_critico'] == 'Si'])
    compliance_rate = ((len(df_qa) - conteo_rac) / len(df_qa)) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Nota Calidad (Promedio)", f"{nota_promedio:.1f}%")
    col2.metric("Errores Criticos (RAC)", f"{conteo_rac}")
    col3.metric("% Cumplimiento (Compliance)", f"{compliance_rate:.1f}%")

    st.divider()

    # 2. Analisis de Errores Criticos
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Distribucion de Notas")
        # Histograma de notas para ver dispersion
        st.bar_chart(df_qa['nota_final'].value_counts().sort_index())

    with col_right:
        st.subheader("Alertas de Coaching Inmediato")
        df_alertas = df_qa[df_qa['error_critico'] == 'Si']
        if not df_alertas.empty:
            for index, row in df_alertas.iterrows():
                st.warning(f"⚠️ **ID: {row['id_llamada']}** - Evaluador: {row['evaluador']} requiere coaching por Error Critico.")
        else:
            st.success("No se detectaron errores criticos en la muestra actual.")

    # 3. Interdependencia: Calidad -> CORTEX (ACs RUICA)
    st.subheader("Acciones Correctivas Sugeridas")
    if conteo_rac > 0:
        st.info("💡 Sentinel sugiere abrir un ticket RUICA para analizar causa raiz en el modulo de MEJORA.")

else:
    st.warning("No hay datos de QA disponibles. Ve a CORTEX para generar o cargar una muestra de Calidad.")
    if st.button("Ir a CORTEX"):
        st.switch_page("pages/1_CORTEX.py")
