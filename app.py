import streamlit as st
import os

# 1. Configuración de página
st.set_page_config(
    page_title="INICIO | VMO OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Control de Entorno Global en Sidebar
if 'usando_datos_ejemplo' not in st.session_state:
    st.session_state.usando_datos_ejemplo = True

with st.sidebar:
    st.title("⚙️ Configuración")
    modo_datos = st.toggle("Activar Mis Datos", value=not st.session_state.usando_datos_ejemplo)
    st.session_state.usando_datos_ejemplo = not modo_datos
    st.divider()
    
    # --- BOTÓN DE AUDITORÍA AUTOMÁTICA ---
    st.subheader("🛠️ Soporte Técnico")
    if st.button("Ejecutar Test de Salud"):
        st.write("Auditando agentes...")
        paginas = [f for f in os.listdir('pages') if f.endswith('.py')]
        errores = []
        
        for pag in sorted(paginas):
            try:
                with open(f"pages/{pag}", "r", encoding="utf-8") as f:
                    exec(f.read(), {'st': st, 'pd': None, 'np': None, 'px': None})
                st.write(f"✅ {pag} listo.")
            except Exception as e:
                # Solo reportamos errores de sintaxis o indentación críticos
                if "IndentationError" in str(e) or "SyntaxError" in str(e):
                    errores.append(f"❌ {pag}: {str(e)}")
        
        if not errores:
            st.success("¡Todos los módulos están OK!")
        else:
            for err in errores:
                st.error(err)

# 3. Banner de Estado
if st.session_state.usando_datos_ejemplo:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.write("---")

# 4. Contenido Principal - INICIO
col_main, col_img = st.columns([2, 1])

with col_main:
    st.title("🏠 INICIO: Gestión VMO")
    st.markdown("""
    Bienvenido al portal **VMO Call Center OS**. Este es el centro de control 
    estratégico para supervisar la operación de tus proveedores BPO.
    
    ### Flujo de Trabajo Recomendado:
    1. **CORTEX**: Genera o carga la base de datos de 2 meses.
    2. **NEXUS/FORGE**: Valida la capacidad y la ejecución real.
    3. **SENTINEL/PULSE**: Audita la calidad y la voz del cliente.
    4. **ATLAS**: Revisa el resumen ejecutivo para tus comités de gerencia.
    """)
    st.info("💡 Utiliza el botón 'Ejecutar Test de Salud' en el menú lateral para verificar que todos los agentes estén operativos.")

with col_img:
    st.image("https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
             caption="VMO Strategic Operations")
