import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="FORGE | GTR", layout="wide")

# Banner de estado
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("FORGE: Control de Gestion en Tiempo Real (GTR)")

# 1. Recuperar datos
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # --- FILTRO MAESTRO DE PCRC ---
    pcrcs = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.selectbox("Seleccione PCRC para Monitoreo GTR:", pcrcs)

    if pcrc_sel != "Todos":
        df = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    else:
        df = df_acd.copy()

    # --- CONFIGURACION DE UMBRALES (GTR) ---
    # Definimos los targets segun el negocio
    targets = {
        "Ventas": {"tmo_max": 500, "SLA_min": 0.80},
        "Atencion": {"tmo_max": 320, "SLA_min": 0.85},
        "Soporte": {"tmo_max": 850, "SLA_min": 0.75},
        "Retenciones": {"tmo_max": 550, "SLA_min": 0.80},
        "Todos": {"tmo_max": 450, "SLA_min": 0.80}
    }
    limit = targets.get(pcrc_sel)

    # --- PANEL DE ALARMAS ---
    st.divider()
    tmo_actual = df['tmo_segundos'].mean()
    nivel_servicio = 1 - df['abandono'].mean()

    c1, c2, c3 = st.columns(3)
    
    # Alarma de TMO
    if tmo_actual > limit["tmo_max"]:
        c1.error(f"ALERTA TMO: {int(tmo_actual)}s (Excede {limit['tmo_max']}s)")
    else:
        c1.success(f"TMO Estable: {int(tmo_actual)}s")

    # Alarma de Nivel de Servicio (SLA)
    if nivel_servicio < limit["SLA_min"]:
        c2.error(f"ALERTA SLA: {nivel_servicio*100:.1f}% (Bajo el {limit['SLA_min']*100}%)")
    else:
        c2.success(f"SLA Cumplido: {nivel_servicio*100:.1f}%")
        
    c3.metric("Llamadas en Proceso", len(df.tail(50)))

    # --- GRAFICAS GTR ---
    st.write("### Graficas de Control de Procesos")
    col_a, col_b = st.columns(2)

    with col_a:
        # Heatmap de Abandono por Hora (Para detectar saturacion)
        df['Hora'] = df['fecha'].dt.hour
        df_error = df.groupby('Hora')['abandono'].mean().reset_index()
        fig_error = px.bar(df_error, x='Hora', y='abandono', 
                           title="Indice de Abandono por Intervalo",
                           color='abandono', color_continuous_scale='Reds')
        st.plotly_chart(fig_error, use_container_width=True)

    with col_b:
        # Grafica de Control de TMO (Evolucion Temporal)
        df_tmo_t = df.resample('H', on='fecha')['tmo_segundos'].mean().reset_index()
        fig_tmo = px.line(df_tmo_t, x='fecha', y='tmo_segundos', title="Evolucion del TMO por Hora")
        fig_tmo.add_hline(y=limit["tmo_max"], line_dash="dash", line_color="red", annotation_text="Limite Operativo")
        st.plotly_chart(fig_tmo, use_container_width=True)

    # --- SUGERENCIAS DE ACCION GTR ---
    st.divider()
    with st.expander("Sugerencias de Accion Inmediata"):
        if tmo_actual > limit["tmo_max"]:
            st.warning("⚠️ Accion: Activar protocolo de llamadas cortas. Revisar si hay incidencias tecnicas masivas.")
        if nivel_servicio < limit["SLA_min"]:
            st.warning("⚠️ Accion: Restringir descansos/capacitaciones. Solicitar apoyo de personal administrativo a linea.")
        if tmo_actual <= limit["tmo_max"] and nivel_servicio >= limit["SLA_min"]:
            st.success("✅ Accion: Operacion en verde. Mantener monitoreo preventivo.")

else:
    st.error("No hay datos cargados en CORTEX para el monitoreo GTR.")
