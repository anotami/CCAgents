import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="RUICA | Mejora", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("↻ RUICA: Registro Único de Mejora")

# 1. Seccion de Registro de Acciones Correctivas
st.subheader("Registro de Acciones Correctivas (AC)")

with st.expander("Abrir Nueva Acción Correctiva", expanded=True):
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        origen = st.selectbox("Origen de la Falla", ["SENTINEL (Calidad)", "PULSE (CX)", "FORGE (Operativo)"])
        criticidad = st.select_slider("Criticidad", options=["Baja", "Media", "Alta", "Bloqueante"])
    with col_r2:
        plan_accion = st.text_area("Descripción del Plan de Acción", "Ej: Re-capacitación en proceso de retención por errores críticos detectados...")
        fecha_cierre = st.date_input("Fecha compromiso de cierre")

    if st.button("Registrar en Ciclo de Mejora"):
        st.success(f"Acción Correctiva registrada. Se ha actualizado la KB del sistema.")

st.divider()

# 2. Status del Ciclo de Mejora
st.subheader("Cierre de Brechas (Tracking)")
data_ruica = {
    "ID AC": ["AC-001", "AC-002"],
    "Origen": ["SENTINEL", "PULSE"],
    "Accion": ["Ajuste de Script Ventas", "Feedback BPO Site Cordoba"],
    "Estado": ["Cerrada", "En Proceso"],
    "Efectividad": ["95%", "Pendiente"]
}
st.table(pd.DataFrame(data_ruica))

# 3. Actualizacion de la Base de Conocimiento (Knowledge Base)
st.subheader("Knowledge Base (KB) Update")
st.info("💡 RUICA ha detectado patrones de falla recurrentes. Se sugiere actualizar los manuales de entrenamiento en CORTEX para la próxima ingesta.")

if st.button("Reiniciar Ciclo VMO con Datos Mejorados"):
    st.balloons()
    st.write("Ciclo reiniciado. Los inputs de RUICA ahora forman parte del motor de validacion en CORTEX.")
