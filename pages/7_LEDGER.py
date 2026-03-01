import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="LEDGER | Financiero", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("LEDGER: Auditoria y Liquidacion Financiera")

# 1. Recuperar datos de todos los agentes
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')

if df_acd is not None:
    # --- CONFIGURACION DE TARIFAS POR PCRC ---
    tarifas = {
        "Ventas": {"hora": 18.5, "bono_qa": 500, "penalidad_rac": 50},
        "Atencion": {"hora": 13.0, "bono_qa": 300, "penalidad_rac": 30},
        "Soporte": {"hora": 21.0, "bono_qa": 400, "penalidad_rac": 100},
        "Retenciones": {"hora": 19.5, "bono_qa": 600, "penalidad_rac": 80}
    }

    # FILTRO MAESTRO
    pcrc_sel = st.selectbox("Seleccione PCRC para Liquidacion:", list(df_acd['pcrc'].unique()))
    conf = tarifas.get(pcrc_sel)

    # Filtrado de datos correlacionados
    df_f = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    if df_qa is not None:
        df_qa_f = df_qa[df_qa['id_llamada'].isin(df_f['id_llamada'])]
    else:
        df_qa_f = pd.DataFrame()

    # --- CALCULOS CORE ---
    horas_facturables = df_f['tmo_segundos'].sum() / 3600
    monto_base = horas_facturables * conf["hora"]
    
    # Calculo de Ajustes (Bonos y Multas)
    multas = 0
    bonos = 0
    if not df_qa_f.empty:
        rac_count = len(df_qa_f[df_qa_f['error_critico'] == 'Si'])
        multas = rac_count * conf["penalidad_rac"]
        if df_qa_f['nota_final'].mean() > 90:
            bonos = conf["bono_qa"]

    total_final = monto_base + bonos - multas

    # --- VISTA 1: SCORECARD FINANCIERO ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monto Base", f"USD {monto_base:,.2f}")
    c2.metric("Bonos QA", f"USD {bonos:,.2f}", delta=f"{bonos}", delta_color="normal")
    c3.metric("Penalidades RAC", f"USD {multas:,.2f}", delta=f"-{multas}", delta_color="inverse")
    c4.metric("Total a Liquidar", f"USD {total_final:,.2f}")

    # --- VISTA 2: GRAFICAS DE DISTRIBUCION ---
    st.write("### Analisis de Costos y Desviaciones")
    col_a, col_b = st.columns(2)

    with col_a:
        # Composicion del pago
        df_pie = pd.DataFrame({
            "Concepto": ["Base Operativa", "Incentivos", "Deducciones"],
            "Valor": [monto_base, bonos, multas]
        })
        fig_pie = px.pie(df_pie, names="Concepto", values="Valor", 
                         title="Composicion de la Factura",
                         color_discrete_map={"Base Operativa":"#1f77b4", "Incentivos":"#2ca02c", "Deducciones":"#d62728"})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        # Tendencia de costo por llamada (CPH)
        df_f['fecha_d'] = pd.to_datetime(df_f['fecha']).dt.date
        cph_daily = df_f.groupby('fecha_d')['tmo_segundos'].mean() * (conf["hora"]/3600)
        fig_cph = px.line(x=cph_daily.index, y=cph_daily.values, 
                          title="Costo Promedio por Llamada (Tendencia)",
                          labels={'x': 'Fecha', 'y': 'USD per Call'})
        st.plotly_chart(fig_cph, use_container_width=True)

    # --- VISTA 3: TABLA DE AUDITORIA ---
    with st.expander("Ver Detalle de Auditoria para Facturacion"):
        st.write("Llamadas con Error Critico (RAC) que generaron penalidad:")
        if not df_qa_f.empty:
            rac_detail = df_qa_f[df_qa_f['error_critico'] == 'Si']
            st.dataframe(rac_detail, width='stretch')
        else:
            st.success("No se detectaron penalidades en este periodo.")

else:
    st.error("No hay datos para liquidar. Ve a CORTEX.")
