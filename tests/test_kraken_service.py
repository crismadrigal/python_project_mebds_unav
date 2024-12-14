import pytest
import pandas as pd
from services.kraken_service import KrakenService

@pytest.fixture
def mock_kraken_service(mocker):
    service = KrakenService()
    mocker.patch.object(service.api, 'query_public')
    return service

def test_obtener_pares_kraken_exitoso(mock_kraken_service):
    mock_kraken_service.api.query_public.return_value = {
        'result': {
            'XBTUSD': {'wsname': 'XBT/USD'},
            'ETHUSD': {'wsname': 'ETH/USD'}
        }
    }
    pares = mock_kraken_service.obtener_pares_kraken()
    assert pares == ['XBT/USD', 'ETH/USD']

def test_obtener_pares_kraken_error(mock_kraken_service):
    mock_kraken_service.api.query_public.side_effect = Exception("Error de prueba")
    pares = mock_kraken_service.obtener_pares_kraken()
    assert pares is None

def test_obtener_datos_kraken_exitoso(mock_kraken_service):
    mock_kraken_service.api.query_public.return_value = {
        'result': {
            'XBTUSD': [
                [1635278400, '61250.0', '61650.0', '61000.0', '61500.0', '61400.0', '120.5', 240]
            ]
        }
    }
    df = mock_kraken_service.obtener_datos_kraken('XBTUSD')
    assert not df.empty, "El DataFrame debería contener datos"
    assert list(df.columns) == ['Open', 'High', 'Low', 'Close', 'VWAP', 'Volume', 'Count']

def test_obtener_datos_kraken_error(mock_kraken_service):
    mock_kraken_service.api.query_public.side_effect = Exception("Error de prueba")
    df = mock_kraken_service.obtener_datos_kraken('XBTUSD')
    assert df.empty
