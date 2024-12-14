import pytest
import pandas as pd
from utils.error_handler import handle_errors

@handle_errors
def funcion_con_error():
    """Función que provoca una excepción."""
    raise ValueError("Error de prueba")

@handle_errors
def funcion_exitosa():
    """Función que se ejecuta con éxito."""
    return "éxito"

@handle_errors
def funcion_dataframe():
    """Función que devuelve un DataFrame."""
    return pd.DataFrame({'A': [1, 2, 3]})

def test_handle_errors_funcion_con_error():
    """Prueba el control de errores con una función que genera excepción."""
    resultado = funcion_con_error()
    
    # Verifica que el resultado sea un DataFrame vacío
    assert resultado.empty, "El decorador debería devolver un DataFrame vacío en caso de error"

def test_handle_errors_funcion_exitosa():
    """Prueba el control de errores con una función que no genera excepción."""
    resultado = funcion_exitosa()
    assert resultado == "éxito"

def test_handle_errors_funcion_dataframe():
    """Prueba el control de errores con una función que devuelve un DataFrame."""
    df = funcion_dataframe()
    assert not df.empty
    assert 'A' in df.columns
