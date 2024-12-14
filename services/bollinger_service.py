import pandas as pd
import plotly.graph_objs as go
from utils.error_handler import handle_errors

class BollingerBandsService:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El parámetro 'df' debe ser un DataFrame de pandas.")
        if df.empty:
            raise ValueError("El DataFrame proporcionado está vacío.")
        self.df = df

    @handle_errors
    def calcular_bandas_bollinger(self, period=10):
        if 'Close' not in self.df.columns:
            raise KeyError("El DataFrame no contiene la columna 'Close' necesaria para el cálculo.")
        self.df['Close'] = pd.to_numeric(self.df['Close'], errors='coerce')
        if self.df['Close'].isnull().any():
            raise ValueError("La columna 'Close' contiene valores nulos o no numéricos.")
        self.df['MA'] = self.df['Close'].rolling(window=period).mean()
        self.df['STD'] = self.df['Close'].rolling(window=period).std()
        self.df['Upper Band'] = self.df['MA'] + (2 * self.df['STD'])
        self.df['Lower Band'] = self.df['MA'] - (2 * self.df['STD'])
        return self.df

    @handle_errors
    def detectar_alertas(self):
        if 'Close' not in self.df.columns or 'Lower Band' not in self.df.columns or 'Upper Band' not in self.df.columns:
            raise KeyError("El DataFrame no contiene las columnas necesarias.")
        self.df['Signal'] = self.df.apply(
            lambda row: 'Compra' if row['Close'] <= row['Lower Band'] 
                        else 'Venta' if row['Close'] >= row['Upper Band'] 
                        else None, axis=1
        )
        return self.df

    @handle_errors
    def generar_grafico_candlestick(self, df, par_deseado):
        if df.empty:
            raise ValueError("El DataFrame proporcionado está vacío.")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Cotización'
        ))
        fig.update_layout(
            title=f'Análisis de {par_deseado}',
            xaxis_title='Fecha',
            yaxis_title='Precio',
            xaxis_rangeslider_visible=False
        )
        return fig
