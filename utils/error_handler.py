import streamlit as st
import functools
import pandas as pd

def handle_errors(func):
    """Decorador para manejar errores y mostrar mensaje de error en Streamlit."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Ejecuta la función original
        except Exception as e:
            # Muestra el error en Streamlit
            st.error(f"Error en la función '{func.__name__}': {e}")
            # Devuelve un resultado seguro según el contexto
            return None if func.__name__ == 'obtener_pares_kraken' else pd.DataFrame()
    return wrapper