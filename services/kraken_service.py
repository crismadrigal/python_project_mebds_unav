import krakenex
import pandas as pd
from utils.error_handler import handle_errors

class KrakenService:
    def __init__(self):
        self.api = krakenex.API()

    @handle_errors
    def obtener_pares_kraken(self):
        response = self.api.query_public('AssetPairs')
        pairs = response['result']
        lista_pares = [pairs[pair]['wsname'] for pair in pairs]
        return lista_pares

    @handle_errors
    def obtener_datos_kraken(self, pair, since=None, interval=1440):
        params = {'pair': pair, 'interval': interval}
        if since:
            params['since'] = since
        response = self.api.query_public('OHLC', params)
        data = response['result'].get(pair, [])
        if not data:
            raise ValueError(f"No se obtuvieron datos para el par {pair}")
        df = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Volume', 'Count'])
        df['Time'] = pd.to_datetime(df['Time'], unit='s', errors='coerce')
        if df['Time'].isnull().any():
            raise ValueError("La columna 'Time' contiene valores nulos después de la conversión a datetime.")
        df.set_index('Time', inplace=True)
        for col in ['Open', 'High', 'Low', 'Close', 'VWAP', 'Volume', 'Count']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df.isnull().any().any():
            raise ValueError("Existen valores nulos después de la conversión de las columnas de datos.")
        return df
