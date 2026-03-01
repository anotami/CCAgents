import streamlit as st
import pandas as pd

st.set_page_config(page_title="LEDGER | Financiero", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("💰 LEDGER: Control Economico")

# Recuperar datos de otros modulos para el calculo
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')

if df_acd is not None:
    st.subheader("Calculo de Facturacion Mensual Estimada")
    
    # Parametros de negocio (Configurables)
    with st.sidebar:
        st.header("Configuracion de Tarifas")
        costo_hora = st.number_input("Costo por Hora Productiva (USD)", value=12.5)
        bono_calidad = st.number_input("Bono por Calidad > 90% (USD)", value=500.0)
        penalidad_rac = st.number_input("Penalidad por Error Critico (USD)", value=50.0)

    # Logica de calculo
    tmo_promedio = df_acd['tmo_segundos'].mean()
    total_llamadas = len(df_acd)
    # Horas productivas = (Llamadas * TMO) / 3600
    horas_productivas = (total_llamadas * tmo_promedio) / 3600
    subtotal = horas_productivas * costo_hora
    
    # Ajustes por Calidad (SENTINEL)
    ajustes = 0
    if df_qa is not None:
        errores_criticos = len(df_qa[df_qa['error_critico'] == 'Si'])
        nota_media = df_qa['nota_final'].mean()
        ajustes -= (errores_criticos * penalidad_rac)
        if nota_media > 90:
            ajustes += bono_calidad

    total_factura = subtotal + ajustes

    # Visualizacion de Resultados
    c1, c2, c3 = st.columns(3)
    c1.metric("Horas Productivas", f"{horas_productivas:.1f} h")
    c2.metric("Subtotal Operativo", f"${subtotal:,.2f}")
    c3.metric("Total Facturacion", f"${total_factura:,.2f}", f"${ajustes:,.2f} Ajustes")

    st.divider()

    # Resumen para QBR (Quarterly Business Review)
    st.subheader("Consolidado para QBR por BPO")
    st.write("Este resumen integra el output de NEXUS (Horas) y SENTINEL (Performance) para la liquidacion financiera.")
    
    data_qbr = {
        "Concepto": ["Horas Netas", "Bonos Desempeño", "Penalidades QA", "Monto Final"],
        "Valor": [f"{horas_productivas:.1f}", f"${max(0, ajustes):,.2f}", f"${min(0, ajustes):,.2f}", f"${total_factura:,.2f}"]
    }
    st.table(pd.DataFrame(data_qbr))

else:
    st.warning("No hay datos operativos suficientes para calcular la facturacion. Asegurate de cargar datos en CORTEX.")
