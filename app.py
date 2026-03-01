import streamlit as st

# 1. Definicion de la navegacion para que el menu diga INICIO
# Esto soluciona el texto "app" en el menu lateral
pg = st.navigation([
    st.Page("app.py", title="INICIO"),
    st.Page("pages/1_CORTEX.py", title="CORTEX"),
    st.Page("pages/2_NEXUS.py", title="NEXUS"),
    st.Page("pages/3_FORGE.py", title="FORGE"),
    st.Page("pages/4_SENTINEL.py", title="SENTINEL"),
    st.Page("pages/5_PULSE.py", title="PULSE"),
    st.Page("pages/6_BLUEPRINT.py", title="BLUEPRINT"),
    st.Page("pages/7_LEDGER.py", title="LEDGER"),
    st.Page("pages/8_ATLAS.py", title="ATLAS"),
    st.Page("pages/9_RUICA.py", title="RUICA"),
])

# 2. Configuracion de la pagina
st.set_page_config(
    page_title="INICIO | VMO OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Inicializacion de variables globales
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# 4. Barra Lateral de Configuracion
with st.sidebar:
    st.title("Configuracion")
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()
    st.write("VMO Call Center OS v1.2")

# Ejecutar el contenido de la pagina seleccionada
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

col_text, col_img = st.columns([2, 1])

with col_text:
    st.title("INICIO: Gestion VMO")
    st.markdown("""
    Bienvenido al centro de control operativo. Este sistema modular permite 
    supervisar la salud de tus proveedores BPO mediante agentes especializados.

    ### Flujo de Trabajo:
    1. **Carga**: Ve a **CORTEX** para generar 2 meses de datos diferenciados.
    2. **Analisis**: Explora **NEXUS** y **SENTINEL** para ver capacidad y calidad.
    3. **Estrategia**: Consulta **ATLAS** para el resumen ejecutivo mensual.
    """)
    # Corregido: Indentacion correcta dentro del bloque with
    st.info("Tip: Si los datos no cargan en los modulos, regresa a CORTEX y pulsa el boton de Generar Datos.")

with col_img:
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
             caption="Operaciones Inteligentes VMO")
