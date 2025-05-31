"""
Visualizador de Algoritmos Genéticos
-----------------------------------
Aplicación para visualizar el funcionamiento de algoritmos genéticos
en la resolución de problemas de optimización de funciones.
"""

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow  # Debes crear esta versión Qt de tu ventana principal

from manager.ga_manager import get_ga_instance, get_available_ga_names

SELECTED_GA_NAME = "example_ga"  # O "standard_ga" para probar el otro

def execute_specific_ga(params: dict, root_qt_window=None, algorithm_name: str = SELECTED_GA_NAME):
    """
    Ejecuta un AG específico y devuelve los resultados en el formato esperado por MainWindow.
    """
    print(f"Solicitando ejecución del AG: '{algorithm_name}'")
    print("Recibidos parámetros para el AG:", params)

    try:
        ga_instance = get_ga_instance(algorithm_name)
    except ValueError as e:
        QMessageBox.critical(root_qt_window, "Error de Configuración", f"No se pudo cargar el AG: {e}")
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
            progress_root_window=root_qt_window  # Qt parent para diálogos de progreso
        )
        return results
    except Exception as e:
        QMessageBox.critical(root_qt_window, "Error en AG", f"Falló la ejecución del AG '{algorithm_name}': {e}")
        print(f"Error ejecutando el AG '{algorithm_name}': {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    app = QApplication(sys.argv)
    try:
        with open("ui/style/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: style.qss not found. Using default styles.")

    print(f"Nombres de AGs disponibles: {get_available_ga_names()}")
    print(f"AG seleccionado para esta sesión: {SELECTED_GA_NAME}")

    if SELECTED_GA_NAME not in get_available_ga_names():
        print(f"Error: El AG '{SELECTED_GA_NAME}' no está registrado. Usando 'example_ga' por defecto.")
        actual_ga_to_use = "example_ga"
        if "example_ga" not in get_available_ga_names():
            QMessageBox.critical(None, "Error Crítico", "No hay ningún AG 'example_ga' registrado. La aplicación no puede continuar.")
            return
    else:
        actual_ga_to_use = SELECTED_GA_NAME

    main_window = MainWindow()  # Debe ser tu ventana principal basada en PySide6

    configured_ga_executor = lambda p, r: execute_specific_ga(p, r, algorithm_name=actual_ga_to_use)
    main_window.set_ga_executor(configured_ga_executor)

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()