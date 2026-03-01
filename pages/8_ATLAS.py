import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ATLAS | Estrategia", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("🧭 ATLAS: Consolidacion Ejecutiva")

# Recuperar datos de todos los modulos
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')
df_cx = st.session_state.get('data_cx')

if df_acd is not None:
    st.subheader("Resumen Ejecutivo Diario / WBR")
    
    # 1. Scorecard Balanceado
    c1, c2, c3, c4 = st.columns(4)
    
    # Metricas de NEXUS/FORGE
    volumen = len(df_acd)
    c1.metric("Volumen Total", f"{volumen} lls")
    
    # Metricas de SENTINEL
    if df_qa is not None:
        nota_qa = df_qa['nota_final'].mean()
        c2.metric("Calidad (QA)", f"{nota_qa:.1f}%")
    
    # Metricas de PULSE
    if df_cx is not None:
        csat = df_cx['csat'].mean()
        c3.metric("Experiencia (CSAT)", f"{csat:.2f}")
    
    # Metrica de Eficiencia (Regla 50/75 simulada)
    c4.metric("Indice Eficiencia (50/75)", "72%", "+2%")

    st.divider()

    # 2. Analisis de Correlacion: Calidad vs Satisfaccion
    st.subheader("Analisis de Priorizacion Estrategica")
    col_chart, col_text = st.columns([2, 1])
    
    with col_chart:
        # Simulamos una comparativa por Site
        data_atp = pd.DataFrame({
            'Site': df_acd['site'].unique(),
            'Productividad': [np.random.randint(70, 95) for _ in df_acd['site'].unique()],
            'Calidad': [np.random.randint(80, 100) for _ in df_acd['site'].unique()]
        })
        fig = px.scatter(data_atp, x="Productividad", y="Calidad", text="Site", size_max=60)
        st.plotly_chart(fig, use_container_width=True)

    with col_text:
        st.info("**Decision VMO:**")
        st.write("Basado en el cuadrante, el Site de Cordoba requiere re-priorizacion de recursos hacia coaching tecnico.")
        if st.button("Generar Reporte MBR Mensual"):
            st.success("Reporte MBR preparado y listo para exportar.")

else:
    st.warning("No hay datos suficientes para consolidar la estrategia. Por favor, completa el ciclo en CORTEX.")
