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

# 1. Recuperar datos
df_acd = st.session_state.get('data_acd')
df_qa = st.session_state.get('data_qa')

if df_acd is not None:
    # --- PANEL DE CRITERIOS (EDITABLE) ---
    with st.sidebar:
        st.header("Criterios de Contrato")
        st.write("Ajusta los valores para el calculo del mes:")
        
        # Diccionario base de tarifas por PCRC
        tarifas_base = {
            "Ventas": {"hora": 18.5, "bono": 500.0, "multa": 50.0},
            "Atencion": {"hora": 13.0, "bono": 300.0, "multa": 30.0},
            "Soporte": {"hora": 21.0, "bono": 400.0, "multa": 100.0},
            "Retenciones": {"hora": 19.5, "bono": 600.0, "multa": 80.0}
        }
        
        pcrc_sel = st.selectbox("PCRC a Liquidar:", list(df_acd['pcrc'].unique()))
        
        # Inputs editables cargados con la base del PCRC seleccionado
        base = tarifas_base.get(pcrc_sel)
        val_hora = st.number_input("Tarifa USD/Hora", value=base["hora"])
        val_bono = st.number_input("Bono por Calidad (>90%)", value=base["bono"])
        val_multa = st.number_input("Multa por Error Critico (RAC)", value=base["multa"])

    # --- LOGICA DE CALCULOS ---
    df_f = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    
    # Horas y Monto Base
    horas_facturables = df_f['tmo_segundos'].sum() / 3600
    monto_base = horas_facturables * val_hora
    
    # Calculo de Incentivos y Penalidades usando los datos de QA
    incentivos = 0.0
    penalidades = 0.0
    nota_avg = 0.0
    rac_count = 0

    if df_qa is not None:
        df_qa_f = df_qa[df_qa['id_llamada'].isin(df_f['id_llamada'])]
        if not df_qa_f.empty:
            nota_avg = df_qa_f['nota_final'].mean()
            rac_count = len(df_qa_f[df_qa_f['error_critico'] == 'Si'])
            
            # Aplicacion de criterios
            if nota_avg >= 90:
                incentivos = val_bono
            penalidades = rac_count * val_multa

    total_liquidar = monto_base + incentivos - penalidades

    # --- VISTA DE CRITERIOS APLICADOS ---
    st.info(f"**Criterios Aplicados para {pcrc_sel}:** Tarifa USD {val_hora}/h | Bono si QA >= 90% | Penalidad USD {val_multa} por RAC.")

    # --- SCORECARD ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monto Horas", f"USD {monto_base:,.2f}")
    c2.metric("Incentivos", f"USD {incentivos:,.2f}", delta=f"QA: {nota_avg:.1f}%")
    c3.metric("Penalidades", f"USD {penalidades:,.2f}", delta=f"RACs: {rac_count}", delta_color="inverse")
    c4.metric("Total Liquidar", f"USD {total_liquidar:,.2f}")

    # --- GRAFICAS ---
    st.divider()
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Composicion de la factura
        df_comp = pd.DataFrame({
            "Concepto": ["Base Operativa", "Bonos", "Multas"],
            "Monto": [monto_base, incentivos, penalidades]
        })
        fig_pie = px.pie(df_comp, names="Concepto", values="Monto", 
                         title=f"Distribucion de Costos: {pcrc_sel}",
                         color_discrete_map={"Base Operativa":"#1f77b4", "Bonos":"#2ca02c", "Multas":"#d62728"})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Comparativa de CPH (Costo por Hora Real vs Pactada)
        st.write("### Auditoria de Cumplimiento")
        st.write(f"Para el negocio de **{pcrc_sel}**, se han auditado **{len(df_qa_f) if df_qa is not None else 0}** llamadas.")
        if rac_count > 0:
            st.warning(f"Se han detectado {rac_count} errores criticos que impactan en -USD {penalidades:,.2f}")
        else:
            st.success("Operacion limpia de errores criticos en la muestra seleccionada.")

    # Tabla de detalle para transparencia
    with st.expander("Ver detalle de calculo por llamada"):
        st.dataframe(df_f[['fecha', 'id_llamada', 'tmo_segundos', 'site']].head(20), width='stretch')

else:
    st.error("Por favor, genera datos en CORTEX para visualizar la liquidacion.")
