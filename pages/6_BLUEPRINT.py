import streamlit as st
import pandas as pd

st.set_page_config(page_title="BLUEPRINT | Procesos", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("📐 BLUEPRINT: Diseño y Cambios")

# Seccion de control de procesos
st.subheader("Gestion de PCRCs (Procesos, Canales, Recursos y Controles)")

with st.expander("Registrar Nuevo Cambio en Proceso", expanded=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        proceso = st.selectbox("Proceso afectado", ["Ventas", "Atencion al Cliente", "Soporte Tecnico", "Retenciones"])
        tipo_cambio = st.radio("Tipo de intervencion", ["Rediseño de Script", "Ajuste de Workflow", "Nuevo Control QA"])
    with col_f2:
        motivo = st.text_area("Motivo del cambio (Basado en PULSE/SENTINEL)", "Ej: Se detecto alta friccion en el paso 3 del journey...")

    if st.button("Implementar Cambio"):
        st.success(f"Cambio registrado para el proceso de {proceso}. Se ha notificado a CORTEX para trackear el impacto en la proxima ingesta.")

st.divider()

# Tablero de Control de Cambios
st.subheader("Estado de Implementaciones")
data_cambios = {
    "Fecha": ["2026-02-20", "2026-02-25"],
    "Proceso": ["Retenciones", "Ventas"],
    "Cambio": ["Nuevo Script de Rebatimiento", "Validacion de Identidad Biometrica"],
    "Estado": ["En Produccion", "Piloto"],
    "Impacto Esperado": ["+5% CSAT", "-20s TMO"]
}
st.table(pd.DataFrame(data_cambios))

st.info("💡 Blueprint recibe puntos de falla de PULSE. Si los sentimientos negativos suben, Blueprint debe rediseñar el PCRC correspondiente.")
