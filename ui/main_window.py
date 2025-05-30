# ===== ./ui/main_window.py =====

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ventana principal de la aplicación - Visualizador de Resultados de AG
"""

import tkinter as tk
from tkinter import messagebox

from ui.config_panel import ConfigPanel
from ui.visualization_panel import VisualizationPanel
from utils.export import ReportGenerator, AnimationGenerator
from utils.math_functions import set_function_provider # Para actualizar el provider de la UI
from ui.function_editor import CustomFunctionProvider # Para instanciar/actualizar el provider

class MainWindow:
    """Clase principal que maneja la ventana y coordina los componentes"""
    
    def __init__(self):
        """Inicializa la ventana principal y sus componentes"""
        self.root = tk.Tk()
        self.root.title("Algoritmo Genético - Visualizador de Resultados")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')

        self.ga_results = None
        self.population_history = []
        self.fitness_history = []
        self.best_fitness_history = []

        # El AG de ejemplo ya no se instancia aquí directamente
        # self.example_ga = GeneticAlgorithm() # ELIMINAR O COMENTAR
        self.report_generator = ReportGenerator()
        self.animation_generator = AnimationGenerator()
        self.ui_function_provider = CustomFunctionProvider()
        set_function_provider(self.ui_function_provider)
        
        self.ga_executor = None # Se establecerá con set_ga_executor

        self.create_interface()

    def create_interface(self):
        """Crea la interfaz dividida en dos paneles"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_frame, bg='white', width=420, relief='raised', bd=2)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Pasamos el ui_function_provider al config_panel
        self.config_panel = ConfigPanel(left_panel, self, self.ui_function_provider)
        self.visualization_panel = VisualizationPanel(right_panel, self)
        
    def run_example_algorithm(self, params):
        """Ejecuta el algoritmo genético configurado con los parámetros proporcionados"""
        if not self.ga_executor:
            messagebox.showerror("Error", "No se ha configurado un ejecutor de Algoritmo Genético.")
            return

        try:
            # Llamar al ejecutor configurado
            results = self.ga_executor(params, self.root) # Pasamos params y la ventana raíz

            if results is None: # La ejecución falló y ya mostró un error
                return

            self.ga_results = results['ga_results']
            self.population_history = results['population_history']
            self.fitness_history = results['fitness_history']
            self.best_fitness_history = results['best_fitness_history']

            function_text_from_ga = self.ga_results.get('function_text_for_report')
            if function_text_from_ga:
                from ui.function_editor import FunctionEditor # Temporal para obtener el validador
                temp_editor_dialog_parent = tk.Toplevel(self.root) # Crear un padre temporal para el diálogo
                temp_editor_dialog_parent.withdraw() # Ocultarlo
                
                temp_editor = FunctionEditor(temp_editor_dialog_parent) 
                temp_editor.current_function.set(function_text_from_ga)
                is_valid = temp_editor.validate_function()
                if is_valid:
                    self.ui_function_provider.set_function(function_text_from_ga, temp_editor.compiled_function)
                    self.config_panel.update_function_display()
                else:
                    messagebox.showerror("Error", "La función reportada por el AG no pudo ser validada por la UI.")
                temp_editor.dialog.destroy()
                temp_editor_dialog_parent.destroy() # Destruir el padre temporal también
            else:
                messagebox.showwarning("Advertencia", "El AG no reportó la función objetivo utilizada.")

            self.config_panel.enable_buttons()
            mode_text = "Minimización" if params['is_minimizing'] else "Maximización"
            messagebox.showinfo("Completado",
                                f"Algoritmo de ejemplo completado! ({mode_text})\n\n"
                                f"Mejor solución: x = {self.ga_results['best_x']:.6f}\n"
                                f"Mejor fitness (real): f(x) = {self.ga_results['best_fitness']:.6f}")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución del AG: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_report(self, filename):
        if not self.ga_results:
            messagebox.showwarning("Advertencia", "No hay resultados para generar el reporte.")
            return False
        try:
            # ReportGenerator usará get_function_provider() que ahora está
            # sincronizado con la función que el AG usó.
            self.report_generator.generate(
                filename, 
                self.ga_results, 
                self.best_fitness_history
            )
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")
            return False
    
    def save_animation(self, filename):
        if not self.ga_results:
            messagebox.showwarning("Advertencia", "Primero debe ejecutar el algoritmo.")
            return False
        try:
            self.animation_generator.generate(
                filename,
                self.best_fitness_history,
                self.ga_results['is_minimizing'],
                self.root
            )
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la animación: {str(e)}")
            return False
    
    def clear_results(self):
        self.ga_results = None
        self.population_history = []
        self.fitness_history = []
        self.best_fitness_history = []
        self.visualization_panel.clear_graph_area()
        self.visualization_panel.create_welcome_message()
        self.config_panel.disable_buttons()
        messagebox.showinfo("Completado", "Todos los resultados han sido limpiados.")
    
    def run(self):
        self.root.mainloop()
    
    def set_ga_executor(self, executor_func):
        """Permite configurar la función que ejecuta el AG"""
        self.ga_executor = executor_func