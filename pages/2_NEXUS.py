import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import forecasting as fc

st.set_page_config(page_title="NEXUS | Capacidad", layout="wide")

# Banner de estado persistente
if st.session_state.get('usando_datos_ejemplo', True):
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>Datos de Ejemplo</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: #00cc66; background-color: #e6ffe6; padding: 10px; border-radius: 5px;'>Tus Datos</h1>", unsafe_allow_html=True)

st.title("NEXUS: Dimensionamiento y Capacidad")

# Recuperar datos de CORTEX
df_acd = st.session_state.get('data_acd')

if df_acd is not None:
    # 1. Preparacion de base temporal
    df_acd['fecha'] = pd.to_datetime(df_acd['fecha'])
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = {'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mie', 'Thursday': 'Jue', 'Friday': 'Vie', 'Saturday': 'Sab', 'Sunday': 'Dom'}
    
    # --- SELECCION DE PCRC (FILTRO MAESTRO) ---
    lista_pcrc = ["Todos"] + list(df_acd['pcrc'].unique())
    pcrc_sel = st.selectbox("Seleccione el PCRC a analizar:", lista_pcrc)
    
    # Aplicacion del filtro maestro a todo el modulo
    if pcrc_sel != "Todos":
        df = df_acd[df_acd['pcrc'] == pcrc_sel].copy()
    else:
        df = df_acd.copy()

    st.divider()

    # --- FILA 1: VOLUMEN MENSUAL Y SEMANAL ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Volumen Mensual: {pcrc_sel}")
        df_mensual = df.resample('M', on='fecha').size().reset_index(name='Llamadas')
        df_mensual['Mes'] = df_mensual['fecha'].dt.strftime('%b %Y')
        fig_mes = px.bar(df_mensual, x='Mes', y='Llamadas', color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_mes, use_container_width=True)

    with col2:
        st.subheader(f"Volumen Semanal: {pcrc_sel}")
        df_semanal = df.resample('W', on='fecha').size().reset_index(name='Llamadas')
        df_semanal['Semana'] = df_semanal['fecha'].dt.strftime('Sem %U')
        fig_sem = px.line(df_semanal, x='Semana', y='Llamadas', markers=True)
        st.plotly_chart(fig_sem, use_container_width=True)

    # --- FILA 2: VOLUMEN POR DIA Y TMO POR DIA ---
    col3, col4 = st.columns(2)
    with col3:
        st.subheader(f"Volumen por Dia de Semana: {pcrc_sel}")
        df['Dia_Nombre'] = df['fecha'].dt.day_name()
        df_vol_dia = df.groupby('Dia_Nombre').size().reindex(dias_orden).reset_index(name='Llamadas')
        df_vol_dia['Dia'] = df_vol_dia['Dia_Nombre'].map(dias_es)
        fig_vol_dia = px.bar(df_vol_dia, x='Dia', y='Llamadas', color='Llamadas', color_continuous_scale='Blues')
        st.plotly_chart(fig_vol_dia, use_container_width=True)

    with col4:
        st.subheader(f"TMO Promedio por Dia: {pcrc_sel}")
        df_tmo_dia = df.groupby('Dia_Nombre')['tmo_segundos'].mean().reindex(dias_orden).reset_index(name='TMO')
        df_tmo_dia['Dia'] = df_tmo_dia['Dia_Nombre'].map(dias_es)
        fig_tmo_dia = px.line(df_tmo_dia, x='Dia', y='TMO', markers=True, color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_tmo_dia, use_container_width=True)

    # --- FILA 3: CURVA DE ARRIBO E INFO ---
    st.subheader(f"Curva de Arribo por Intervalo: {pcrc_sel}")
    df['Hora'] = df['fecha'].dt.hour
    df_intervalo = df.groupby('Hora').size().reset_index(name='Llamadas')
    fig_int = px.bar(df_intervalo, x='Hora', y='Llamadas', color='Llamadas', color_continuous_scale='Viridis')
    st.plotly_chart(fig_int, use_container_width=True)

    # --- RESUMEN FINAL ---
    st.divider()
    tmo_avg = df['tmo_segundos'].mean()
    workload_hrs = (len(df) * tmo_avg) / 3600
    st.info(f"Analisis de Capacidad ({pcrc_sel}): Carga total de {workload_hrs:.1f} horas netas. TMO promedio de {int(tmo_avg)} segundos.")

    # =========================================================
    # AGENTE DE PRONOSTICO DE LLAMADAS (FORECAST)
    # =========================================================
    st.divider()
    st.header(f"Pronostico de Llamadas: {pcrc_sel}")

    # --- Parametros del modelo ---
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        horizonte = st.slider("Horizonte de pronostico (dias)", 7, 90, 30)
    with c_p2:
        dias_bt = st.slider("Dias de validacion (backtest)", 7, 28, 14)
    with c_p3:
        sl_pct = st.slider("Nivel de Servicio objetivo (%)", 70, 95, 80)
        asa_obj = st.number_input("ASA objetivo (segundos)", 5, 120, 20)

    serie = fc.preparar_serie_diaria(df_acd, pcrc_sel)

    try:
        # --- 1. Validacion del modelo (backtest) ---
        bt = fc.backtest(serie, dias_prueba=dias_bt)
        m1, m2, m3 = st.columns(3)
        m1.metric("Precision del modelo", f"{bt['precision']:.1f}%")
        m2.metric("WAPE", f"{bt['wape']:.1f}%")
        m3.metric("MAPE", f"{bt['mape']:.1f}%")
        st.caption(f"Validado contra los ultimos {dias_bt} dias reales (entrenando solo con los dias previos).")

        # --- 2. Pronostico futuro ---
        df_fc = fc.pronosticar(serie, horizonte)

        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=serie.index, y=serie.values, name="Historico",
                                    line=dict(color="#1f77b4")))
        fig_fc.add_trace(go.Scatter(x=df_fc['fecha'], y=df_fc['banda_sup'], name="Banda superior",
                                    line=dict(width=0), showlegend=False))
        fig_fc.add_trace(go.Scatter(x=df_fc['fecha'], y=df_fc['banda_inf'], name="Confianza 95%",
                                    fill='tonexty', fillcolor='rgba(255,127,14,0.2)', line=dict(width=0)))
        fig_fc.add_trace(go.Scatter(x=df_fc['fecha'], y=df_fc['pronostico'], name="Pronostico",
                                    line=dict(color="#ff7f0e", dash="dash")))
        fig_fc.update_layout(title=f"Llamadas diarias: historico y pronostico a {horizonte} dias",
                             xaxis_title="Fecha", yaxis_title="Llamadas")
        st.plotly_chart(fig_fc, use_container_width=True)

        # --- 3. Dimensionamiento intradia (Erlang C) ---
        st.subheader("Dimensionamiento del dia pronosticado")
        fecha_sel = st.selectbox("Selecciona el dia a dimensionar:",
                                 df_fc['fecha'].dt.strftime('%Y-%m-%d (%a)'))
        total_dia = df_fc.loc[df_fc['fecha'].dt.strftime('%Y-%m-%d (%a)') == fecha_sel, 'pronostico'].iloc[0]

        perfil = fc.perfil_intradia(df_acd, pcrc_sel)
        llamadas_hora = fc.distribuir_intradia(total_dia, perfil)
        df_staff = pd.DataFrame({
            'Hora': range(24),
            'Llamadas': llamadas_hora.values,
            'Agentes': [fc.agentes_requeridos(v, tmo_avg, asa_objetivo_seg=asa_obj, sl_objetivo=sl_pct / 100)
                        for v in llamadas_hora.values]
        })

        c_g1, c_g2 = st.columns(2)
        with c_g1:
            fig_int_fc = px.bar(df_staff, x='Hora', y='Llamadas', color='Llamadas',
                                color_continuous_scale='Oranges',
                                title=f"Llamadas pronosticadas por hora ({int(total_dia)} totales)")
            st.plotly_chart(fig_int_fc, use_container_width=True)
        with c_g2:
            fig_staff = px.bar(df_staff, x='Hora', y='Agentes', color='Agentes',
                               color_continuous_scale='Greens',
                               title=f"Agentes requeridos (SL {sl_pct}/{asa_obj}, Erlang C)")
            st.plotly_chart(fig_staff, use_container_width=True)

        st.success(f"Para el {fecha_sel} se pronostican {int(total_dia)} llamadas. "
                   f"Pico de staffing: {df_staff['Agentes'].max()} agentes a las {df_staff.loc[df_staff['Agentes'].idxmax(), 'Hora']}:00 hrs.")

        # --- 4. Exportar pronostico ---
        csv_fc = df_fc.assign(fecha=df_fc['fecha'].dt.date).round(1).to_csv(index=False).encode('utf-8')
        st.download_button("Descargar pronostico (CSV)", csv_fc,
                           file_name=f"pronostico_{pcrc_sel}_{horizonte}d.csv", mime="text/csv")

    except ValueError as e:
        st.warning(f"No se pudo generar el pronostico: {e}")

else:
    st.warning("No hay datos cargados. Por favor, ve a CORTEX y genera el ecosistema de 2 meses.")
