import streamlit as st
import os

# 1. Configuracion de pagina
st.set_page_config(
    page_title="INICIO | VMO OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicializacion de variables globales
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

# 3. BARRA LATERAL (Configuracion y Auditoria)
with st.sidebar:
    st.title("Configuracion")
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    
    st.divider()
    
    # --- BOTON DE AUDITORIA DE CODIGO ---
    st.subheader("Auditoria de Sistema")
    if st.button("Ejecutar Test de Salud"):
        st.write("Verificando integridad de los modulos...")
        folder = 'pages'
        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.endswith('.py')]
            errors_found = False
            
            for file in sorted(files):
                path = os.path.join(folder, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        # Compila el codigo para buscar errores de sintaxis o indentacion
                        compile(f.read(), path, 'exec')
                    st.success(f"Archivo OK: {file}")
                except Exception as e:
                    errors_found = True
                    st.error(f"Error en: {file}")
                    st.code(str(e))
            
            if not errors_found:
                st.balloons()
                st.success("¡Diagnostico completado! No se detectaron errores de codigo.")
        else:
            st.error("Carpeta 'pages/' no encontrada.")

# 4. Banner de Estado
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 5. CONTENIDO PRINCIPAL (INICIO)
col_text, col_img = st.columns([2, 1])

with col_text:
    st.title("INICIO: Gestion VMO")
    st.markdown("""
    Bienvenido al centro de control operativo **VMO Call Center OS**. 
    Este sistema modular permite supervisar la salud de tus proveedores BPO 
    mediante agentes especializados de analisis.

    ### Pasos para operar el sistema:
    1. **Carga**: Ve a **CORTEX** para generar la base de 2 meses.
    2. **Analisis**: Explora **NEXUS** y **SENTINEL** para ver capacidad y calidad.
    3. **Estrategia**: Consulta **ATLAS** para el resumen ejecutivo.
    """)
    st.info("💡 Tip: Si realizas cambios en el codigo, usa el boton 'Ejecutar Test de Salud' para confirmar que todo sigue operativo.")

with col_img:
    # Imagen técnica de operaciones
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80")
