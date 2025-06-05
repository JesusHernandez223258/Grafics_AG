# ===== ./ui/main_window.py =====

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ventana principal de la aplicación - Visualizador de Resultados de AG (Versión PySide6)
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter, QMessageBox, QVBoxLayout, QFileDialog, QProgressDialog, QApplication
from PySide6.QtCore import Qt, QUrl
# from PySide6.QtGui import QDesktopServices # No se usa directamente aquí si open_file lo maneja

# Asegúrate de que estas importaciones apunten a las versiones PySide6 de tus paneles
from ui.config_panel import ConfigPanel
from ui.visualization_panel import VisualizationPanel # Asumimos que este es PySide6
from utils.export import ReportGenerator, AnimationGenerator
from utils.math_functions import set_function_provider
# Asegúrate que CustomFunctionProvider es la versión adaptada para PySide6/Sympy
from ui.function_editor import CustomFunctionProvider, FunctionEditor # Asumimos que FunctionEditor es PySide6
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
        self.animation_generator = AnimationGenerator() # Asegúrate que usa QMessageBox/QProgressDialog
        self.ui_function_provider = CustomFunctionProvider()
        set_function_provider(self.ui_function_provider)

        self.ga_executor = None
        
        # Inicializar los paneles a None primero
        self.config_panel = None
        self.visualization_panel = None

        self.create_interface()

        # Llamar a disable_buttons DESPUÉS de que create_interface haya completado
        # y ambos paneles (config_panel y visualization_panel) existan.
        if self.config_panel:
            self.config_panel.disable_buttons() # Establece el estado inicial correcto


    def create_interface(self):
        """Crea la interfaz dividida en dos paneles usando QSplitter"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Panel izquierdo (Configuración)
        self.left_pane_container = QWidget()
        left_layout = QVBoxLayout(self.left_pane_container)
        left_layout.setContentsMargins(0,0,0,0)
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

        self.main_splitter.setSizes([420, self.width() - 450])
        self.main_splitter.setStretchFactor(0, 0)
        self.main_splitter.setStretchFactor(1, 1)

    def run_example_algorithm(self, params: dict):
        if not self.ga_executor:
            QMessageBox.critical(self, "Error", "No se ha configurado un ejecutor de Algoritmo Genético.")
            return

        progress_dialog = QProgressDialog("Ejecutando AG...", "Cancelar", 0, 0, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle("Procesando")
        progress_dialog.show()

        try:
            results = self.ga_executor(params, self)

            if results is None:
                progress_dialog.close()
                return

            self.ga_results = results['ga_results']
            self.population_history = results['population_history']
            self.fitness_history = results['fitness_history']
            self.best_fitness_history = results['best_fitness_history']

            function_text_from_ga = self.ga_results.get('function_text_for_report')
            if function_text_from_ga and self.config_panel: # Verificar config_panel
                # Asumiendo que FunctionEditor es un QDialog
                temp_editor = FunctionEditor(self)
                if hasattr(temp_editor, 'function_entry'):
                    temp_editor.function_entry.setText(function_text_from_ga)
                    is_valid = temp_editor.validate_function()
                    if is_valid and hasattr(temp_editor, 'compiled_function_result'):
                        self.ui_function_provider.set_function(function_text_from_ga, temp_editor.compiled_function_result)
                        self.config_panel.update_function_display()
                    elif not is_valid:
                        QMessageBox.critical(self, "Error de Función", "La función reportada por el AG no pudo ser validada por la UI.")
                else:
                    QMessageBox.warning(self, "Advertencia", "Editor de funciones no compatible para actualización automática.")

            if self.config_panel: self.config_panel.enable_buttons()
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


    def generate_report(self):
        if not self.ga_results:
            QMessageBox.warning(self, "Advertencia", "No hay resultados para generar el reporte.")
            return False

        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Guardar Reporte", "", "Text files (*.txt);;All files (*.*)"
        )
        if not filename: return False

        try:
            self.report_generator.generate(
                filename, self.ga_results, self.best_fitness_history
            )
            QMessageBox.information(self, "Reporte Guardado", f"Reporte guardado en:\n{filename}")
            if QMessageBox.question(self, "Abrir Reporte", "¿Desea abrir el reporte generado?") == QMessageBox.Yes:
                # utils.helpers.open_file debe ser compatible con PySide6 (no usar tkinter.messagebox)
                if not open_file(filename):
                     QMessageBox.warning(self, "Abrir Archivo", "No se pudo abrir el archivo automáticamente.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error de Reporte", f"Error al generar el reporte: {str(e)}")
            return False


    def save_animation(self):
        if not self.ga_results:
            QMessageBox.warning(self, "Advertencia", "Primero debe ejecutar el algoritmo.")
            return False

        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Guardar Animación", "", "MP4 files (*.mp4);;GIF files (*.gif);;All files (*.*)"
        )
        if not filename:
            return False
    
        progress_dialog_anim = QProgressDialog("Generando Animación...", "Cancelar", 0, 0, self)
        progress_dialog_anim.setWindowModality(Qt.WindowModal)
        progress_dialog_anim.setWindowTitle("Procesando Animación")
        progress_dialog_anim.show()
        QApplication.processEvents()  # Asegura que el diálogo se muestre
    
        try:
            # LLAMADA SIN EL 5to ARGUMENTO
            result_info = self.animation_generator.generate(
                filename,
                self.best_fitness_history,
                self.ga_results['is_minimizing']
            )
            progress_dialog_anim.close()
    
            if result_info and result_info.get("success"):
                QMessageBox.information(self, "Animación Guardada", result_info.get("message", "Animación guardada."))
                if QMessageBox.question(self, "Abrir Animación", "¿Desea abrir la animación generada?") == QMessageBox.Yes:
                    from utils.helpers import open_file
                    if not open_file(filename):
                        QMessageBox.warning(self, "Abrir Archivo", "No se pudo abrir el archivo automáticamente.")
                return True
            elif result_info:
                QMessageBox.critical(self, "Error de Animación", result_info.get("message", "Error desconocido al generar animación."))
                return False
            else:
                QMessageBox.critical(self, "Error de Animación", "Error desconocido al generar animación.")
                return False
    
        except Exception as e:
            progress_dialog_anim.close()
            QMessageBox.critical(self, "Error de Animación", f"Excepción al generar la animación: {str(e)}")
            return False

    def clear_results(self):
        self.ga_results = None
        self.population_history = []
        self.fitness_history = []
        self.best_fitness_history = []
        
        if self.visualization_panel:
            self.visualization_panel.clear_graph_area()
            self.visualization_panel.create_welcome_message()

        if self.config_panel:
            self.config_panel.disable_buttons()
            self.config_panel.update_graph_button_selection(None)

        QMessageBox.information(self, "Resultados Limpiados", "Todos los resultados han sido limpiados.")


    def set_ga_executor(self, executor_func):
        self.ga_executor = executor_func