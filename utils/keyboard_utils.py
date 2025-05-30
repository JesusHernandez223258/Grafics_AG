#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilidades para el teclado virtual y la edición de funciones
"""

import re
import numpy as np
from sympy import symbols, sympify, lambdify, SympifyError

def format_function_text(function_text):
    """
    Formatea el texto de una función para mejor visualización
    
    Args:
        function_text: Texto de la función
    
    Returns:
        str: Texto formateado
    """
    display_text = function_text.replace('*', '·')
    display_text = display_text.replace('pi', 'π')
    display_text = display_text.replace('/', '÷')
    display_text = display_text.replace('sqrt', '√')
    return display_text

def prepare_function_for_eval(function_text):
    """
    Prepara el texto de una función para evaluación
    
    Args:
        function_text: Texto de la función
    
    Returns:
        str: Texto preparado para evaluación
    """
    eval_text = function_text.replace('π', 'pi')
    eval_text = eval_text.replace('^', '**')
    eval_text = eval_text.replace('ln(', 'log(')
    return eval_text

def validate_function_syntax(function_text):
    """
    Valida la sintaxis de una función
    
    Args:
        function_text: Texto de la función
    
    Returns:
        tuple: (bool, str, función_compilada) donde:
            - bool: True si la función es válida, False en caso contrario
            - str: Mensaje de error o éxito
            - función_compilada: Función compilada o None
    """
    # Si está vacía
    if not function_text.strip():
        return False, "Función vacía", None
    
    try:
        # Preparar el texto para evaluación
        eval_text = prepare_function_for_eval(function_text)
        
        # Usar sympy para validar la expresión
        x = symbols('x')
        expr = sympify(eval_text)
        
        # Convertir a una función lambda de numpy para evaluación rápida
        compiled_function = lambdify(x, expr, ['numpy', {'ln': np.log, 'log': np.log10}])
        
        # Probar la función con varios valores
        test_values = [-10, -1, 0, 1, 10]
        for val in test_values:
            try:
                result = compiled_function(val)
                # Verificar si el resultado es válido
                if not np.isfinite(result) or np.isnan(result):
                    return False, f"La función produce valores no válidos para x={val}", None
            except Exception as e:
                return False, f"Error al evaluar x={val}: {str(e)}", None
        
        return True, "Función válida", compiled_function
                
    except SympifyError as e:
        return False, f"Error de sintaxis: {str(e)}", None
    except Exception as e:
        return False, f"Error: {str(e)}", None

def get_function_complexity(function_text):
    """
    Calcula la complejidad de una función basada en operadores y funciones
    
    Args:
        function_text: Texto de la función
    
    Returns:
        int: Valor de complejidad (mayor es más complejo)
    """
    complexity = 0
    
    # Contar operadores
    operators = ['+', '-', '*', '/', '^']
    for op in operators:
        complexity += function_text.count(op)
    
    # Contar funciones (más peso)
    functions = ['sin', 'cos', 'tan', 'exp', 'log', 'ln', 'sqrt', 'abs']
    for func in functions:
        complexity += function_text.count(func) * 2
    
    # Contar paréntesis anidados (mayor complejidad)
    max_depth = 0
    current_depth = 0
    for char in function_text:
        if char == '(':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ')':
            current_depth = max(0, current_depth - 1)
    
    complexity += max_depth * 3
    
    return complexity

def evaluate_function(compiled_function, x_value, is_minimizing=True):
    """
    Evalúa una función compilada en un valor dado
    
    Args:
        compiled_function: Función compilada
        x_value: Valor en el que evaluar
        is_minimizing: Si estamos minimizando o maximizando
    
    Returns:
        float: Resultado de la evaluación (adaptado para min/max)
    """
    try:
        result = compiled_function(x_value)
        
        # Si estamos minimizando, negamos el resultado
        if is_minimizing:
            return -result  # Negativo para minimización
        else:
            return result   # Positivo para maximización
    except Exception:
        return float('inf') if is_minimizing else float('-inf')