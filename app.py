import streamlit as st

# 1. Configuracion de pagina
# El parametro page_title cambia lo que sale en la pestaña del navegador
st.set_page_config(
    page_title="INICIO | VMO OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicializacion de variables globales
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# 3. BARRA LATERAL (Configuracion)
with st.sidebar:
    st.title("Configuracion")
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()
    st.write("VMO Call Center OS v1.2")

# 4. Banner de Estado
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 5. CONTENIDO PRINCIPAL (INICIO)
col_text, col_img = st.columns([2, 1])

with col_text:
    # Este titulo confirma que estamos en la pagina de INICIO
    st.title("INICIO: Gestion VMO")
    st.markdown("""
    Bienvenido al centro de control operativo. Este sistema modular permite 
    supervisar la salud de tus proveedores BPO mediante agentes especializados.

    ### Flujo de Trabajo:
    1. **Carga**: Ve a **CORTEX** para generar 2 meses de datos.
    2. **Analisis**: Explora **NEXUS** y **SENTINEL** para ver capacidad y calidad.
    3. **Estrategia**: Consulta **ATLAS** para el resumen ejecutivo mensual.
    """)
    # Corregido: Indentacion correcta para evitar el error anterior
    st.info("Tip: Si los datos no cargan en los modulos, regresa a CORTEX y pulsa el boton de Generar Datos.")

with col_img:
    # Imagen tecnica de operaciones (sin emojis)
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
             caption="Operaciones Inteligentes VMO")
