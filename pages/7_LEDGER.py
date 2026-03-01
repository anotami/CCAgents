import streamlit as st
import pandas as pd

st.set_page_config(page_title="LEDGER | Financiero", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("💰 LEDGER: Liquidación Financiera por PCRC")

# Recuperar datos
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')

if df_acd is not None:
    # --- FILTROS Y TARIFAS LATERALES ---
    st.sidebar.header("Configuración de Contrato")
    lista_pcrc = list(df_acd['pcrc'].unique())
    pcrc_sel = st.sidebar.selectbox("Selecciona PCRC para Liquidar", lista_pcrc)
    
    # Tarifas dinámicas según el PCRC seleccionado
    st.sidebar.divider()
    costo_h = st.sidebar.number_input(f"Tarifa Hora {pcrc_sel} (USD)", value=15.0 if pcrc_sel == "Ventas" else 12.0)
    bono_calidad = st.sidebar.number_input("Bono Cumplimiento QA (USD)", value=1000.0)
    penalidad_rac = st.sidebar.number_input("Multa por Error Crítico (USD)", value=100.0)

    # Filtrado de datos para el cálculo
    df_acd_f = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    ids_pcrc = df_acd_f['id_llamada']
    df_qa_f = df_qa[df_qa['id_llamada'].isin(ids_pcrc)].copy() if df_qa is not None else None

    # --- LÓGICA DE CÁLCULO ---
    total_lls = len(df_acd_f)
    tmo_avg = df_acd_f['tmo_segundos'].mean()
    horas_prod = (total_lls * tmo_avg) / 3600
    monto_base = horas_prod * costo_h
    
    # Ajustes por Calidad (Sentinel)
    ajustes = 0
    nota_qa = 0
    if df_qa_f is not None and not df_qa_f.empty:
        nota_qa = df_qa_f['nota_final'].mean()
        rac_counts = len(df_qa_f[df_qa_f['error_critico'] == 'Si'])
        ajustes -= (rac_counts * penalidad_rac)
        if nota_qa >= 90:
            ajustes += bono_calidad

    total_factura = monto_base + ajustes

    # --- VISUALIZACIÓN ---
    st.subheader(f"Estado de Cuenta: {pcrc_sel}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Horas a Liquidar", f"{horas_prod:.1f} h")
    c2.metric("Monto Operativo", f"${monto_base:,.2f}")
    c3.metric("Total Factura", f"${total_factura:,.2f}", f"${ajustes:,.2f} Ajustes")

    st.divider()

    # Desglose de Liquidación
    st.subheader("Detalle de Conceptos")
    desglose = pd.DataFrame({
        "Concepto": ["Servicio de Voz (Horas)", "Ajustes por Calidad (Nota)", "Penalidades Errores Críticos", "TOTAL"],
        "Detalle": [f"{total_lls} llamadas atendidas", f"Nota: {nota_qa:.1f}%", f"RACs detectados", "-"],
        "Monto": [f"${monto_base:,.2f}", f"${max(0, ajustes):,.2f}", f"${min(0, ajustes):,.2f}", f"${total_factura:,.2f}"]
    })
    st.table(desglose)

    st.info(f"💡 El cálculo financiero de **LEDGER** utiliza las horas productivas validadas en **NEXUS** y los errores críticos de **SENTINEL**.")

else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX para generar el ecosistema de 2 meses.")
