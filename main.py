"""
Visualizador de Algoritmos Genéticos
-----------------------------------
Aplicación para visualizar el funcionamiento de algoritmos genéticos
en la resolución de problemas de optimización de funciones.
"""
import tkinter as tk
from tkinter import ttk, messagebox  # Importar messagebox aquí
from ui.main_window import MainWindow
# from example_ga.genetic_algorithm import GeneticAlgorithm # Ya no se importa directamente aquí

# Importar el gestor de AGs
from manager.ga_manager import get_ga_instance, get_available_ga_names

# Variable global para seleccionar el AG a usar.
# Esto podría venir de una configuración, un argumento de línea de comandos, o una selección en la GUI en el futuro.
SELECTED_GA_NAME = "example_ga"  # O "standard_ga" para probar el otro

def execute_specific_ga(params: dict, root_tk_window=None, algorithm_name: str = SELECTED_GA_NAME):
    """
    Esta función ejecuta un AG específico y devuelve los resultados
    en el formato esperado por MainWindow.

    Args:
        params (dict): Diccionario con los parámetros de configuración de la GUI.
                       Debe contener: 'interval_a', 'interval_b', 'delta_x',
                       'pop_size', 'num_generations', 'prob_crossover',
                       'prob_mutation_i', 'prob_mutation_g', 'is_minimizing'.
        root_tk_window (tk.Tk, optional): Ventana raíz de Tkinter, por si el AG
                                         necesita mostrar diálogos de progreso.
        algorithm_name (str): Nombre del algoritmo a ejecutar, registrado en ga_manager.

    Returns:
        dict: Un diccionario con los resultados del AG, con las claves:
              'ga_results', 'population_history', 'fitness_history', 'best_fitness_history'.
              Retorna None si la ejecución falla.
    """
    print(f"Solicitando ejecución del AG: '{algorithm_name}'")
    print("Recibidos parámetros para el AG:", params)

    try:
        # Obtener una instancia del AG seleccionado desde el manager
        ga_instance = get_ga_instance(algorithm_name)
    except ValueError as e:
        tk.messagebox.showerror("Error de Configuración", f"No se pudo cargar el AG: {e}")
        print(f"Error cargando el AG: {e}")
        return None

    try:
        results = ga_instance.run(
            x_min=params['interval_a'],
            x_max=params['interval_b'],
            delta_x=params['delta_x'],
            pop_size=params['pop_size'],
            max_generations=params['num_generations'],
            prob_crossover=params['prob_crossover'],
            prob_mutation_i=params['prob_mutation_i'],
            prob_mutation_g=params['prob_mutation_g'],
            is_minimizing=params['is_minimizing'],
            progress_root_window=root_tk_window  # Pasar la ventana raíz para el progreso
        )
        return results
    except Exception as e:
        tk.messagebox.showerror("Error en AG", f"Falló la ejecución del AG '{algorithm_name}': {e}")
        print(f"Error ejecutando el AG '{algorithm_name}': {e}")
        import traceback
        traceback.print_exc()  # Para más detalles en la consola
        return None

def main():
    """Punto de entrada principal de la aplicación"""
    
    # Aquí podrías eventualmente tener una lógica para seleccionar SELECTED_GA_NAME
    # Por ejemplo, desde la interfaz de usuario o argumentos de línea de comandos.
    # Por ahora, está hardcodeado arriba.
    print(f"Nombres de AGs disponibles: {get_available_ga_names()}")
    print(f"AG seleccionado para esta sesión: {SELECTED_GA_NAME}")

    if SELECTED_GA_NAME not in get_available_ga_names():
        print(f"Error: El AG '{SELECTED_GA_NAME}' no está registrado. Usando 'example_ga' por defecto.")
        actual_ga_to_use = "example_ga"
        if "example_ga" not in get_available_ga_names():  # Fallback extremo
            messagebox.showerror("Error Crítico", "No hay ningún AG 'example_ga' registrado. La aplicación no puede continuar.")
            return
    else:
        actual_ga_to_use = SELECTED_GA_NAME

    app = MainWindow()
    
    # Creamos una función lambda para que el executor tenga el nombre del AG fijado.
    # La función que espera MainWindow no toma `algorithm_name` directamente.
    configured_ga_executor = lambda p, r: execute_specific_ga(p, r, algorithm_name=actual_ga_to_use)
    
    app.set_ga_executor(configured_ga_executor)
    app.run()

if __name__ == "__main__":
    main()