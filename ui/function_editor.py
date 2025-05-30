#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor de funciones con teclado virtual
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import numpy as np
from sympy import symbols, sympify, lambdify, SympifyError

class FunctionEditor:
    """Editor de funciones con teclado virtual"""
    
    # Añadir initial_function
    def __init__(self, parent, callback_function=None, initial_function=None):
        """
        Inicializa el editor de funciones
        
        Args:
            parent: Widget padre
            callback_function: Función a llamar cuando se acepta una función
            initial_function: Texto de función inicial (opcional)
        """
        self.parent = parent
        self.callback_function = callback_function
        self.default_function = "ln(1+abs(x^7)) + π*cos(x) + sin(15.5*x)"
        
        # Usar initial_function si se provee, sino la default
        current_initial = initial_function if initial_function is not None else self.default_function
        self.current_function = tk.StringVar(value=current_initial)
        
        self.compiled_function = None
        
        # Crear la ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editor de Funciones")
        self.dialog.geometry("850x650")  # Aumentar el tamaño para asegurar visibilidad
        self.dialog.minsize(800, 600)    # Establecer un tamaño mínimo
        self.dialog.resizable(True, True)
        self.dialog.configure(bg='#f5f5f5')
        
        # Hacer que la ventana sea modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar en la pantalla
        self.center_window()
        
        # Crear la interfaz
        self.create_interface()
        
        # Validar la función inicial
        self.validate_function()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_interface(self):
        """Crea la interfaz del editor de funciones"""
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#f5f5f5')
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Crear un canvas y scrollbar para el scroll principal
        canvas = tk.Canvas(main_frame, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')
        
        # Configurar el scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Permitir scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux
        
        # Empaquetar el canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title_label = tk.Label(scrollable_frame, text="Editor de Función Objetivo", 
                              font=("Arial", 16, "bold"), bg='#f5f5f5')
        title_label.pack(pady=(0, 15))
        
        # Frame para el editor
        editor_frame = tk.LabelFrame(scrollable_frame, text="Función f(x)", 
                                    font=("Arial", 12, "bold"), 
                                    bg='#f5f5f5', padx=10, pady=10)
        editor_frame.pack(fill="x", pady=10)
        
        # Entrada de texto para la función
        self.function_entry = tk.Entry(editor_frame, textvariable=self.current_function, 
                                      font=("Consolas", 14), width=50)
        self.function_entry.pack(fill="x", pady=5)
        
        # Frame para el teclado virtual
        keyboard_frame = tk.LabelFrame(scrollable_frame, text="Teclado Virtual", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#f5f5f5', padx=10, pady=10)
        keyboard_frame.pack(fill="x", pady=10)
        
        # Crear el teclado virtual
        self.create_virtual_keyboard(keyboard_frame)
        
        # Frame para la previsualización
        preview_frame = tk.LabelFrame(scrollable_frame, text="Previsualización", 
                                     font=("Arial", 12, "bold"), 
                                     bg='#f5f5f5', padx=10, pady=10)
        preview_frame.pack(fill="x", pady=10)
        
        # Label para mostrar la función en notación matemática
        self.preview_label = tk.Label(preview_frame, text="", 
                                     font=("Consolas", 14), bg='white', 
                                     relief="sunken", bd=1)
        self.preview_label.pack(fill="x", pady=5, ipady=5)
        
        # Frame para validación y botones
        validation_frame = tk.Frame(scrollable_frame, bg='#f5f5f5')
        validation_frame.pack(fill="x", pady=10)
        
        # Texto de validación
        self.validation_text = tk.StringVar(value="")
        validation_label = tk.Label(validation_frame, textvariable=self.validation_text, 
                                   font=("Arial", 12), fg='green', bg='#f5f5f5')
        validation_label.pack(side="left", padx=5)
        
        # Botones
        button_frame = tk.Frame(scrollable_frame, bg='#f5f5f5')
        button_frame.pack(fill="x", pady=10)
        
        reset_btn = tk.Button(button_frame, text="Restaurar Predeterminada", 
                             command=self.reset_to_default,
                             bg='#FF9800', fg='white', 
                             font=("Arial", 11, "bold"),
                             padx=10, pady=5)
        reset_btn.pack(side="left", padx=5)
        
        validate_btn = tk.Button(button_frame, text="Validar Función", 
                               command=self.validate_function,
                               bg='#2196F3', fg='white', 
                               font=("Arial", 11, "bold"),
                               padx=10, pady=5)
        validate_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancelar", 
                             command=self.dialog.destroy,
                             bg='#f44336', fg='white', 
                             font=("Arial", 11, "bold"),
                             padx=10, pady=5)
        cancel_btn.pack(side="right", padx=5)
        
        accept_btn = tk.Button(button_frame, text="Aceptar", 
                             command=self.accept_function,
                             bg='#4CAF50', fg='white', 
                             font=("Arial", 11, "bold"),
                             padx=10, pady=5)
        accept_btn.pack(side="right", padx=5)
        
        # Vincular eventos
        self.current_function.trace('w', lambda *args: self.update_preview())
        
        # Actualizar previsualización inicial
        self.update_preview()
    
    def create_virtual_keyboard(self, parent):
        """Crea el teclado virtual con botones matemáticos"""
        # Definir conjuntos de botones
        operators = ['+', '-', '*', '/', '^', '=', '(', ')', ',', '.']
        numbers = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0']
        functions_trig = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        functions_other = ['exp', 'log', 'ln', 'sqrt', 'abs', 'sign']
        functions_hyp = ['sinh', 'cosh', 'tanh']
        constants = ['π', 'e', 'x', 'i']
        
        # Frame principal para el teclado - usando grid para mejor organización
        keyboard_container = tk.Frame(parent, bg='#f5f5f5')
        keyboard_container.pack(fill="x", pady=5)
        
        # Sección 1: Números y operadores básicos
        basic_section = tk.LabelFrame(keyboard_container, text="Números y Operadores", 
                                     bg='#f5f5f5', padx=10, pady=10)
        basic_section.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Contenedor para números
        num_frame = tk.Frame(basic_section, bg='#f5f5f5')
        num_frame.pack(side="left", padx=5)
        
        # Crear grid para números (estilo calculadora)
        row, col = 0, 0
        for num in numbers:
            button = tk.Button(num_frame, text=num, width=4, height=2,
                              command=lambda n=num: self.insert_text(n),
                              font=("Arial", 12), bg='white', relief="raised",
                              activebackground="#e0e0e0")
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Contenedor para operadores básicos
        op_frame = tk.Frame(basic_section, bg='#f5f5f5')
        op_frame.pack(side="left", padx=5)
        
        # Crear grid para operadores
        row, col = 0, 0
        for op in operators:
            button = tk.Button(op_frame, text=op, width=4, height=2,
                              command=lambda o=op: self.insert_text(o),
                              font=("Arial", 12), bg='#e0e0e0', relief="raised",
                              activebackground="#d0d0d0")
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Sección 2: Funciones trigonométricas
        trig_section = tk.LabelFrame(keyboard_container, text="Funciones Trigonométricas", 
                                    bg='#f5f5f5', padx=10, pady=10)
        trig_section.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # Frame para funciones trigonométricas
        trig_frame = tk.Frame(trig_section, bg='#f5f5f5')
        trig_frame.pack(fill="x", pady=5)
        
        # Crear botones de funciones en dos filas
        row, col = 0, 0
        for i, func in enumerate(functions_trig):
            display_text = func + "()"
                
            button = tk.Button(trig_frame, text=display_text, width=6, height=2,
                              command=lambda f=func: self.insert_function(f),
                              font=("Arial", 11), bg='#d1e7f7', relief="raised",
                              activebackground="#b0d4f1")
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 2:  # 3 botones por fila
                col = 0
                row += 1
        
        # Frame para funciones hiperbólicas
        hyp_frame = tk.Frame(trig_section, bg='#f5f5f5')
        hyp_frame.pack(fill="x", pady=5)
        
        for i, func in enumerate(functions_hyp):
            display_text = func + "()"
                
            button = tk.Button(hyp_frame, text=display_text, width=6, height=2,
                              command=lambda f=func: self.insert_function(f),
                              font=("Arial", 11), bg='#e1d7f7', relief="raised",
                              activebackground="#c0b4d1")
            button.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
        
        # Sección 3: Otras funciones
        other_section = tk.LabelFrame(keyboard_container, text="Otras Funciones", 
                                     bg='#f5f5f5', padx=10, pady=10)
        other_section.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Frame para otras funciones
        other_frame = tk.Frame(other_section, bg='#f5f5f5')
        other_frame.pack(fill="x", pady=5)
        
        row, col = 0, 0
        for i, func in enumerate(functions_other):
            display_text = func
            if func != 'abs' and func != 'sign':
                display_text = func + "()"
            else:
                display_text = func + "()"
                
            button = tk.Button(other_frame, text=display_text, width=6, height=2,
                              command=lambda f=func: self.insert_function(f),
                              font=("Arial", 11), bg='#d7f7e1', relief="raised",
                              activebackground="#b4d1c0")
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 2:  # 3 botones por fila
                col = 0
                row += 1
        
        # Sección 4: Constantes y edición
        const_edit_section = tk.LabelFrame(keyboard_container, text="Constantes y Edición", 
                                         bg='#f5f5f5', padx=10, pady=10)
        const_edit_section.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # Contenedor para constantes
        const_frame = tk.Frame(const_edit_section, bg='#f5f5f5')
        const_frame.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Crear botones de constantes en una fila
        for i, const in enumerate(constants):
            button = tk.Button(const_frame, text=const, width=6, height=2,
                              command=lambda c=const: self.insert_text(c),
                              font=("Arial", 11), bg='#f7e6d1', relief="raised",
                              activebackground="#f1d4b0")
            button.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
        
        # Contenedor para botones de edición
        edit_frame = tk.Frame(const_edit_section, bg='#f5f5f5')
        edit_frame.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Crear botones de edición
        backspace_btn = tk.Button(edit_frame, text="⌫ Retroceso", width=12, height=2,
                                 command=self.backspace,
                                 font=("Arial", 11), bg='#ffcccc', relief="raised",
                                 activebackground="#ffaaaa")
        backspace_btn.pack(side="left", padx=2, pady=2)
        
        clear_btn = tk.Button(edit_frame, text="Limpiar Todo", width=12, height=2,
                             command=self.clear_entry,
                             font=("Arial", 11), bg='#ffcccc', relief="raised",
                             activebackground="#ffaaaa")
        clear_btn.pack(side="left", padx=2, pady=2)
        
        # Configurar el comportamiento del grid
        keyboard_container.columnconfigure(0, weight=1)
        keyboard_container.columnconfigure(1, weight=1)
        keyboard_container.rowconfigure(0, weight=1)
        keyboard_container.rowconfigure(1, weight=1)
    
    def insert_text(self, text):
        """Inserta texto en la posición del cursor"""
        current_pos = self.function_entry.index(tk.INSERT)
        self.function_entry.insert(current_pos, text)
        self.function_entry.focus_set()
    
    def insert_function(self, func):
        """Inserta una función con paréntesis en la posición del cursor"""
        current_pos = self.function_entry.index(tk.INSERT)
        if func in ['sin', 'cos', 'tan', 'exp', 'log', 'ln', 'sqrt']:
            self.function_entry.insert(current_pos, f"{func}()")
            # Mover el cursor dentro de los paréntesis
            self.function_entry.icursor(current_pos + len(func) + 1)
        else:
            self.function_entry.insert(current_pos, f"{func}()")
            # Mover el cursor dentro de los paréntesis
            self.function_entry.icursor(current_pos + len(func) + 1)
        
        self.function_entry.focus_set()
    
    def backspace(self):
        """Elimina el carácter anterior al cursor"""
        current_pos = self.function_entry.index(tk.INSERT)
        if current_pos > 0:
            self.function_entry.delete(current_pos - 1, current_pos)
        self.function_entry.focus_set()
    
    def clear_entry(self):
        """Limpia toda la entrada de texto"""
        self.function_entry.delete(0, tk.END)
        self.function_entry.focus_set()
    
    def update_preview(self):
        """Actualiza la previsualización de la función"""
        # Obtener la función actual
        func_text = self.current_function.get()
        
        # Reemplazar símbolos para mejor visualización
        preview_text = func_text
        preview_text = preview_text.replace('π', 'π')  # Asegurarse de que π se muestre correctamente
        preview_text = preview_text.replace('*', '×')
        preview_text = preview_text.replace('/', '÷')
        preview_text = preview_text.replace('sqrt', '√')
        
        # Mostrar en la etiqueta de previsualización
        self.preview_label.config(text=f"f(x) = {preview_text}")
    
    def reset_to_default(self):
        """Restaura la función predeterminada"""
        self.current_function.set(self.default_function)
        self.validate_function()
    
    def validate_function(self):
        """Valida la función ingresada"""
        # Obtener la función actual
        func_text = self.current_function.get()
        
        # Si está vacía
        if not func_text.strip():
            self.validation_text.set("⚠️ Ingrese una función válida")
            self.preview_label.config(fg='red')
            return False
        
        try:
            # Preparar el texto para evaluación
            # Reemplazar símbolos matemáticos
            eval_text = func_text.replace('π', 'pi')
            eval_text = eval_text.replace('^', '**')
            eval_text = eval_text.replace('ln(', 'log(')
            
            # Usar sympy para validar la expresión
            x = symbols('x')
            expr = sympify(eval_text)
            
            # Convertir a una función lambda de numpy para evaluación rápida
            self.compiled_function = lambdify(x, expr, ['numpy', {'ln': np.log, 'log': np.log10}])
            
            # Probar la función con un valor
            test_value = 1.5
            result = self.compiled_function(test_value)
            
            # Si el resultado es un número válido, la función es válida
            if np.isfinite(result) and not np.isnan(result):
                self.validation_text.set("✅ Función válida")
                self.preview_label.config(fg='green')
                return True
            else:
                self.validation_text.set("⚠️ La función produce valores no válidos")
                self.preview_label.config(fg='red')
                return False
                
        except SympifyError as e:
            self.validation_text.set(f"❌ Error de sintaxis: {str(e)}")
            self.preview_label.config(fg='red')
            return False
        except Exception as e:
            self.validation_text.set(f"❌ Error: {str(e)}")
            self.preview_label.config(fg='red')
            return False
    
    def parse_function(self, x_value):
        """Evalúa la función en un valor x dado"""
        if self.compiled_function is None:
            valid = self.validate_function()
            if not valid:
                return None
        
        try:
            result = self.compiled_function(x_value)
            return result
        except Exception:
            return None
    
    def accept_function(self):
        """Acepta la función actual y cierra el diálogo"""
        # Validar una última vez
        valid = self.validate_function()
        
        if valid:
            # Si hay una función de callback, llamarla
            if self.callback_function:
                self.callback_function(self.current_function.get(), self.compiled_function)
            
            # Cerrar el diálogo
            self.dialog.destroy()
        else:
            # Mostrar mensaje de error
            messagebox.showerror("Error de Validación", 
                               "La función ingresada no es válida. Por favor corrija los errores.")


