#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel de configuración de la aplicación
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QDoubleSpinBox, QPushButton, QLabel, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from utils.math_functions import set_function_provider

class ConfigPanel(QWidget):
    """Clase que maneja el panel de configuración (izquierdo)"""
    
    def __init__(self, parent_widget, main_window, function_provider_instance):
        super().__init__(parent_widget)  # parent_widget debe ser QWidget o None
        self.main_window = main_window
        self.function_provider = function_provider_instance
        set_function_provider(self.function_provider)

        self.init_ui_from_designer()

        # Conecta señales de los widgets cargados desde el archivo .ui
        if hasattr(self, 'interval_a_spinbox') and self.interval_a_spinbox:
            self.interval_a_spinbox.valueChanged.connect(self.update_calculated_values)
        if hasattr(self, 'editFunctionButton') and self.editFunctionButton:
            self.editFunctionButton.clicked.connect(self.open_function_editor)
        if hasattr(self, 'execute_ag_btn') and self.execute_ag_btn:
            self.execute_ag_btn.clicked.connect(self.run_example_algorithm_from_config)

        self.update_function_display()
        self.update_calculated_values()
        self.disable_buttons()

    def init_ui_from_designer(self):
        outer_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        outer_layout.addWidget(scroll_area)

        loader = QUiLoader()
        ui_file_path = "ui/config_panel.ui"
        ui_file = QFile(ui_file_path)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open UI file: {ui_file_path} - {ui_file.errorString()}")
            QMessageBox.critical(self, "UI Load Error", f"Could not load {ui_file_path}")
            return

        self.scrollable_widget_content = loader.load(ui_file, self)
        ui_file.close()

        if not self.scrollable_widget_content:
            print(f"Error loading UI file {ui_file_path}: {loader.errorString()}")
            QMessageBox.critical(self, "UI Load Error", f"Error parsing {ui_file_path}: {loader.errorString()}")
            return

        scroll_area.setWidget(self.scrollable_widget_content)

        # --- Acceso robusto a todos los widgets necesarios ---
        self.interval_a_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "interval_a_spinbox")
        if not self.interval_a_spinbox:
            print("CRITICAL ERROR: 'interval_a_spinbox' not found in config_panel.ui. Check objectName.")

        self.interval_b_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "interval_b_spinbox")
        if not self.interval_b_spinbox:
            print("CRITICAL ERROR: 'interval_b_spinbox' not found. Check objectName.")

        self.num_points_label = self.scrollable_widget_content.findChild(QLabel, "num_points_label")
        if not self.num_points_label:
            print("CRITICAL ERROR: 'num_points_label' not found. Check objectName.")

        self.num_bits_label = self.scrollable_widget_content.findChild(QLabel, "num_bits_label")
        if not self.num_bits_label:
            print("CRITICAL ERROR: 'num_bits_label' not found. Check objectName.")

        self.max_decimal_label = self.scrollable_widget_content.findChild(QLabel, "max_decimal_label")
        if not self.max_decimal_label:
            print("CRITICAL ERROR: 'max_decimal_label' not found. Check objectName.")

        self.function_display_label = self.scrollable_widget_content.findChild(QLabel, "functionDisplayLabel")
        if not self.function_display_label:
            print("CRITICAL ERROR: 'functionDisplayLabel' not found. Check objectName.")

        self.editFunctionButton = self.scrollable_widget_content.findChild(QPushButton, "editFunctionButton")
        if not self.editFunctionButton:
            print("CRITICAL ERROR: 'editFunctionButton' not found. Check objectName.")

        self.execute_ag_btn = self.scrollable_widget_content.findChild(QPushButton, "execute_ag_btn")
        if not self.execute_ag_btn:
            print("CRITICAL ERROR: 'execute_ag_btn' not found. Check objectName.")

        self.delta_x_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "delta_x_spinbox")
        if not self.delta_x_spinbox:
            print("CRITICAL ERROR: 'delta_x_spinbox' not found. Check objectName.")

        from PySide6.QtWidgets import QSpinBox, QRadioButton
        self.pop_size_spinbox = self.scrollable_widget_content.findChild(QSpinBox, "pop_size_spinbox")
        if not self.pop_size_spinbox:
            print("CRITICAL ERROR: 'pop_size_spinbox' not found. Check objectName.")

        self.num_generations_spinbox = self.scrollable_widget_content.findChild(QSpinBox, "num_generations_spinbox")
        if not self.num_generations_spinbox:
            print("CRITICAL ERROR: 'num_generations_spinbox' not found. Check objectName.")

        self.prob_crossover_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_crossover_spinbox")
        if not self.prob_crossover_spinbox:
            print("CRITICAL ERROR: 'prob_crossover_spinbox' not found. Check objectName.")

        self.prob_mutation_i_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_mutation_i_spinbox")
        if not self.prob_mutation_i_spinbox:
            print("CRITICAL ERROR: 'prob_mutation_i_spinbox' not found. Check objectName.")

        self.prob_mutation_g_spinbox = self.scrollable_widget_content.findChild(QDoubleSpinBox, "prob_mutation_g_spinbox")
        if not self.prob_mutation_g_spinbox:
            print("CRITICAL ERROR: 'prob_mutation_g_spinbox' not found. Check objectName.")

        self.minimize_radio = self.scrollable_widget_content.findChild(QRadioButton, "minimize_radio")
        if not self.minimize_radio:
            print("CRITICAL ERROR: 'minimize_radio' not found. Check objectName.")

        self.maximize_radio = self.scrollable_widget_content.findChild(QRadioButton, "maximize_radio")
        if not self.maximize_radio:
            print("CRITICAL ERROR: 'maximize_radio' not found. Check objectName.")

    def open_function_editor(self):
        # MODIFICADO: Importar FunctionEditor dentro del método
        from ui.function_editor import FunctionEditor
        
        def on_function_accept(function_text, compiled_function):
            self.function_provider.set_function(function_text, compiled_function)
            set_function_provider(self.function_provider)
            self.update_function_display()
            QMessageBox.information(self, "Función Actualizada", 
                              "La función objetivo ha sido actualizada para el visualizador y el AG de ejemplo.")
        
        FunctionEditor(self, on_function_accept, initial_function=self.function_provider.function_text)

    def update_function_display(self):
        if hasattr(self, 'function_display_label') and self.function_provider:
            function_text = self.function_provider.function_text
            display_text = function_text.replace('*', '·')
            self.function_display_label.setText(f"f(x) = {display_text}")

    def update_calculated_values(self):
        try:
            x_min = self.interval_a_spinbox.value()
            x_max = self.interval_b_spinbox.value()
            delta_x = self.delta_x_spinbox.value()
            if x_max > x_min and delta_x > 0:
                # MODIFICADO: Simplificado el cálculo de n_bits como en el AG.
                # Este cálculo es principalmente para visualización en la UI,
                # el AG debe realizar su propio cálculo exacto.
                if x_min == 0 and x_max == 31 and delta_x == 1.0: # Caso especial para coincidir con AG
                    n_bits = 5
                elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0: # Otro caso para rangos enteros
                    range_size = int(x_max - x_min) + 1
                    n_bits = int((range_size - 1).bit_length())
                else: # Cálculo general
                    num_divisions = int(round((x_max - x_min) / delta_x)) # Usar round para evitar problemas de flotantes
                    n_bits = int((num_divisions + 1).bit_length()) if num_divisions >= 0 else 0 # +1 para incluir el punto final
                
                if n_bits < 1: n_bits = 1 # Asegurar al menos 1 bit

                max_decimal = 2 ** n_bits - 1
                num_points = max_decimal + 1 # O num_divisions + 1 para el cálculo general
                
                self.num_points_label.setText(str(num_points))
                self.num_bits_label.setText(str(n_bits))
                self.max_decimal_label.setText(str(max_decimal))
            else:
                self.num_points_label.setText("...")
                self.num_bits_label.setText("...")
                self.max_decimal_label.setText("...")
        except Exception:
            self.num_points_label.setText("Error")
            self.num_bits_label.setText("Error")
            self.max_decimal_label.setText("Error")


    def run_example_algorithm_from_config(self):
        x_min = self.interval_a_spinbox.value()
        x_max = self.interval_b_spinbox.value()
        delta_x = self.delta_x_spinbox.value()
        pop_size_val = self.pop_size_spinbox.value()
        num_generations_val = self.num_generations_spinbox.value()
        prob_crossover_val = self.prob_crossover_spinbox.value()
        prob_mutation_i_val = self.prob_mutation_i_spinbox.value()
        prob_mutation_g_val = self.prob_mutation_g_spinbox.value()
        is_minimizing = self.minimize_radio.isChecked()

        if x_min >= x_max:
            QMessageBox.critical(self, "Error", "El intervalo [a,b] no es válido. a debe ser menor que b.")
            return
        if delta_x <= 0:
            QMessageBox.critical(self, "Error", "Δx debe ser mayor que 0.")
            return

        params = {
            'interval_a': x_min, 'interval_b': x_max, 'delta_x': delta_x,
            'pop_size': int(pop_size_val),
            'num_generations': int(num_generations_val),
            'prob_crossover': prob_crossover_val,
            'prob_mutation_i': prob_mutation_i_val,
            'prob_mutation_g': prob_mutation_g_val,
            'is_minimizing': is_minimizing
        }
        self.main_window.run_example_algorithm(params)

    def enable_buttons(self):
        # Implementa según tus botones
        pass

    def disable_buttons(self):
        # Implementa según tus botones
        pass

    def clear_results(self):
        self.main_window.clear_results()
        # self.update_button_selection("none")

class Frame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ... tu inicialización ...