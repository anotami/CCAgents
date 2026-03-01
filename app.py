import streamlit as st

# 1. Configuracion de pagina
st.set_page_config(
    page_title="VMO Call Center OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Control de Entorno Global (PERSISTENTE)
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# Banner visual segun el estado de los datos
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 3. Contenido de la pagina de inicio
st.title("Sistema de Gestion VMO")
st.markdown("""
Bienvenido al ecosistema integral de gestion de Call Centers. 
Este sistema funciona en ciclos de 9 fases.

Usa el menu lateral para navegar entre los agentes.
""")

# Selector de modo para pruebas (esto ayuda a cambiar el banner)
if st.checkbox("Activar modo 'Mis Datos'"):
    st.session_state.usando_datos_ejemplo = False
    st.rerun()
