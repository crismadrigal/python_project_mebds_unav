import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from services.kraken_service import KrakenService
from services.bollinger_service import BollingerBandsService
from utils.error_handler import handle_errors

# Configuración de la página
st.set_page_config(
    page_title="Análisis Financiero Kraken",
    page_icon="📈",
    layout="wide"
)

# Título y descripción
st.title("Análisis Financiero con Kraken API")
st.write("Esta aplicación permite visualizar gráficos de velas y Bandas de Bollinger para pares de divisas seleccionados de Kraken.")

# Inicializa el servicio de Kraken
kraken_service = KrakenService()

try:
    # Obtener todos los pares de divisas disponibles
    lista_pares = kraken_service.obtener_pares_kraken()

    if lista_pares:
        par_deseado = st.sidebar.selectbox("Selecciona el par de divisas:", lista_pares)

        periodo_bollinger = st.sidebar.slider("Período para Bandas de Bollinger:", min_value=5, max_value=30, value=10, step=1)

        fecha_inicio = st.sidebar.date_input("Fecha de inicio", pd.to_datetime("2024-10-25"))
        since_timestamp = int(pd.to_datetime(fecha_inicio).timestamp())

        intervalo = st.sidebar.selectbox(
            "Selecciona el intervalo (en minutos):",
            options=[1, 5, 15, 30, 60, 240, 1440],
            format_func=lambda x: f"{x} minuto{'s' if x > 1 else ''}" if x < 60 else f"{x//60} hora{'s' if x > 60 else ''}"
        )

        if st.sidebar.button("Obtener datos y generar gráfico"):
            # Control de errores al obtener datos
            try:
                df = kraken_service.obtener_datos_kraken(par_deseado, since=since_timestamp, interval=intervalo)

                if not df.empty:
                    # Inicializa el servicio de Bollinger con control de errores
                    try:
                        bollinger_service = BollingerBandsService(df)
                        df = bollinger_service.calcular_bandas_bollinger(period=periodo_bollinger)
                        df = bollinger_service.detectar_alertas()

                        fig = bollinger_service.generar_grafico_candlestick(df, par_deseado)
                        st.plotly_chart(fig)

                        st.write("Datos de cotización con alertas:")
                        st.dataframe(df)
                    except Exception as e:
                        st.error(f"Error al calcular Bandas de Bollinger o generar gráficos: {e}")
                else:
                    st.warning("No se encontraron datos para la fecha seleccionada o el intervalo especificado. Intenta con un intervalo más grande o una fecha más reciente.")
            except Exception as e:
                st.error(f"Error al obtener datos de Kraken: {e}")
    else:
        st.error("No se pudieron obtener los pares de divisas de Kraken. Revisa la conexión o las credenciales de la API.")
except Exception as e:
    st.error(f"Error al inicializar la aplicación: {e}")
