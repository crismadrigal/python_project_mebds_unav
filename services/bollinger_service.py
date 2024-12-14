import pandas as pd
import plotly.graph_objs as go
from utils.error_handler import handle_errors  # Asumiendo que el decorador está en utils/error_handler.py

class BollingerBandsService:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El parámetro 'df' debe ser un DataFrame de pandas.")
        if df.empty:
            raise ValueError("El DataFrame proporcionado está vacío.")
        self.df = df

    @handle_errors
    def calcular_bandas_bollinger(self, period=10):
        """Calcula las Bandas de Bollinger y añade las columnas al DataFrame."""
        if 'Close' not in self.df.columns:
            raise KeyError("El DataFrame no contiene la columna 'Close' necesaria para el cálculo.")
        self.df['MA'] = self.df['Close'].rolling(window=period).mean()
        self.df['STD'] = self.df['Close'].rolling(window=period).std()
        self.df['Upper Band'] = self.df['MA'] + (2 * self.df['STD'])
        self.df['Lower Band'] = self.df['MA'] - (2 * self.df['STD'])
        return self.df

    @handle_errors
    def detectar_alertas(self):
        """Detecta señales de compra y venta."""
        if 'Close' not in self.df.columns or 'Lower Band' not in self.df.columns or 'Upper Band' not in self.df.columns:
            raise KeyError("El DataFrame no contiene las columnas necesarias ('Close', 'Lower Band', 'Upper Band') para detectar alertas.")
        self.df['Signal'] = self.df.apply(
            lambda row: 'Compra' if row['Close'] <= row['Lower Band'] 
                        else 'Venta' if row['Close'] >= row['Upper Band'] 
                        else None, axis=1
        )
        return self.df

    @handle_errors
    def generar_grafico_candlestick(self, df, par_deseado):
        """Genera el gráfico de velas japonesas con las Bandas de Bollinger y señales."""
        if df.empty:
            raise ValueError("El DataFrame proporcionado está vacío. No se puede generar el gráfico.")
        if any(col not in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Upper Band', 'Lower Band', 'Signal', 'MA']):
            raise KeyError("El DataFrame no contiene las columnas necesarias para generar el gráfico.")

        fig = go.Figure()

        # Gráfico de velas japonesas
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Cotización'
        ))

        # Sombreado de la zona entre la Banda Superior y la Banda Inferior
        fig.add_trace(go.Scatter(
            x=pd.concat([pd.Series(df.index), pd.Series(df.index[::-1])]),  # Solución al error
            y=pd.concat([df['Upper Band'], df['Lower Band'][::-1]]), 
            fill='toself', 
            fillcolor='rgba(128, 128, 128, 0.2)', 
            line=dict(color='rgba(255,255,255,0)'), 
            name='Zona de Bandas'
        ))

        # Banda Superior en verde
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['Upper Band'], 
            name='Banda Superior', 
            mode='lines', 
            line=dict(color='green')
        ))

        # Banda Inferior
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['Lower Band'], 
            name='Banda Inferior', 
            mode='lines', 
            line=dict(color='red')
        ))

        # Media Móvil en azul
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['MA'], 
            name='Media Móvil', 
            mode='lines', 
            line=dict(color='blue', dash='dash')
        ))

        # Señales de compra
        buy_signals = df[df['Signal'] == 'Compra']
        fig.add_trace(go.Scatter(
            x=buy_signals.index, 
            y=buy_signals['Close'], 
            mode='markers', 
            marker=dict(color='green', symbol='triangle-up', size=10), 
            name='Señal de Compra'
        ))

        # Señales de venta
        sell_signals = df[df['Signal'] == 'Venta']
        fig.add_trace(go.Scatter(
            x=sell_signals.index, 
            y=sell_signals['Close'], 
            mode='markers', 
            marker=dict(color='red', symbol='triangle-down', size=10), 
            name='Señal de Venta'
        ))

        # Configuración del diseño del gráfico
        fig.update_layout(
            title=f'Análisis de {par_deseado}',
            xaxis_title='Fecha',
            yaxis_title='Precio',
            template='plotly_white',
            xaxis_rangeslider_visible=False
        )

        return fig
