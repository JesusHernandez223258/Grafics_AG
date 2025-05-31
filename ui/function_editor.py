#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor de funciones con teclado virtual usando CustomTkinter
(Paleta de colores mejorada para modo oscuro)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QGridLayout, QMessageBox, QGroupBox, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import numpy as np
from sympy import symbols, sympify, lambdify, SympifyError

class FunctionEditor(QDialog):
    def __init__(self, parent, callback_function=None, initial_function=None):
        super().__init__(parent)
        self.callback_function = callback_function
        self.default_function = "ln(1+abs(x^7)) + pi*cos(x) + sin(15.5*x)"
        current_initial = initial_function if initial_function is not None else self.default_function
        self.compiled_function_result = None

        self.setWindowTitle("Editor de Funciones")
        self.setMinimumSize(800, 650)

        self.init_ui(current_initial)
        self.validate_function()
        self.function_entry.textChanged.connect(self.update_preview_and_validate)

    def init_ui(self, initial_function_str):
        main_layout = QVBoxLayout(self)

        # Input field
        self.function_entry = QLineEdit(initial_function_str)
        self.function_entry.setFont(QFont("Consolas", 16))
        main_layout.addWidget(self.function_entry)

        # Virtual Keyboard
        keyboard_group = QGroupBox("Teclado Virtual")
        keyboard_layout = QGridLayout()
        keyboard_group.setLayout(keyboard_layout)
        main_layout.addWidget(keyboard_group)

        # Keyboard buttons
        buttons = [
            # Row, Col, Text, Insert
            (0, 0, '7', '7'), (0, 1, '8', '8'), (0, 2, '9', '9'), (0, 3, '+', '+'), (0, 4, '-', '-'),
            (1, 0, '4', '4'), (1, 1, '5', '5'), (1, 2, '6', '6'), (1, 3, '*', '*'), (1, 4, '/', '/'),
            (2, 0, '1', '1'), (2, 1, '2', '2'), (2, 2, '3', '3'), (2, 3, '^', '^'), (2, 4, '(', '('),
            (3, 0, '0', '0'), (3, 1, '.', '.'), (3, 2, ')', ')'), (3, 3, ',', ','), (3, 4, '=', '='),
            (4, 0, 'π', 'π'), (4, 1, 'e', 'e'), (4, 2, 'x', 'x'),
        ]
        for row, col, text, insert in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(38)
            btn.clicked.connect(lambda _, t=insert: self.insert_text(t))
            keyboard_layout.addWidget(btn, row, col)

        # Function buttons
        func_buttons = [
            ('sin', 'sin()'), ('cos', 'cos()'), ('tan', 'tan()'), ('exp', 'exp()'),
            ('log', 'log()'), ('ln', 'ln()'), ('sqrt', 'sqrt()'), ('abs', 'abs()'),
            ('sign', 'sign()'), ('sinh', 'sinh()'), ('cosh', 'cosh()'), ('tanh', 'tanh()')
        ]
        for idx, (label, func) in enumerate(func_buttons):
            btn = QPushButton(label)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda _, f=func: self.insert_function(f))
            keyboard_layout.addWidget(btn, 5 + idx // 6, idx % 6)

        # Edit buttons
        back_btn = QPushButton("⌫ Retroceso")
        back_btn.clicked.connect(self.backspace)
        keyboard_layout.addWidget(back_btn, 7, 0, 1, 2)
        clear_btn = QPushButton("Limpiar Todo")
        clear_btn.clicked.connect(self.clear_entry)
        keyboard_layout.addWidget(clear_btn, 7, 2, 1, 2)

        # Preview
        self.preview_label = QLabel("f(x) = ...")
        self.preview_label.setFont(QFont("Consolas", 14))
        main_layout.addWidget(self.preview_label)

        # Validation
        self.validation_label = QLabel("...")
        main_layout.addWidget(self.validation_label)

        # Buttons (Accept, Cancel, Reset)
        button_layout = QHBoxLayout()
        accept_btn = QPushButton("Aceptar")
        accept_btn.clicked.connect(self.accept_function)
        button_layout.addWidget(accept_btn)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        reset_btn = QPushButton("Restaurar Predeterminada")
        reset_btn.clicked.connect(self.reset_to_default)
        button_layout.addWidget(reset_btn)
        main_layout.addLayout(button_layout)

        self.update_preview()

    def insert_text(self, text_to_insert):
        self.function_entry.insert(text_to_insert)
        self.function_entry.setFocus()

    def insert_function(self, func_text):
        cursor_pos = self.function_entry.cursorPosition()
        self.function_entry.insert(func_text)
        # Move cursor inside the parentheses
        self.function_entry.setCursorPosition(cursor_pos + len(func_text) - 1)
        self.function_entry.setFocus()

    def backspace(self):
        cursor_pos = self.function_entry.cursorPosition()
        if cursor_pos > 0:
            text = self.function_entry.text()
            new_text = text[:cursor_pos - 1] + text[cursor_pos:]
            self.function_entry.setText(new_text)
            self.function_entry.setCursorPosition(cursor_pos - 1)
        self.function_entry.setFocus()

    def clear_entry(self):
        self.function_entry.clear()
        self.function_entry.setFocus()

    def update_preview_and_validate(self):
        self.update_preview()
        self.validate_function()

    def update_preview(self):
        func_text = self.function_entry.text()
        preview_text = func_text.replace('*', '·').replace('/', '÷').replace('sqrt', '√')
        self.preview_label.setText(f"f(x) = {preview_text}")

    def reset_to_default(self):
        self.function_entry.setText(self.default_function)
        self.validate_function()

    def validate_function(self):
        func_text = self.function_entry.text()
        if not func_text.strip():
            self.validation_label.setText("⚠️ Ingrese una función válida")
            self.validation_label.setStyleSheet("color: orange;")
            return False
        try:
            eval_text = func_text.replace('π', 'pi').replace('^', '**').replace('ln(', 'log(')
            x = symbols('x')
            expr = sympify(eval_text)
            self.compiled_function_result = lambdify(
                x, expr, ['numpy', {'ln': np.log, 'log': np.log10, 'abs': np.abs, 'sign': np.sign}]
            )
            test_value = np.array([1.5, 0.0, -1.5])
            result = self.compiled_function_result(test_value)
            if np.all(np.isfinite(result)) and not np.any(np.isnan(result)):
                self.validation_label.setText("✅ Función válida")
                self.validation_label.setStyleSheet("color: green;")
                return True
            else:
                self.validation_label.setText("⚠️ La función produce valores no válidos (NaN, Inf)")
                self.validation_label.setStyleSheet("color: orange;")
                return False
        except SympifyError:
            self.validation_label.setText("❌ Error de sintaxis en la función.")
            self.validation_label.setStyleSheet("color: red;")
            return False
        except Exception as e:
            self.validation_label.setText(f"❌ Error: {type(e).__name__}")
            self.validation_label.setStyleSheet("color: red;")
            return False

    def accept_function(self):
        if self.validate_function():
            if self.callback_function:
                self.callback_function(self.function_entry.text(), self.compiled_function_result)
            self.accept()
        else:
            QMessageBox.critical(self, "Error de Validación", "La función no es válida.")

# Adaptador para math_functions.py
class CustomFunctionProvider:
    def __init__(self):
        self.function_text = "ln(1+abs(x**7)) + pi*cos(x) + sin(15.5*x)"
        self.compiled_function = None
        self._compile_current_function()

    def _compile_current_function(self):
        try:
            eval_text = self.function_text.replace('π', 'pi').replace('^', '**').replace('ln(','log(')
            x_sym = symbols('x')
            expr = sympify(eval_text)
            numpy_modules = ['numpy', {'abs': np.abs, 'sign': np.sign}]
            self.compiled_function = lambdify(x_sym, expr, modules=numpy_modules)
        except Exception:
            print(f"Warning: Failed to compile '{self.function_text}'. Using x**2 as fallback.")
            x_sym = symbols('x')
            self.compiled_function = lambdify(x_sym, x_sym**2, modules=['numpy'])

    def set_function(self, text, compiled_func):
        self.function_text = text
        self.compiled_function = compiled_func

    def evaluate(self, x_val, is_minimizing):
        if not self.compiled_function:
            self._compile_current_function()
            if not self.compiled_function:
                raise ValueError("Función objetivo no compilada o no válida.")
        raw_value = self.get_raw_function_value(x_val)
        return -raw_value if is_minimizing else raw_value

    def get_raw_function_value(self, x_val):
        if not self.compiled_function:
            self._compile_current_function()
            if not self.compiled_function:
                raise ValueError("Función objetivo no compilada o no válida.")
        try:
            return float(self.compiled_function(x_val))
        except Exception as e:
            print(f"Error evaluating function '{self.function_text}' at x={x_val}: {e}")
            return np.nan