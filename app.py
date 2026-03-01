import streamlit as st

# 1. Configuración de página (Debe ser lo primero)
st.set_page_config(
    page_title="CCAgents AI | FTDStudio",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialización de estado para los datos
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# 3. Barra Lateral (Sidebar)
with st.sidebar:
    st.title("Configuracion")
    # El toggle permite al usuario decidir si usa el simulador o sus propios archivos
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()
    st.write("VMO Call Center OS v1.2")

# 4. Banner Visual de Estado
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 5. Dashboard Principal de Agentes
st.caption("VMO AI • COPC R8.0")
st.title("Sistema de 8 Agentes IA para Gestión de BPO")

# Mosaico de Agentes (Visual de referencia)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**ATLAS**\n\nCerebro ejecutivo del VMO. Consolida KPIs y genera Business Reviews.")
    st.success("**SENTINEL**\n\nControl calidad end-to-end. Automatiza monitoreo y detecta RACs.")

with col2:
    st.info("**PULSE**\n\nMide y analiza CX. Gestiona CSAT, NPS y sentimiento del cliente.")
    st.success("**NEXUS**\n\nMotor WFM completo. Forecast, Capacity y GTR automatizado.")

with col3:
    st.info("**FORGE**\n\nCiclo de vida del agente. Reclutamiento, formación y desempeño.")
    st.success("**BLUEPRINT**\n\nDiseña y controla cambios en procesos y PCRCs.")

with col4:
    st.info("**LEDGER**\n\nControla la relación económica. Facturación, multas y bonos.")
    st.success("**CORTEX**\n\nMotor de datos central. Valida integridad y genera el ecosistema.")

st.divider()

# Instrucciones de uso
c_txt, c_img = st.columns([2, 1])

with c_txt:
    st.subheader("Flujo de Trabajo Sugerido")
    st.markdown("""
    1. Ve al módulo **CORTEX** para poblar el sistema con 180 días de datos.
    2. Navega por los módulos para ver el impacto en **Capacidad, Calidad y Finanzas**.
    3. Toma decisiones estratégicas en el módulo **ATLAS**.
    """)
    st.info("💡 Tip: Si un botón de la barra lateral no carga la página, intenta refrescar el navegador (F5).")

with c_img:
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
             caption="Operaciones Inteligentes VMO")
