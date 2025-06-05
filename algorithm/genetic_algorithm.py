"""
Implementación del algoritmo genético de ejemplo, adaptado a la interfaz estándar,
con correcciones para:
  1) incluir 'objective_function_raw' en los resultados;
  2) lógica de emparejamiento, poda y mutación según las indicaciones:
     - Emparejamiento: cada individuo se empareja con otro aleatorio (puede ser sí mismo).
     - Poda: eliminar aleatoriamente individuos, siempre conservando al mejor.
     - Mutación: solo mutan individuos que no superen p_mutation_i (PMI). 
       Dentro de ellos, solo mutan genes que no superen p_mutation_g (PMG).
"""

import random
import numpy as np
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Dict, Any

from utils.math_functions import (
    objective_function,
    get_raw_function_value,
    binary_to_decimal,
    get_function_provider
)

class GeneticAlgorithm:
    """Clase que implementa el algoritmo genético de ejemplo"""

    def __init__(self):
        pass

    def create_individual(self, n_bits: int) -> List[int]:
        """Crea un individuo aleatorio (lista de bits)"""
        return [random.randint(0, 1) for _ in range(n_bits)]

    def crossover_three_points(
        self,
        parent1: List[int],
        parent2: List[int],
        prob_crossover: float
    ) -> Tuple[List[int], List[int]]:
        """
        Cruza dos padres con tres puntos aleatorios.
        Si random < prob_crossover, intercambia segmentos entre puntos.
        """
        child1, child2 = parent1.copy(), parent2.copy()
        if random.random() < prob_crossover and len(parent1) >= 4:
            # Elegir (hasta) 3 puntos de cruce únicos en [1, len-1)
            puntos = sorted(random.sample(range(1, len(parent1)), min(3, len(parent1)-1)))
            swap = False
            prev = 0
            for punto in puntos + [len(parent1)]:
                if swap:
                    child1[prev:punto] = parent2[prev:punto]
                    child2[prev:punto] = parent1[prev:punto]
                swap = not swap
                prev = punto
        return child1, child2

    def mutation_gene(
        self,
        individual: List[int],
        prob_mutation_gene: float
    ) -> List[int]:
        """
        Mutación a nivel de gen: para cada gen, con prob_mutation_gene, 
        cambiar 0→1 o 1→0.  
        (Esta es la mutación por gen: PMG).
        """
        mutated = individual.copy()
        for idx in range(len(mutated)):
            if random.random() < prob_mutation_gene:
                mutated[idx] = 1 - mutated[idx]
        return mutated

    def run(
        self,
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
        """
        Ejecuta el algoritmo genético completo, devolviendo:
          {
            'ga_results': {
                'best_individual': [...],
                'best_x': float,
                'best_fitness': float,
                'objective_function_raw': float,
                'x_min': ..., 'x_max': ..., 'n_bits': ...,
                'pop_size': ..., 'generations': ...,
                'prob_crossover': ..., 'prob_mutation_i': ...,
                'prob_mutation_g': ..., 'improvement': ...,
                'final_population': [...],
                'final_fitness': [...],
                'is_minimizing': ...,
                'function_text_for_report': str
            },
            'population_history': [...],       # poblaciones por generación (listas de individuos)
            'fitness_history': [...],          # fitness real de cada individuo por generación
            'best_fitness_history': [...]      # mejor fitness real por generación
          }
        """

        # --- 0. Obtener la función objetivo (texto y proveedor) ---
        current_function_provider = get_function_provider()
        function_text_used_by_ga = current_function_provider.function_text

        # --- 1. Calcular n_bits en base a (x_min, x_max, delta_x) ---
        if x_min == 0 and x_max == 31 and delta_x == 1.0:
            n_bits = 5
        elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0:
            rango = int(x_max - x_min) + 1
            n_bits = int(np.ceil(np.log2(rango))) if rango > 0 else 0
        else:
            divisiones = int(np.round((x_max - x_min) / delta_x)) if delta_x > 0 else 0
            n_bits = int(np.ceil(np.log2(divisiones + 1))) if divisiones >= 0 else 0

        if n_bits == 0 and ((x_max - x_min) > 0 or (x_min == x_max and delta_x > 0)):
            puntos_posibles = (int(np.round((x_max - x_min) / delta_x)) + 1) if delta_x > 0 else 1
            if puntos_posibles > 1:
                n_bits = max(1, n_bits)
            elif puntos_posibles == 1:
                if x_min == x_max:
                    n_bits = 0
                else:
                    n_bits = 1

        # --- 2. Inicialización de estructuras para historial ---
        population_history_data = []           # List[List[individuo_bits]]
        raw_fitness_history_data = []          # List[List[float]] (fitness real de cada individuo)
        best_raw_fitness_history_data = []     # List[float] (mejor fitness real por generación)

        # Creamos la población inicial (aleatoria)
        population = [self.create_individual(n_bits) for _ in range(pop_size)]

        # --- 2b. (opcional) Barra de progreso en Tkinter ---
        internal_progress_window = None
        local_progress_bar = None
        local_progress_label = None
        is_tk_parent = progress_root_window and (
            isinstance(progress_root_window, tk.Tk) or isinstance(progress_root_window, tk.Toplevel)
        )
        if is_tk_parent:
            try:
                internal_progress_window = tk.Toplevel(progress_root_window)
                internal_progress_window.title("Ejecutando AG (Ejemplo)...")
                internal_progress_window.geometry("400x120")
                internal_progress_window.configure(bg='#f0f0f0')
                modo = "Minimizando" if is_minimizing else "Maximizando"
                tk.Label(
                    internal_progress_window,
                    text=f"Ejecutando AG de Ejemplo... ({modo})",
                    font=("Arial", 12),
                    bg='#f0f0f0'
                ).pack(pady=20)
                local_progress_bar = ttk.Progressbar(
                    internal_progress_window,
                    mode='determinate',
                    maximum=max_generations
                )
                local_progress_bar.pack(pady=10, padx=20, fill='x')
                local_progress_label = tk.Label(
                    internal_progress_window,
                    text="",
                    font=("Arial", 10),
                    bg='#f0f0f0'
                )
                local_progress_label.pack()
                internal_progress_window.update()
            except tk.TclError:
                internal_progress_window = None

        # --- 3. Bucle principal de generaciones ---
        for generation in range(max_generations):
            # 3.1 Evaluar cada individuo: obtener fitness interno (para la lógica del AG)
            #     y fitness real (para historiales y reporte final)
            internal_fitness_scores = []
            current_gen_raw_fitness = []
            for indiv in population:
                x_val = binary_to_decimal(indiv, x_min, x_max, n_bits)
                fit_interna = objective_function(x_val, is_minimizing)   # fitness “interno” según si minimiza/maximiza
                fit_cruda   = get_raw_function_value(x_val)               # fitness real (sin signo)
                internal_fitness_scores.append(fit_interna)
                current_gen_raw_fitness.append(fit_cruda)

            # 3.2 Guardar historiales de fitness real
            if is_minimizing:
                mejor_raw_esta_gen = min(current_gen_raw_fitness) if current_gen_raw_fitness else np.inf
            else:
                mejor_raw_esta_gen = max(current_gen_raw_fitness) if current_gen_raw_fitness else -np.inf

            best_raw_fitness_history_data.append(mejor_raw_esta_gen)
            raw_fitness_history_data.append(current_gen_raw_fitness.copy())
            population_history_data.append([ind.copy() for ind in population])

            # 3.3 Actualizar barra de progreso (si aplica)
            if internal_progress_window and local_progress_bar and local_progress_label:
                local_progress_bar.config(value=generation + 1)
                local_progress_label.config(text=f"Generación {generation + 1}/{max_generations}")
                internal_progress_window.update()

            # 3.4 SELECCIÓN + PODA:
            #     - Primero, hallamos el fitness interno de cada individuo.
            #     - Identificamos al “mejor” (según fitness interno).
            #     - Después, para simular “poda aleatoria conservando al mejor”:
            #         * Siempre mantenemos al mejor (por fitness real).
            #         * De los demás, eliminamos aleatoriamente hasta reducir al 50% de la población actual.
            #       (ejemplo: pop_size=10 → queremos 5 individuos para la siguiente fase)
            #
            #     NOTA: el enunciado pide “eliminar aleatoriamente, conservando al mejor”.
            #
            # Primer paso: encontrar índice del mejor individuo (por fitness real)
            if current_gen_raw_fitness:
                if is_minimizing:
                    idx_mejor = current_gen_raw_fitness.index(min(current_gen_raw_fitness))
                else:
                    idx_mejor = current_gen_raw_fitness.index(max(current_gen_raw_fitness))
            else:
                idx_mejor = None

            # Crear lista de pareja candidata: todos los índices menos el del mejor
            indices_todos = list(range(len(population)))
            if idx_mejor is not None:
                indice_mejor = idx_mejor
            else:
                indice_mejor = None

            # Ahora, escogemos aleatoriamente la mitad de los demás para eliminar:
            # queremos conservar exactamente pop_size//2 individuos (incluido el mejor).
            num_a_conservar = max(1, pop_size // 2)  # al menos 1 (que será el mejor).
            conservados = []
            if indice_mejor is not None:
                conservados.append(indice_mejor)

            candidatos_eliminar = [i for i in indices_todos if i != indice_mejor]
            # Aleatoriamente escogemos (num_a_conservar-1) índices de los candidatos para conservar
            if num_a_conservar - 1 > 0 and candidatos_eliminar:
                seleccionados = random.sample(
                    candidatos_eliminar,
                    min(len(candidatos_eliminar), num_a_conservar - 1)
                )
                conservados += seleccionados

            # Reconstruir población “podada”: solo los individuos en “conservados”
            nueva_poblacion_parte = [population[i] for i in conservados]

            # 3.5 EMPAREJAMIENTO + CRUZA + MUTACIÓN:
            #
            # Ahora, cada individuo de `nueva_poblacion_parte` genera una pareja “aleatoria”:
            #   * Puede emparejarse incluso consigo mismo.
            #   * Repetimos hasta reconstruir nuevamente pop_size individuos.
            #
            # Después, hacemos crossover de tres puntos y mutación (si cumple PMI → PMG).

            new_population = []
            # Creamos lista “posibles padres” igual a la población podada
            posibles_padres = nueva_poblacion_parte.copy()
            # Mientras no hayamos generado pop_size hijos (nueva generación):
            while len(new_population) < pop_size:
                # 1) Elegir un padre_i (en orden cíclico) y parearlo con un padre_j aleatorio:
                padre_i = posibles_padres[len(new_population) % len(posibles_padres)]
                padre_j = random.choice(posibles_padres)  # podría ser el mismo

                # 2) Cruza tres puntos:
                hijo1, hijo2 = self.crossover_three_points(padre_i, padre_j, prob_crossover)

                # 3) MUTACIÓN:
                #    - Primero: ver si el individuo cumple PMI (prob_mutation_i).
                #    - Si cumple, aplicar “mutación_gen” con prob_mutation_g (PMG).
                if random.random() < prob_mutation_i:
                    hijo1 = self.mutation_gene(hijo1, prob_mutation_g)
                if random.random() < prob_mutation_i:
                    hijo2 = self.mutation_gene(hijo2, prob_mutation_g)

                new_population.append(hijo1)
                if len(new_population) < pop_size:
                    new_population.append(hijo2)

            # Actualizar población para la siguiente generación
            population = new_population[:pop_size]

        # Fin del bucle de generaciones
        if internal_progress_window:
            internal_progress_window.destroy()

        # --- 4. Evaluación final de la población y mejores resultados ---
        final_internal_fitness = []
        final_raw_fitness_report = []
        for indiv in population:
            x_val = binary_to_decimal(indiv, x_min, x_max, n_bits)
            final_internal_fitness.append(objective_function(x_val, is_minimizing))
            final_raw_fitness_report.append(get_raw_function_value(x_val))

        # Determinar el mejor individuo final (según fitness REAL)
        if final_raw_fitness_report:
            if is_minimizing:
                idx_mejor_final = final_raw_fitness_report.index(min(final_raw_fitness_report))
            else:
                idx_mejor_final = final_raw_fitness_report.index(max(final_raw_fitness_report))
        else:
            idx_mejor_final = None

        if idx_mejor_final is not None:
            best_individual_final = population[idx_mejor_final]
            best_x_final         = binary_to_decimal(best_individual_final, x_min, x_max, n_bits)
            best_raw_fitness_final = get_raw_function_value(best_x_final)
        else:
            # En caso extremo, generamos un individuo al azar
            best_individual_final = self.create_individual(n_bits)
            best_x_final = binary_to_decimal(best_individual_final, x_min, x_max, n_bits)
            best_raw_fitness_final = get_raw_function_value(best_x_final)

        # Calcular mejora sobre los fitness reales (de la primera generación a la última)
        improvement = 0.0
        if best_raw_fitness_history_data:
            inicial = best_raw_fitness_history_data[0]
            if is_minimizing:
                improvement = inicial - best_raw_fitness_final
            else:
                improvement = best_raw_fitness_final - inicial

        ga_results_dict = {
            'best_individual': best_individual_final,
            'best_x': best_x_final,
            'best_fitness': best_raw_fitness_final,         # fitness real en best_x
            'objective_function_raw': best_raw_fitness_final, # <--- aquí incluimos la clave
            'x_min': x_min,
            'x_max': x_max,
            'n_bits': n_bits,
            'pop_size': pop_size,
            'generations': max_generations,
            'prob_crossover': prob_crossover,
            'prob_mutation_i': prob_mutation_i,
            'prob_mutation_g': prob_mutation_g,
            'improvement': improvement,
            'final_population': [ind.copy() for ind in population],
            'final_fitness': final_raw_fitness_report,
            'is_minimizing': is_minimizing,
            'function_text_for_report': function_text_used_by_ga
        }

        return {
            'ga_results': ga_results_dict,
            'population_history': population_history_data,
            'fitness_history': raw_fitness_history_data,
            'best_fitness_history': best_raw_fitness_history_data
        }
