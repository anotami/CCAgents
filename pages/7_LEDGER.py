import streamlit as st
import pandas as pd

st.set_page_config(page_title="LEDGER | Financiero", layout="wide")

st.title("LEDGER: Liquidacion por PCRC")

df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # Tarifas unicas por negocio
    tarifas = {"Ventas": 18.5, "Atencion": 13.0, "Soporte": 21.0, "Retenciones": 19.5}
    
    pcrc_sel = st.selectbox("Seleccione PCRC para Facturacion:", list(df_acd['pcrc'].unique()))
    tarifa_act = tarifas.get(pcrc_sel, 15.0)

    df_f = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    
    # Calculo de facturacion neta
    horas_totales = df_f['tmo_segundos'].sum() / 3600
    monto_total = horas_totales * tarifa_act

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Horas Atendidas", f"{horas_totales:.1f} h")
    c2.metric("Tarifa Pactada", f"USD {tarifa_act}/h")
    c3.metric("Monto a Facturar", f"USD {monto_total:,.2f}")

    st.info(f"Liquidacion basada en {len(df_f)} llamadas procesadas para el negocio de {pcrc_sel}.")
else:
    st.error("Cargue datos en CORTEX para ver la liquidacion.")
