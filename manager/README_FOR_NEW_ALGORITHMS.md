# Guía para Integrar Nuevos Algoritmos Genéticos

Este documento describe la interfaz y los requisitos que debe cumplir cualquier nueva implementación de un Algoritmo Genético (AG) para ser compatible con el sistema visualizador. El archivo `manager/ga_manager.py` es el encargado de gestionar estos algoritmos.

## Estructura de Archivos

1.  Cree una nueva carpeta dedicada para su algoritmo dentro del directorio principal del proyecto (al mismo nivel que `example_ga/`, `ui/`, etc.). Por ejemplo: `my_custom_ga/`.
2.  Dentro de esta carpeta, incluya su archivo Python con la implementación del AG, por ejemplo, `my_custom_ga_logic.py`.
3.  Asegúrese de tener un archivo `__init__.py` en su carpeta para que Python la reconozca como un paquete.

## Interfaz de la Clase del AG

Su clase de AG debe cumplir con la siguiente estructura:

```python
# En my_custom_ga/my_custom_ga_logic.py

import random
import numpy as np
import tkinter as tk # Opcional, para progreso
from tkinter import ttk # Opcional, para progreso
from typing import List, Tuple, Dict, Any

# CRUCIAL: Importar estas funciones para interactuar con la función objetivo definida en la UI
from utils.math_functions import objective_function, get_raw_function_value, binary_to_decimal, get_function_provider

class MyCustomGeneticAlgorithm:
    def __init__(self):
        """
        Constructor de su AG. Puede inicializar parámetros internos aquí si es necesario.
        """
        pass

    def run(self,
            x_min: float,
            x_max: float,
            delta_x: float,
            pop_size: int,
            max_generations: int,
            prob_crossover: float,
            prob_mutation_i: float,  # Probabilidad de mutar un individuo
            prob_mutation_g: float,  # Probabilidad de mutar un gen (si aplica a su mutación)
            is_minimizing: bool,
            progress_root_window: tk.Tk = None  # Opcional: para mostrar progreso
            ) -> Dict[str, Any]:
        """
        Punto de entrada principal para ejecutar el algoritmo genético.

        Args:
            x_min (float): Límite inferior del intervalo de búsqueda para x.
            x_max (float): Límite superior del intervalo de búsqueda para x.
            delta_x (float): Precisión deseada para x. Usar para calcular n_bits.
            pop_size (int): Tamaño de la población.
            max_generations (int): Número máximo de generaciones.
            prob_crossover (float): Probabilidad de cruzamiento.
            prob_mutation_i (float): Probabilidad de mutación por individuo.
            prob_mutation_g (float): Probabilidad de mutación por gen (o parámetro similar para su operador).
            is_minimizing (bool): True si se busca minimizar la función objetivo, False si se busca maximizar.
                                  La función `objective_function(x, is_minimizing)` ya maneja la inversión
                                  del valor si es necesario para la lógica de minimización/maximización interna del AG.
                                  Su AG debería, por lo general, intentar maximizar el valor devuelto por `objective_function`.
            progress_root_window (tk.Tk, optional): Ventana raíz de Tkinter para crear diálogos de progreso.

        Returns:
            Dict[str, Any]: Un diccionario con los resultados del AG. Debe tener la siguiente estructura:
            {
                'ga_results': {
                    'best_individual': List[int],  # El mejor individuo (lista de bits)
                    'best_x': float,              # Valor 'x' decodificado del mejor individuo
                    'best_fitness': float,        # Fitness REAL (valor crudo de f(x)) del mejor individuo
                    'x_min': float,               # x_min usado
                    'x_max': float,               # x_max usado
                    'n_bits': int,                # Número de bits calculado y usado
                    'pop_size': int,              # pop_size usado
                    'generations': int,           # max_generations usado (o las reales si hubo corte temprano)
                    'prob_crossover': float,      # prob_crossover usado
                    'prob_mutation_i': float,     # prob_mutation_i usado
                    'prob_mutation_g': float,     # prob_mutation_g usado
                    'improvement': float,         # Mejora total (fitness_final_real - fitness_inicial_real o viceversa)
                    'final_population': List[List[int]], # Población final (lista de individuos)
                    'final_fitness': List[float], # Lista de fitness REALES de la población final
                    'is_minimizing': bool,        # is_minimizing usado
                    'function_text_for_report': str # TEXTO de la función objetivo que se utilizó.
                                                     # Obtenerla de get_function_provider().function_text
                },
                'population_history': List[List[List[int]]], # Historial de poblaciones por generación
                                                              # (lista de generaciones, cada una es una lista de individuos)
                'fitness_history': List[List[float]],    # Historial de fitness REALES de cada individuo por generación
                                                              # (lista de generaciones, cada una es una lista de fitness)
                'best_fitness_history': List[float]      # Historial del MEJOR fitness REAL por generación
            }
        """

        # 0. OBTENER LA FUNCIÓN OBJETIVO ACTUAL DEL PROVEEDOR GLOBAL
        current_function_provider = get_function_provider()
        function_text_used_by_ga = current_function_provider.function_text
        # Esta `function_text_used_by_ga` DEBE ser devuelta en 'ga_results['function_text_for_report']'

        # 1. CÁLCULO DE n_bits (basado en x_min, x_max, delta_x)
        #    (Puede usar la misma lógica que en example_ga/genetic_algorithm.py)
        if x_min == 0 and x_max == 31 and delta_x == 1.0: # Caso especial simplificado
             n_bits = 5
        elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0: # Otro caso para rangos enteros
             range_size = int(x_max - x_min) + 1
             n_bits = int(np.ceil(np.log2(range_size)))
        else:
             num_divisions = int((x_max - x_min) / delta_x)
             n_bits = int(np.ceil(np.log2(num_divisions + 1)))


        # 2. INICIALIZACIÓN
        #    - Crear población inicial.
        #    - Inicializar listas para `population_history`, `fitness_history`, `best_fitness_history`.

        # 3. BUCLE DE GENERACIONES
        #    - Para cada generación:
        #        - Evaluar la población:
        #            - Para cada individuo:
        #                - Decodificar a `x_real` usando `binary_to_decimal(individuo, x_min, x_max, n_bits)`.
        #                - Obtener fitness para la lógica del AG: `internal_fitness = objective_function(x_real, is_minimizing)`.
        #                  Su AG generalmente intentará MAXIMIZAR este `internal_fitness`.
        #                - Obtener fitness real para historial/reporte: `raw_fitness = get_raw_function_value(x_real)`.
        #        - Guardar en `population_history` la población actual.
        #        - Guardar en `fitness_history` la lista de `raw_fitness` de la población actual.
        #        - Guardar en `best_fitness_history` el mejor `raw_fitness` de la generación actual.
        #        - Aplicar selección, cruzamiento, mutación para crear la nueva población.
        #        - Actualizar barra de progreso (opcional, si `progress_root_window` se proporciona).

        # 4. POST-PROCESAMIENTO
        #    - Determinar el mejor individuo de la población final.
        #    - Calcular `best_x`, `best_fitness` (real).
        #    - Calcular `improvement`.
        #    - Ensamblar el diccionario de resultados como se especificó arriba.
        #      Asegúrese de que 'ga_results' incluye 'function_text_for_report': function_text_used_by_ga

        # Ejemplo de retorno (debe ser completado con datos reales):
        # dummy_best_individual = [0] * n_bits
        # dummy_population = [dummy_best_individual] * pop_size
        # dummy_raw_fitness_list = [0.0] * pop_size

        # results = {
        #     'ga_results': {
        #         'best_individual': dummy_best_individual,
        #         'best_x': x_min,
        #         'best_fitness': 0.0, # Usar get_raw_function_value() para el mejor
        #         'x_min': x_min, 'x_max': x_max, 'n_bits': n_bits,
        #         'pop_size': pop_size, 'generations': max_generations,
        #         'prob_crossover': prob_crossover,
        #         'prob_mutation_i': prob_mutation_i, 'prob_mutation_g': prob_mutation_g,
        #         'improvement': 0.0,
        #         'final_population': dummy_population,
        #         'final_fitness': dummy_raw_fitness_list,
        #         'is_minimizing': is_minimizing,
        #         'function_text_for_report': function_text_used_by_ga
        #     },
        #     'population_history': [dummy_population] * max_generations,
        #     'fitness_history': [dummy_raw_fitness_list] * max_generations,
        #     'best_fitness_history': [0.0] * max_generations
        # }
        # return results
        raise NotImplementedError("El método run debe ser implementado por la subclase.")

    # Puede añadir métodos auxiliares aquí (crear_individuo, cruzamiento, mutación, etc.)
    # como en example_ga/genetic_algorithm.py