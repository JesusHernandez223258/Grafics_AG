# ===== ./algorithm/genetic_algorithm.py =====

"""
Implementación de un Algoritmo Genético Estándar (Ejemplo 2)
"""

import random
import numpy as np
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Dict, Any

from utils.math_functions import objective_function, get_raw_function_value, binary_to_decimal, get_function_provider

class GeneticAlgorithm:  # Mismo nombre de clase, pero en diferente módulo
    """Clase que implementa un algoritmo genético estándar"""

    def __init__(self):
        pass

    def run(self,
            x_min: float,
            x_max: float,
            delta_x: float,
            pop_size: int,
            max_generations: int,
            prob_crossover: float,
            prob_mutation_i: float,
            prob_mutation_g: float,
            is_minimizing: bool,
            progress_root_window: tk.Tk = None
            ) -> Dict[str, Any]:

        current_function_provider = get_function_provider()
        function_text_used_by_ga = current_function_provider.function_text

        print(f"--- Ejecutando Algoritmo Genético 'Standard' (desde algorithm/genetic_algorithm.py) ---")
        print(f"--- Función objetivo: {function_text_used_by_ga} ---")

        if x_min == 0 and x_max == 31 and delta_x == 1.0:
            n_bits = 5
        elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0:
            range_size = int(x_max - x_min) + 1
            n_bits = int(np.ceil(np.log2(range_size)))
        else:
            num_divisions = int((x_max - x_min) / delta_x)
            n_bits = int(np.ceil(np.log2(num_divisions + 1)))

        # Para este ejemplo, simplemente retornamos una estructura dummy
        dummy_best_individual = [random.randint(0, 1) for _ in range(n_bits)]
        dummy_population = [[random.randint(0, 1) for _ in range(n_bits)] for _ in range(pop_size)]
        
        best_x_val = binary_to_decimal(dummy_best_individual, x_min, x_max, n_bits)
        best_fitness_val = get_raw_function_value(best_x_val)

        final_fitness_vals = [get_raw_function_value(binary_to_decimal(ind, x_min, x_max, n_bits)) for ind in dummy_population]
        
        # Simular historial (muy simplificado)
        population_history_dummy = [dummy_population for _ in range(max_generations)]
        fitness_history_dummy = [final_fitness_vals for _ in range(max_generations)]
        best_fitness_history_dummy = [best_fitness_val for _ in range(max_generations)]

        if progress_root_window:
            progress_window = tk.Toplevel(progress_root_window)
            progress_window.title("Ejecutando AG (Standard)...")
            progress_window.geometry("400x120")
            tk.Label(progress_window, text=f"Simulando ejecución de AG Standard...").pack(pady=20)
            temp_progress_bar = ttk.Progressbar(progress_window, mode='determinate', maximum=max_generations, value=max_generations)
            temp_progress_bar.pack(pady=10, padx=20, fill='x')
            progress_window.update()
            progress_window.after(1000, progress_window.destroy)  # Cierra después de 1 seg

        results = {
            'ga_results': {
                'best_individual': dummy_best_individual,
                'best_x': best_x_val,
                'best_fitness': best_fitness_val,
                'x_min': x_min, 'x_max': x_max, 'n_bits': n_bits,
                'pop_size': pop_size, 'generations': max_generations,
                'prob_crossover': prob_crossover,
                'prob_mutation_i': prob_mutation_i, 'prob_mutation_g': prob_mutation_g,
                'improvement': 0.1,  # Dummy
                'final_population': dummy_population,
                'final_fitness': final_fitness_vals,
                'is_minimizing': is_minimizing,
                'function_text_for_report': function_text_used_by_ga
            },
            'population_history': population_history_dummy,
            'fitness_history': fitness_history_dummy,
            'best_fitness_history': best_fitness_history_dummy
        }
        print(f"--- AG 'Standard' finalizado. Mejor X: {best_x_val}, Fitness: {best_fitness_val} ---")
        return results