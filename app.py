import streamlit as st

# 1. Configuración de página
st.set_page_config(
    page_title="VMO Call Center OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Control de Entorno Global en Sidebar
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

with st.sidebar:
    st.title("Configuración")
    # Toggle para cambiar entre datos de prueba y reales
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()

# 3. Banner Visual de Estado
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 4. Contenido Principal
col_main, col_img = st.columns([2, 1])

with col_main:
    st.title("Sistema de Gestión VMO")
    st.markdown("""
    Bienvenido al ecosistema integral de gestión estratégica para Call Centers. 
    Este sistema automatiza el flujo de decisión basado en datos reales de operación, 
    calidad y experiencia del cliente.

    ### Instrucciones Rápidas:
    1. Ve al módulo **CORTEX** para poblar el sistema con 2 meses de datos.
    2. Navega por los módulos para ver el impacto en **Capacidad, Calidad y Finanzas**.
    3. Toma decisiones estratégicas en el módulo **ATLAS**.
    """)

with col_img:
    # Imagen alusiva a centros de datos y operaciones
    

st.info("💡 Tip: Si los datos no cargan en los módulos, regresa a CORTEX y pulsa el botón de Generar Datos.")
