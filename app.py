import streamlit as st

# 1. Configuración de página (SIEMPRE debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="VMO Call Center OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Control de Entorno: Lógica central para los datos
# Por ahora lo definimos aquí, luego lo podemos conectar a un botón en la barra lateral
usando_datos_ejemplo = True 

# Alerta visual estandarizada en la parte superior
if usando_datos_ejemplo:
    st.markdown("<h2 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>DATOS DE EJEMPLO</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>TUS DATOS</h2>", unsafe_allow_html=True)

st.write("---")

# 3. Contenido de la página de inicio
st.title("Sistema de Gestión VMO 🏢")
st.markdown("""
Bienvenido al ecosistema integral de gestión de Call Centers y BPOs. 
Este sistema está diseñado en 9 fases modulares que se alimentan entre sí.

👈 **Para comenzar, selecciona un módulo en el menú lateral izquierdo.**

### Flujo del Ecosistema:
1. 🧠 **CORTEX:** Ingesta y validación de datos (ACD, CRM, QA).
2. ⚙️ **NEXUS:** Dimensionamiento y cálculo de capacidad.
3. 🔥 **FORGE:** GTR Intraday y ejecución.
4. 🛡️ **SENTINEL:** Calidad, monitoreo y detección de errores.
5. 💓 **PULSE:** Medición de la experiencia (CX/CSAT).
6. 📐 **BLUEPRINT:** Diseño y reingeniería de procesos.
7. 💰 **LEDGER:** Control económico y facturación.
8. 🧭 **ATLAS:** Estrategia y consolidación ejecutiva.
9. ↻ **RUICA:** Mejora continua.
""")

st.info("💡 **Tip:** Asegúrate de subir los archivos base en CORTEX antes de operar los demás módulos.")
