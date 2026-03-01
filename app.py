import streamlit as st

# 1. Configuración de navegación para que el menú diga INICIO
# Esto reemplaza el texto "app" por un título limpio
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

# 2. Configuración de página
st.set_page_config(
    page_title="VMO AI | COPC R8.0",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Inicialización de estado
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# 4. Barra Lateral
with st.sidebar:
    st.title("Configuracion")
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()
    st.write("VMO Call Center OS v1.2")

# 5. Ejecución del Dashboard de Inicio
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# Títulos del Portal
st.caption("VMO AI • COPC R8.0")
st.title("Sistema de 8 Agentes IA para Gestión de BPO")

# Grid de Agentes (Mosaico)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**ATLAS**\n\nCerebro ejecutivo del VMO. Consolida KPIs, genera Business Review.")
    st.success("**SENTINEL**\n\nControl calidad end-to-end. Automatiza monitoreo y RACs.")

with col2:
    st.info("**PULSE**\n\nMide y analiza CX. Gestiona CSAT/DSAT, NPS y sentimiento.")
    st.success("**NEXUS**\n\nMotor WFM completo. Forecast, Capacity y GTR automatizado.")

with col3:
    st.info("**FORGE**\n\nCiclo de vida del agente. Reclutamiento, formación y skills.")
    st.success("**BLUEPRINT**\n\nDiseña y controla cambios en procesos y PCRCs.")

with col4:
    st.info("**LEDGER**\n\nControla relación económica. Facturación, multas y bonos.")
    st.success("**CORTEX**\n\nMotor de datos central. Valida integridad y genera reportes.")

st.divider()

# Sección Informativa
c_txt, c_img = st.columns([2, 1])

with c_txt:
    st.subheader("Flujo de Trabajo Sugerido")
    st.markdown("""
    1. **Carga**: Ve a **CORTEX** para generar 180 días de datos operativos.
    2. **Análisis**: Navega por **NEXUS** y **SENTINEL** para ver capacidad y calidad.
    3. **Estrategia**: Consulta **ATLAS** para el resumen ejecutivo mensual.
    """)
    st.info("💡 Tip: Si los datos no cargan en los módulos, regresa a CORTEX y genera un nuevo ecosistema.")

with c_img:
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
             caption="Operaciones Inteligentes VMO")
