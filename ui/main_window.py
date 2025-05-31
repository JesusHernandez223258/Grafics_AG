# ===== ./ui/main_window.py =====

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ventana principal de la aplicación - Visualizador de Resultados de AG (Versión PySide6)
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter, QMessageBox, QVBoxLayout, QFileDialog, QProgressDialog
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

# Asegúrate de que estas importaciones apunten a las versiones PySide6 de tus paneles
from ui.config_panel import ConfigPanel
from ui.visualization_panel import VisualizationPanel
from utils.export import ReportGenerator, AnimationGenerator
from utils.math_functions import set_function_provider
# Asegúrate que CustomFunctionProvider es la versión adaptada para PySide6/Sympy
from ui.function_editor import CustomFunctionProvider, FunctionEditor
from utils.helpers import open_file # Usaremos el helper para abrir archivos

class MainWindow(QMainWindow):
    """Clase principal que maneja la ventana y coordina los componentes (PySide6)"""

    def __init__(self):
        """Inicializa la ventana principal y sus componentes"""
        super().__init__()
        self.setWindowTitle("Algoritmo Genético - Visualizador de Resultados (PySide6)")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1000, 600)

        self.ga_results = None
        self.population_history = []
        self.fitness_history = []
        self.best_fitness_history = []

        self.report_generator = ReportGenerator()
        self.animation_generator = AnimationGenerator()
        self.ui_function_provider = CustomFunctionProvider() # Esta es tu clase adaptada
        set_function_provider(self.ui_function_provider)

        self.ga_executor = None

        self.create_interface()

    def create_interface(self):
        """Crea la interfaz dividida en dos paneles usando QSplitter"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Panel izquierdo (Configuración)
        # Creamos un QWidget que actuará como contenedor para el ConfigPanel
        self.left_pane_container = QWidget()
        left_layout = QVBoxLayout(self.left_pane_container) # Layout para el contenedor
        left_layout.setContentsMargins(0,0,0,0) # Para que ConfigPanel lo llene
        # ConfigPanel se añade a este QWidget contenedor
        self.config_panel = ConfigPanel(self.left_pane_container, self, self.ui_function_provider)
        left_layout.addWidget(self.config_panel)
        self.main_splitter.addWidget(self.left_pane_container)

        # Panel derecho (Visualización)
        self.right_pane_container = QWidget()
        right_layout = QVBoxLayout(self.right_pane_container)
        right_layout.setContentsMargins(0,0,0,0)
        self.visualization_panel = VisualizationPanel(self.right_pane_container, self)
        right_layout.addWidget(self.visualization_panel)
        self.main_splitter.addWidget(self.right_pane_container)

        # Ajustar tamaños iniciales y políticas de expansión
        self.main_splitter.setSizes([420, self.width() - 450]) # Tamaños iniciales aproximados
        self.main_splitter.setStretchFactor(0, 0) # Panel izquierdo no se estira tanto
        self.main_splitter.setStretchFactor(1, 1) # Panel derecho se estira más

    def run_example_algorithm(self, params: dict):
        """Ejecuta el algoritmo genético configurado con los parámetros proporcionados"""
        if not self.ga_executor:
            QMessageBox.critical(self, "Error", "No se ha configurado un ejecutor de Algoritmo Genético.")
            return

        # Mostrar un diálogo de progreso simple
        progress_dialog = QProgressDialog("Ejecutando AG...", "Cancelar", 0, 0, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle("Procesando")
        progress_dialog.show()
        # QApplication.processEvents() # Para que se muestre inmediatamente

        try:
            # Pasamos 'self' (la QMainWindow) como ventana padre para el AG,
            # por si el AG necesita crear sus propios diálogos de progreso Qt.
            results = self.ga_executor(params, self)

            if results is None:
                progress_dialog.close()
                return

            self.ga_results = results['ga_results']
            self.population_history = results['population_history']
            self.fitness_history = results['fitness_history']
            self.best_fitness_history = results['best_fitness_history']

            # Actualizar la función en la UI si el AG la reporta
            function_text_from_ga = self.ga_results.get('function_text_for_report')
            if function_text_from_ga:
                # Usamos el FunctionEditor de PySide6 para validar y obtener la función compilada
                temp_editor = FunctionEditor(self) # 'self' es el padre QMainWindow
                temp_editor.function_entry.setText(function_text_from_ga) # Asumimos que FunctionEditor tiene 'function_entry'
                is_valid = temp_editor.validate_function()
                if is_valid:
                    # Asumimos que validate_function en FunctionEditor actualiza self.compiled_function_result
                    self.ui_function_provider.set_function(function_text_from_ga, temp_editor.compiled_function_result)
                    self.config_panel.update_function_display() # ConfigPanel debe tener este método
                else:
                    QMessageBox.critical(self, "Error de Función",
                                         "La función reportada por el AG no pudo ser validada por la UI.")
                # temp_editor.destroy() # No es necesario, se cierra con el scope o si es modal
            else:
                QMessageBox.warning(self, "Advertencia", "El AG no reportó la función objetivo utilizada.")

            self.config_panel.enable_buttons() # ConfigPanel debe tener este método
            mode_text = "Minimización" if params['is_minimizing'] else "Maximización"
            QMessageBox.information(self, "Completado",
                                f"Algoritmo de ejemplo completado! ({mode_text})\n\n"
                                f"Mejor solución: x = {self.ga_results['best_x']:.6f}\n"
                                f"Mejor fitness (real): f(x) = {self.ga_results['best_fitness']:.6f}")

        except Exception as e:
            QMessageBox.critical(self, "Error en AG", f"Error durante la ejecución del AG: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            progress_dialog.close()


    def generate_report(self): # Ya no necesita 'filename' como argumento directo
        if not self.ga_results:
            QMessageBox.warning(self, "Advertencia", "No hay resultados para generar el reporte.")
            return False

        # Usar QFileDialog para obtener el nombre del archivo
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte",
            "", # Directorio inicial (opcional)
            "Text files (*.txt);;All files (*.*)"
        )
        if not filename: # El usuario canceló
            return False

        try:
            self.report_generator.generate(
                filename,
                self.ga_results,
                self.best_fitness_history
            )
            QMessageBox.information(self, "Reporte Guardado", f"Reporte guardado en:\n{filename}")
            if QMessageBox.question(self, "Abrir Reporte", "¿Desea abrir el reporte generado?") == QMessageBox.Yes:
                open_file(filename) # Usar el helper
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error de Reporte", f"Error al generar el reporte: {str(e)}")
            return False


    def save_animation(self): # Ya no necesita 'filename' como argumento directo
        if not self.ga_results:
            QMessageBox.warning(self, "Advertencia", "Primero debe ejecutar el algoritmo.")
            return False

        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Guardar Animación",
            "",
            "MP4 files (*.mp4);;GIF files (*.gif);;All files (*.*)"
        )
        if not filename:
            return False

        try:
            # El AnimationGenerator ya maneja su propio diálogo de progreso y QMessageBox
            # Pasamos 'self' como ventana raíz para que los diálogos del generador sean modales a esta.
            success = self.animation_generator.generate(
                filename,
                self.best_fitness_history,
                self.ga_results['is_minimizing'],
                self # QWidget padre para los diálogos del AnimationGenerator
            )
            # Nota: AnimationGenerator debería mostrar su propio QMessageBox de éxito/error
            return success
        except Exception as e:
            # Esto es un fallback si AnimationGenerator no maneja su propia excepción
            QMessageBox.critical(self, "Error de Animación", f"Error al generar la animación: {str(e)}")
            return False


    def clear_results(self):
        self.ga_results = None
        self.population_history = []
        self.fitness_history = []
        self.best_fitness_history = []
        self.visualization_panel.clear_graph_area()
        self.visualization_panel.create_welcome_message() # Recrear mensaje de bienvenida
        self.config_panel.disable_buttons() # ConfigPanel debe tener este método
        QMessageBox.information(self, "Resultados Limpiados", "Todos los resultados han sido limpiados.")

    # El método run() ya no es necesario aquí, QApplication.exec() en main.py lo maneja.

    def set_ga_executor(self, executor_func):
        self.ga_executor = executor_func