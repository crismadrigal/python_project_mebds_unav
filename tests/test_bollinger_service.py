import pytest
import pandas as pd
from services.bollinger_service import BollingerBandsService

@pytest.fixture
def df_test():
    data = {'Time': pd.date_range(start='2024-01-01', periods=20, freq='D'),
            'Open': [1.0] * 20,
            'High': [1.5] * 20,
            'Low': [0.8] * 20,
            'Close': [1.2] * 20}
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    if df['Time'].isnull().any():
        raise ValueError("Existen valores nulos en la columna 'Time'.")
    df = df.set_index('Time')
    return df

def test_calcular_bandas_bollinger(df_test):
    service = BollingerBandsService(df_test)
    df = service.calcular_bandas_bollinger(period=10)
    assert 'Upper Band' in df.columns
    assert 'Lower Band' in df.columns
    assert not df['Upper Band'].isnull().all()
    assert 'MA' in df.columns and not df['MA'].isnull().all()

def test_detectar_alertas(df_test):
    service = BollingerBandsService(df_test)
    df = service.calcular_bandas_bollinger(period=10)
    df = service.detectar_alertas()
    assert 'Signal' in df.columns
    assert df['Signal'].notnull().sum() > 0

def test_generar_grafico_candlestick(df_test):
    service = BollingerBandsService(df_test)
    df = service.calcular_bandas_bollinger(period=10)
    df = service.detectar_alertas()
    fig = service.generar_grafico_candlestick(df, 'XBT/USD')
    assert fig is not None
    assert len(fig.data) > 0  # Asegúrate de que el gráfico tiene trazas
