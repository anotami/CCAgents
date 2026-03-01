import streamlit as st

# Configuracion basica
st.set_page_config(page_title="VMO Call Center OS", layout="wide")

# Inicializar el estado si no existe
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# Banner superior
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("Sistema de Gestion VMO")
st.write("Si ves este mensaje, la app ya salio del horno. Usa el menu de la izquierda para ir a CORTEX.")

if st.button("Cambiar a modo Tus Datos"):
    st.session_state.usando_datos_ejemplo = False
    st.rerun()
