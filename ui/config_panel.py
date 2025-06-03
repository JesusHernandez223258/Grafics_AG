#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel de configuración de la aplicación
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QDoubleSpinBox, QPushButton,
    QLabel, QMessageBox, QSpinBox, QRadioButton, QGroupBox
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt
from utils.math_functions import set_function_provider
import numpy as np

class ConfigPanel(QWidget):
    """Clase que maneja el panel de configuración (izquierdo)"""

    def __init__(self, parent_widget, main_window, function_provider_instance):
        super().__init__(parent_widget)
        self.main_window = main_window
        self.function_provider = function_provider_instance
        set_function_provider(self.function_provider)

        # Inicializar TODOS los atributos de widgets a None ANTES de cargar la UI
        self.interval_a_spinbox = None
        self.interval_b_spinbox = None
        self.delta_x_spinbox = None
        self.pop_size_spinbox = None
        self.num_generations_spinbox = None
        self.prob_crossover_spinbox = None
        self.prob_mutation_i_spinbox = None
        self.prob_mutation_g_spinbox = None
        self.minimize_radio = None
        self.maximize_radio = None
        self.function_display_label = None
        self.num_points_label = None
        self.num_bits_label = None
        self.max_decimal_label = None
        self.editFunctionButton = None
        self.execute_ag_btn = None
        self.scrollable_widget_content = None

        # Nuevos botones
        self.objectiveGraphButton = None
        self.bestEvolutionGraphButton = None
        self.allEvolutionGraphButton = None
        self.animatedEvolutionButton = None
        self.generateReportButton = None
        self.downloadAnimationButton = None
        self.clearResultsButton = None
        self.graph_buttons_list = []


        ui_loaded_successfully = self.init_ui_from_designer()

        if ui_loaded_successfully:
            # Conecta señales
            if self.interval_a_spinbox:
                self.interval_a_spinbox.valueChanged.connect(self.update_calculated_values)
            if self.interval_b_spinbox:
                self.interval_b_spinbox.valueChanged.connect(self.update_calculated_values)
            if self.delta_x_spinbox:
                self.delta_x_spinbox.valueChanged.connect(self.update_calculated_values)

            if self.editFunctionButton:
                self.editFunctionButton.clicked.connect(self.open_function_editor)
            if self.execute_ag_btn:
                self.execute_ag_btn.clicked.connect(self.run_example_algorithm_from_config)

            # Conexiones para nuevos botones
            if self.objectiveGraphButton:
                self.objectiveGraphButton.clicked.connect(lambda: self.show_graph_slot("objective"))
            if self.bestEvolutionGraphButton:
                self.bestEvolutionGraphButton.clicked.connect(lambda: self.show_graph_slot("evolution_best"))
            if self.allEvolutionGraphButton:
                self.allEvolutionGraphButton.clicked.connect(lambda: self.show_graph_slot("evolution_all"))
            if self.animatedEvolutionButton:
                self.animatedEvolutionButton.clicked.connect(self.start_animation_slot)

            if self.generateReportButton:
                self.generateReportButton.clicked.connect(self.generate_report_slot)
            if self.downloadAnimationButton:
                self.downloadAnimationButton.clicked.connect(self.save_animation_slot)
            if self.clearResultsButton:
                self.clearResultsButton.clicked.connect(self.clear_results_slot)

            self.update_function_display()
            self.update_calculated_values()
            # self.disable_buttons() # Se llama desde MainWindow.__init__ después de que todo está creado
        else:
            print("ConfigPanel UI failed to load. Panel functionality will be limited.")
            # self.disable_buttons() # Podría ser necesario si la UI falla gravemente


    def init_ui_from_designer(self):
        outer_layout = QVBoxLayout() # No pasar 'self' aquí si se va a setear el layout luego
        self.setLayout(outer_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        outer_layout.addWidget(scroll_area)

        loader = QUiLoader()
        ui_file_path = "ui/config_panel.ui"
        ui_file = QFile(ui_file_path)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open UI file: {ui_file_path} - {ui_file.errorString()}")
            QMessageBox.critical(self, "UI Load Error", f"Could not load {ui_file_path}.\nEnsure the file exists and the path is correct relative to the execution directory (AG-main).")
            return False

        self.scrollable_widget_content = loader.load(ui_file, self)
        ui_file.close()

        if not self.scrollable_widget_content:
            print(f"Error loading UI file {ui_file_path}: {loader.errorString()}")
            QMessageBox.critical(self, "UI Load Error", f"Error parsing {ui_file_path}: {loader.errorString()}")
            return False

        scroll_area.setWidget(self.scrollable_widget_content)

        # --- Acceso a widgets del .ui ---
        self.interval_a_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "interval_a_spinbox")
        self.interval_b_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "interval_b_spinbox")
        self.delta_x_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "delta_x_spinbox")
        self.pop_size_spinbox = self.scrollable_widget_content.findChild(QSpinBox, "pop_size_spinbox")
        self.num_generations_spinbox = self.scrollable_widget_content.findChild(QSpinBox, "num_generations_spinbox")
        self.prob_crossover_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_crossover_spinbox")
        self.prob_mutation_i_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_mutation_i_spinbox")
        self.prob_mutation_g_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_mutation_g_spinbox")
        self.minimize_radio = self.scrollable_widget_content.findChild(QRadioButton, "minimize_radio")
        self.maximize_radio = self.scrollable_widget_content.findChild(QRadioButton, "maximize_radio")
        self.function_display_label = self.scrollable_widget_content.findChild(QLabel, "functionDisplayLabel")
        self.num_points_label = self.scrollable_widget_content.findChild(QLabel, "num_points_label")
        self.num_bits_label = self.scrollable_widget_content.findChild(QLabel, "num_bits_label")
        self.max_decimal_label = self.scrollable_widget_content.findChild(QLabel, "max_decimal_label")
        self.editFunctionButton = self.scrollable_widget_content.findChild(QPushButton, "editFunctionButton")
        self.execute_ag_btn = self.scrollable_widget_content.findChild(QPushButton, "execute_ag_btn")

        # --- Acceso a botones añadidos al .ui (si se hizo con Designer) ---
        self.objectiveGraphButton = self.scrollable_widget_content.findChild(QPushButton, "objectiveGraphButton")
        self.bestEvolutionGraphButton = self.scrollable_widget_content.findChild(QPushButton, "bestEvolutionGraphButton")
        self.allEvolutionGraphButton = self.scrollable_widget_content.findChild(QPushButton, "allEvolutionGraphButton")
        self.animatedEvolutionButton = self.scrollable_widget_content.findChild(QPushButton, "animatedEvolutionButton")
        self.generateReportButton = self.scrollable_widget_content.findChild(QPushButton, "generateReportButton")
        self.downloadAnimationButton = self.scrollable_widget_content.findChild(QPushButton, "downloadAnimationButton")
        self.clearResultsButton = self.scrollable_widget_content.findChild(QPushButton, "clearResultsButton")
        
        # Llenar graph_buttons_list
        if self.objectiveGraphButton: self.graph_buttons_list.append(self.objectiveGraphButton)
        if self.bestEvolutionGraphButton: self.graph_buttons_list.append(self.bestEvolutionGraphButton)
        if self.allEvolutionGraphButton: self.graph_buttons_list.append(self.allEvolutionGraphButton)
        if self.animatedEvolutionButton: self.graph_buttons_list.append(self.animatedEvolutionButton)

        # Verificar que los widgets esenciales (del .ui original y los nuevos) fueron encontrados
        essential_widgets_map = {
            "interval_a_spinbox": self.interval_a_spinbox, "interval_b_spinbox": self.interval_b_spinbox,
            "delta_x_spinbox": self.delta_x_spinbox, "pop_size_spinbox": self.pop_size_spinbox,
            "num_generations_spinbox": self.num_generations_spinbox,
            "prob_crossover_spinbox": self.prob_crossover_spinbox,
            "prob_mutation_i_spinbox": self.prob_mutation_i_spinbox,
            "prob_mutation_g_spinbox": self.prob_mutation_g_spinbox,
            "minimize_radio": self.minimize_radio, "functionDisplayLabel": self.function_display_label,
            "num_points_label": self.num_points_label, "num_bits_label": self.num_bits_label,
            "max_decimal_label": self.max_decimal_label, "editFunctionButton": self.editFunctionButton,
            "execute_ag_btn": self.execute_ag_btn,
            "objectiveGraphButton": self.objectiveGraphButton, # Nuevo
            "generateReportButton": self.generateReportButton, # Nuevo
            "clearResultsButton": self.clearResultsButton      # Nuevo
        }

        all_essentials_found = True
        for name, widget_instance in essential_widgets_map.items():
            if not widget_instance:
                print(f"CRITICAL WARNING: Widget '{name}' not found in config_panel.ui. Check objectName in Qt Designer or if it was added to the .ui file.")
                all_essentials_found = False
        
        if not all_essentials_found:
            QMessageBox.warning(self, "UI Incompleta", "Algunos componentes de la UI no se cargaron correctamente. La funcionalidad puede estar limitada.")
            # Considerar retornar False si la UI es inutilizable sin estos.
            # return False 
            
        return True


    def open_function_editor(self):
        from ui.function_editor import FunctionEditor
        editor = FunctionEditor(self)

        if self.function_provider and self.function_provider.function_text:
            editor.function_entry.setText(self.function_provider.function_text)
        elif hasattr(editor, 'default_function'):
             editor.function_entry.setText(editor.default_function)

        def on_function_accept_wrapper(function_text, compiled_function):
            if self.function_provider:
                self.function_provider.set_function(function_text, compiled_function)
                self.update_function_display()
                QMessageBox.information(self, "Función Actualizada", "La función objetivo ha sido actualizada.")
            else:
                QMessageBox.warning(self, "Error", "Function provider no disponible.")

        editor.callback_function = on_function_accept_wrapper
        editor.exec()


    def update_function_display(self):
        if self.function_display_label and self.function_provider:
            function_text = self.function_provider.function_text
            display_text = function_text.replace('*', '·')
            self.function_display_label.setText(f"f(x) = {display_text}")
        elif not self.function_display_label:
            print("Warning: functionDisplayLabel not found for update.")


    def update_calculated_values(self):
        required_spinboxes = [self.interval_a_spinbox, self.interval_b_spinbox, self.delta_x_spinbox]
        required_labels = [self.num_points_label, self.num_bits_label, self.max_decimal_label]

        if not all(s for s in required_spinboxes) or not all(l for l in required_labels):
            if self.num_points_label: self.num_points_label.setText("...")
            if self.num_bits_label: self.num_bits_label.setText("...")
            if self.max_decimal_label: self.max_decimal_label.setText("...")
            return

        try:
            x_min = self.interval_a_spinbox.value()
            x_max = self.interval_b_spinbox.value()
            delta_x = self.delta_x_spinbox.value()

            if x_max > x_min and delta_x > 0:
                n_bits = 0
                if x_min == 0 and x_max == 31 and delta_x == 1.0:
                    n_bits = 5
                elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0:
                    range_size = int(x_max - x_min) + 1
                    n_bits = (range_size -1 ).bit_length() if range_size > 0 else 0
                else:
                    num_divisions = int(np.round((x_max - x_min) / delta_x))
                    n_bits = (num_divisions).bit_length() if num_divisions >= 0 else 0
                
                if n_bits == 0 and ((x_max - x_min) > 0 or (x_min == x_max and delta_x > 0)):
                    n_bits = max(1, n_bits)
                if x_min == x_max and n_bits == 1 and delta_x > 0 : # Un solo punto, 0 bits es más correcto
                    num_possible_points = int(np.round((x_max - x_min) / delta_x)) + 1
                    if num_possible_points == 1:
                        n_bits = 0

                max_decimal = (2**n_bits - 1) if n_bits > 0 else 0
                num_points = max_decimal + 1

                self.num_points_label.setText(str(num_points))
                self.num_bits_label.setText(str(n_bits))
                self.max_decimal_label.setText(str(max_decimal))
            else:
                self.num_points_label.setText("...")
                self.num_bits_label.setText("...")
                self.max_decimal_label.setText("...")
        except Exception as e:
            print(f"Error in update_calculated_values: {e}")
            import traceback
            traceback.print_exc()
            if self.num_points_label: self.num_points_label.setText("Error")
            if self.num_bits_label: self.num_bits_label.setText("Error")
            if self.max_decimal_label: self.max_decimal_label.setText("Error")


    def run_example_algorithm_from_config(self):
        required_widgets_for_run = [
            self.interval_a_spinbox, self.interval_b_spinbox, self.delta_x_spinbox,
            self.pop_size_spinbox, self.num_generations_spinbox, self.prob_crossover_spinbox,
            self.prob_mutation_i_spinbox, self.prob_mutation_g_spinbox, self.minimize_radio
        ]
        if not all(w for w in required_widgets_for_run):
            QMessageBox.critical(self, "Error de Configuración", "Faltan componentes de UI. Verifique objectNames en .ui y código.")
            return

        params = {
            'interval_a': self.interval_a_spinbox.value(),
            'interval_b': self.interval_b_spinbox.value(),
            'delta_x': self.delta_x_spinbox.value(),
            'pop_size': self.pop_size_spinbox.value(),
            'num_generations': self.num_generations_spinbox.value(),
            'prob_crossover': self.prob_crossover_spinbox.value(),
            'prob_mutation_i': self.prob_mutation_i_spinbox.value(),
            'prob_mutation_g': self.prob_mutation_g_spinbox.value(),
            'is_minimizing': self.minimize_radio.isChecked() if self.minimize_radio else True
        }
        if self.main_window:
            self.main_window.run_example_algorithm(params)
        else:
            QMessageBox.critical(self, "Error Interno", "Referencia a MainWindow no encontrada.")


    def show_graph_slot(self, graph_type: str):
        if not self.main_window or not self.main_window.ga_results:
            QMessageBox.warning(self, "Advertencia", "Primero debe ejecutar el algoritmo.")
            return
        self.update_graph_button_selection(graph_type)
        if hasattr(self.main_window, 'visualization_panel') and self.main_window.visualization_panel:
            self.main_window.visualization_panel.show_graph(
                graph_type,
                self.main_window.ga_results,
                self.main_window.population_history,
                self.main_window.fitness_history,
                self.main_window.best_fitness_history
            )

    def start_animation_slot(self):
        if not self.main_window or not self.main_window.ga_results:
            QMessageBox.warning(self, "Advertencia", "Primero debe ejecutar el algoritmo.")
            return
        
        vis_panel = self.main_window.visualization_panel
        if vis_panel and vis_panel.is_animating: # Verificar que vis_panel exista
            if self.animatedEvolutionButton: self.animatedEvolutionButton.setText("Evolución Animada")
            vis_panel.stop_animation()
            self.update_graph_button_selection(None)
        elif vis_panel: # Verificar que vis_panel exista
            if self.animatedEvolutionButton: self.animatedEvolutionButton.setText("Detener Animación")
            self.update_graph_button_selection("animation")
            vis_panel.start_animation(
                self.main_window.best_fitness_history,
                self.main_window.ga_results['is_minimizing']
            )

    def generate_report_slot(self):
        if self.main_window: self.main_window.generate_report()

    def save_animation_slot(self):
        if self.main_window: self.main_window.save_animation()

    def clear_results_slot(self):
        if self.main_window: self.main_window.clear_results()


    def update_graph_button_selection(self, selected_type: str | None):
        buttons_map = {
            "objective": self.objectiveGraphButton,
            "evolution_best": self.bestEvolutionGraphButton,
            "evolution_all": self.allEvolutionGraphButton,
        }
        for graph_name, button_widget in buttons_map.items():
            if button_widget:
                is_selected = (graph_name == selected_type)
                button_widget.setProperty("selected", is_selected)
                button_widget.style().unpolish(button_widget)
                button_widget.style().polish(button_widget)

        if self.animatedEvolutionButton:
            is_anim_selected = False
            is_animating_now = False
            if self.main_window and hasattr(self.main_window, 'visualization_panel') and self.main_window.visualization_panel:
                is_animating_now = self.main_window.visualization_panel.is_animating
            
            is_anim_selected = (selected_type == "animation" or is_animating_now)
            self.animatedEvolutionButton.setProperty("selected", is_anim_selected)

            if is_animating_now:
                 self.animatedEvolutionButton.setText("Detener Animación")
            else:
                 self.animatedEvolutionButton.setText("Evolución Animada")

            self.animatedEvolutionButton.style().unpolish(self.animatedEvolutionButton)
            self.animatedEvolutionButton.style().polish(self.animatedEvolutionButton)


    def enable_buttons(self):
        has_results = self.main_window and hasattr(self.main_window, 'ga_results') and self.main_window.ga_results is not None

        if self.execute_ag_btn: self.execute_ag_btn.setEnabled(True)
        if self.editFunctionButton: self.editFunctionButton.setEnabled(True)

        for btn in self.graph_buttons_list:
            if btn: btn.setEnabled(has_results)
        
        if self.generateReportButton: self.generateReportButton.setEnabled(has_results)
        if self.downloadAnimationButton: self.downloadAnimationButton.setEnabled(has_results)
        if self.clearResultsButton: self.clearResultsButton.setEnabled(True)
        
        if has_results:
            # No seleccionar nada por defecto aquí para evitar problemas de inicialización.
            # La selección se manejará cuando el usuario haga clic o termine la animación.
            pass 
        else:
             self.update_graph_button_selection(None)


    def disable_buttons(self):
        if self.execute_ag_btn: self.execute_ag_btn.setEnabled(True)
        if self.editFunctionButton: self.editFunctionButton.setEnabled(True)

        for btn in self.graph_buttons_list:
            if btn: btn.setEnabled(False)
        
        if self.generateReportButton: self.generateReportButton.setEnabled(False)
        if self.downloadAnimationButton: self.downloadAnimationButton.setEnabled(False)
        if self.clearResultsButton: self.clearResultsButton.setEnabled(True) 
        
        self.update_graph_button_selection(None)