class CustomFunctionProvider:
    """Clase que proporciona una interfaz para funciones personalizadas"""
    
    def __init__(self):
        """Inicializa el proveedor de funciones personalizadas"""
        self.default_function_text = "ln(1+abs(x^7)) + π*cos(x) + sin(15.5*x)"
        self.function_text = self.default_function_text
        self.compiled_function = None
        self.reset_to_default()  # Compilar la función predeterminada al inicio
    
    def set_function(self, function_text, compiled_function):
        self.function_text = function_text
        self.compiled_function = compiled_function
    
    def reset_to_default(self):
        self.function_text = self.default_function_text
        try:
            import sympy
            x = sympy.symbols('x')
            eval_text = self.function_text.replace('π', 'pi').replace('^', '**')
            expr = sympy.sympify(eval_text)
            self.compiled_function = sympy.lambdify(
                x, expr, modules=['numpy', {'ln': np.log, 'log': np.log10, 'abs': np.abs, 'sign': np.sign}]
            )
        except Exception as e:
            print(f"Error compilando función predeterminada en provider: {e}")
            self.compiled_function = None
    
    def _ensure_compiled(self):
        """Asegura que la función esté compilada si es posible."""
        if self.compiled_function is None and self.function_text:
            try:
                import sympy
                x = sympy.symbols('x')
                eval_text = self.function_text.replace('π', 'pi').replace('^', '**')
                expr = sympy.sympify(eval_text)
                self.compiled_function = sympy.lambdify(
                    x, expr, modules=['numpy', {'ln': np.log, 'log': np.log10, 'abs': np.abs, 'sign': np.sign}]
                )
            except Exception as e:
                print(f"Error recompilando función en provider: {e}")
                self.compiled_function = None

    def evaluate(self, x_val, is_minimizing=True):
        self._ensure_compiled()
        if self.compiled_function is None:
            print("Advertencia: Usando función de evaluación de fallback (no compilada).")
            return float('inf') if is_minimizing else float('-inf')
        try:
            result = self.compiled_function(x_val)
            if not np.isfinite(result):
                return float('inf') if is_minimizing else float('-inf')
            return -result if is_minimizing else result
        except Exception as e:
            print(f"Error evaluando función '{self.function_text}' en x={x_val}: {e}")
            return float('inf') if is_minimizing else float('-inf')
    
    def get_raw_function_value(self, x_val):
        self._ensure_compiled()
        if self.compiled_function is None:
            print("Advertencia: Usando función raw de fallback (no compilada).")
            return 0.0
        try:
            result = self.compiled_function(x_val)
            if not np.isfinite(result):
                return 0.0
            return result
        except Exception as e:
            print(f"Error obteniendo raw value de '{self.function_text}' en x={x_val}: {e}")
            return 0.0

if __name__ == "__main__":
    # Prueba del editor de funciones
    root = tk.Tk()
    root.title("Prueba del Editor de Funciones")
    root.geometry("300x200")
    
    def test_callback(function_text, compiled_function):
        print(f"Función aceptada: {function_text}")
        if compiled_function:
            print(f"Prueba de evaluación: f(2) = {compiled_function(2)}")
    
    btn = tk.Button(root, text="Abrir Editor", 
                   command=lambda: FunctionEditor(root, test_callback))
    btn.pack(padx=20, pady=20)
    
    root.mainloop()