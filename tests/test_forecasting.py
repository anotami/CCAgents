import numpy as np
import pandas as pd
import pytest

import forecasting as fc


@pytest.fixture
def df_acd_sintetico():
    """Genera 90 dias de llamadas con patron conocido: mas volumen entre semana, pico a las 10am."""
    rng = np.random.default_rng(42)
    registros = []
    fecha_ini = pd.Timestamp("2026-01-01")
    for d in range(90):
        fecha = fecha_ini + pd.Timedelta(days=d)
        base = 60 if fecha.dayofweek < 5 else 30  # finde con menos llamadas
        for _ in range(base + int(rng.integers(-5, 6))):
            pesos_hora = np.array([1]*9 + [8] + [3]*8 + [1]*6, dtype=float)
            hora = int(rng.choice(range(24), p=pesos_hora / pesos_hora.sum()))
            registros.append({
                'fecha': fecha.replace(hour=hora, minute=int(rng.integers(0, 60))),
                'pcrc': str(rng.choice(['Atencion', 'Ventas'])),
                'tmo_segundos': int(rng.normal(300, 50)),
            })
    return pd.DataFrame(registros)


def test_serie_diaria_cubre_todo_el_rango(df_acd_sintetico):
    serie = fc.preparar_serie_diaria(df_acd_sintetico)
    assert len(serie) == 90
    assert serie.sum() == len(df_acd_sintetico)


def test_indices_capturan_estacionalidad_semanal(df_acd_sintetico):
    serie = fc.preparar_serie_diaria(df_acd_sintetico)
    idx = fc.indices_dia_semana(serie)
    # Entre semana (0-4) debe estar por encima del promedio, finde (5-6) por debajo
    assert idx[:5].mean() > 1.0
    assert idx[5:].mean() < 1.0


def test_pronostico_devuelve_horizonte_y_bandas_coherentes(df_acd_sintetico):
    serie = fc.preparar_serie_diaria(df_acd_sintetico)
    df_fc = fc.pronosticar(serie, horizonte=21)
    assert len(df_fc) == 21
    assert df_fc['fecha'].iloc[0] == serie.index[-1] + pd.Timedelta(days=1)
    assert (df_fc['pronostico'] >= 0).all()
    assert (df_fc['banda_inf'] <= df_fc['pronostico']).all()
    assert (df_fc['pronostico'] <= df_fc['banda_sup']).all()


def test_pronostico_requiere_historia_minima():
    serie = pd.Series(10, index=pd.date_range("2026-01-01", periods=7, freq='D'))
    with pytest.raises(ValueError):
        fc.pronosticar(serie)


def test_backtest_precision_razonable_en_patron_estable(df_acd_sintetico):
    serie = fc.preparar_serie_diaria(df_acd_sintetico)
    bt = fc.backtest(serie, dias_prueba=14)
    # Con un patron sintetico estable el modelo debe lograr WAPE bajo
    assert bt['wape'] < 15
    assert len(bt['detalle']) == 14


def test_perfil_intradia_suma_uno_y_detecta_pico(df_acd_sintetico):
    perfil = fc.perfil_intradia(df_acd_sintetico)
    assert perfil.sum() == pytest.approx(1.0)
    assert perfil.idxmax() == 9  # el pico sintetico esta a las 9-10am


def test_distribuir_intradia_conserva_el_total():
    perfil = pd.Series(1 / 24, index=range(24))
    horario = fc.distribuir_intradia(240, perfil)
    assert horario.sum() == pytest.approx(240, abs=24)  # tolerancia por redondeo


def test_erlang_c_valores_conocidos():
    # 100 llamadas/hora, TMO 300s -> 8.33 erlangs; SL 80/20 requiere ~10-11 agentes
    n = fc.agentes_requeridos(100, 300, asa_objetivo_seg=20, sl_objetivo=0.80)
    assert 9 <= n <= 12
    # Siempre por encima de la carga ofrecida
    assert n > 100 * 300 / 3600


def test_erlang_c_casos_borde():
    assert fc.agentes_requeridos(0, 300) == 0
    assert fc.agentes_requeridos(10, 0) == 0
    # Mas exigencia de SL nunca debe requerir menos agentes
    n_relajado = fc.agentes_requeridos(100, 300, sl_objetivo=0.70)
    n_exigente = fc.agentes_requeridos(100, 300, sl_objetivo=0.95)
    assert n_exigente >= n_relajado
