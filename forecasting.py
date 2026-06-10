"""
Motor de Pronostico de Llamadas (Forecast WFM)
Modelo: Tendencia lineal sobre serie desestacionalizada x Indice de dia de semana.
Incluye backtest (WAPE/MAPE), perfil intradia y staffing con Erlang C.
"""
import numpy as np
import pandas as pd


def preparar_serie_diaria(df_acd, pcrc=None):
    """Agrega el detalle ACD a una serie diaria de llamadas (rellena dias sin datos con 0)."""
    df = df_acd.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    if pcrc and pcrc != "Todos":
        df = df[df['pcrc'] == pcrc]
    serie = df.set_index('fecha').resample('D').size()
    return serie.asfreq('D', fill_value=0)


def indices_dia_semana(serie):
    """Indice estacional por dia de semana (Lun=0 ... Dom=6). 1.0 = dia promedio."""
    media = serie.mean()
    if media == 0:
        return pd.Series(1.0, index=range(7))
    idx = serie.groupby(serie.index.dayofweek).mean() / media
    idx = idx.reindex(range(7), fill_value=1.0)
    return idx.replace(0, 1.0)


def pronosticar(serie, horizonte=30):
    """
    Genera el pronostico diario de llamadas.
    1. Desestacionaliza la serie con el indice de dia de semana.
    2. Ajusta tendencia lineal sobre la serie desestacionalizada.
    3. Proyecta y re-estacionaliza. Banda de confianza al 95% via residuos.
    Devuelve DataFrame con: fecha, pronostico, banda_inf, banda_sup.
    """
    if len(serie) < 14:
        raise ValueError("Se requieren al menos 14 dias de historia para pronosticar.")

    idx_dow = indices_dia_semana(serie)
    factor = serie.index.dayofweek.map(idx_dow).values
    desest = serie.values / factor

    t = np.arange(len(serie))
    pendiente, intercepto = np.polyfit(t, desest, 1)
    sigma = (desest - (pendiente * t + intercepto)).std()

    fechas_fut = pd.date_range(serie.index[-1] + pd.Timedelta(days=1), periods=horizonte, freq='D')
    t_fut = np.arange(len(serie), len(serie) + horizonte)
    base = pendiente * t_fut + intercepto
    estacional = fechas_fut.dayofweek.map(idx_dow).values

    return pd.DataFrame({
        'fecha': fechas_fut,
        'pronostico': np.maximum(base * estacional, 0),
        'banda_inf': np.maximum((base - 1.96 * sigma) * estacional, 0),
        'banda_sup': np.maximum((base + 1.96 * sigma) * estacional, 0),
    })


def backtest(serie, dias_prueba=14):
    """
    Valida el modelo: entrena sin los ultimos N dias y compara contra lo real.
    Devuelve dict con WAPE, MAPE, precision (100-WAPE) y el detalle real vs pronostico.
    """
    if len(serie) < dias_prueba + 14:
        raise ValueError("Historia insuficiente para el backtest solicitado.")

    train, test = serie[:-dias_prueba], serie[-dias_prueba:]
    pred = pronosticar(train, dias_prueba)
    real, est = test.values.astype(float), pred['pronostico'].values

    wape = np.abs(real - est).sum() / max(real.sum(), 1) * 100
    con_volumen = real > 0
    mape = (np.abs(real[con_volumen] - est[con_volumen]) / real[con_volumen]).mean() * 100 if con_volumen.any() else 0.0

    detalle = pd.DataFrame({'fecha': test.index, 'real': real, 'pronostico': est})
    return {'wape': wape, 'mape': mape, 'precision': max(0.0, 100 - wape), 'detalle': detalle}


def perfil_intradia(df_acd, pcrc=None):
    """Proporcion historica de llamadas por hora del dia (suma 1.0)."""
    df = df_acd.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    if pcrc and pcrc != "Todos":
        df = df[df['pcrc'] == pcrc]
    conteo = df.groupby(df['fecha'].dt.hour).size().reindex(range(24), fill_value=0)
    total = conteo.sum()
    if total == 0:
        return pd.Series(1.0 / 24, index=range(24))
    return conteo / total


def distribuir_intradia(total_dia, perfil):
    """Reparte el total diario pronosticado en los 24 intervalos horarios."""
    return (perfil * total_dia).round().astype(int)


def _prob_espera_erlang_c(n_agentes, intensidad):
    """Probabilidad de espera (formula Erlang C, via Erlang B iterativo para evitar overflow)."""
    b = 1.0
    for k in range(1, n_agentes + 1):
        b = intensidad * b / (k + intensidad * b)
    return n_agentes * b / (n_agentes - intensidad * (1 - b))


def agentes_requeridos(llamadas, tmo_seg, intervalo_seg=3600, asa_objetivo_seg=20, sl_objetivo=0.80):
    """
    Calcula agentes necesarios por intervalo para cumplir el nivel de servicio (Erlang C).
    sl_objetivo: fraccion de llamadas atendidas antes de asa_objetivo_seg (ej. 0.80 = SL 80/20).
    """
    if llamadas <= 0 or tmo_seg <= 0:
        return 0
    intensidad = llamadas * tmo_seg / intervalo_seg  # carga en erlangs
    n = max(int(np.ceil(intensidad)), 1)
    while n < intensidad + 500:
        if n > intensidad:  # con n <= intensidad la cola es inestable
            pw = _prob_espera_erlang_c(n, intensidad)
            sl = 1 - pw * np.exp(-(n - intensidad) * asa_objetivo_seg / tmo_seg)
            if sl >= sl_objetivo:
                return n
        n += 1
    return n
