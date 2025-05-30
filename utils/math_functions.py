#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones matemáticas para el algoritmo genético
"""

import numpy as np
from typing import List

# Variable global para almacenar la instancia del proveedor de funciones
_function_provider = None

def set_function_provider(provider):
    """Establece el proveedor de funciones a usar globalmente"""
    global _function_provider
    _function_provider = provider

def get_function_provider():
    """Obtiene el proveedor de funciones actual"""
    global _function_provider
    # Si no existe, usar la función predeterminada
    if _function_provider is None:
        from ui.function_editor import CustomFunctionProvider  # Importación local
        _function_provider = CustomFunctionProvider()
        # CustomFunctionProvider ahora intenta compilar su función predeterminada en __init__
    return _function_provider

def objective_function(x: float, is_minimizing: bool) -> float:
    """Función objetivo adaptada según modo de optimización (para uso del AG)"""
    provider = get_function_provider()
    return provider.evaluate(x, is_minimizing)

def get_raw_function_value(x: float) -> float:
    """Obtiene el valor real de la función (para reportes y visualización)"""
    provider = get_function_provider()
    return provider.get_raw_function_value(x)

def binary_to_decimal(binary: List[int], x_min: float, x_max: float, n_bits: int) -> float:
    """Convierte un individuo binario a valor decimal"""
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + bit
    
    max_decimal = 2**n_bits - 1
    if max_decimal == 0:  # Evitar división por cero si n_bits es 0 o hay un error
        return x_min
    x = x_min + (decimal / max_decimal) * (x_max - x_min)
    return x

def decimal_to_binary(decimal: int, n_bits: int) -> List[int]:
    """Convierte un valor decimal a una representación binaria"""
    binary = []
    if n_bits <= 0:
        return []
    for _ in range(n_bits):
        binary.insert(0, decimal % 2)
        decimal //= 2
    return binary