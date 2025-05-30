#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel de configuración de la aplicación
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from utils.math_functions import set_function_provider  # Para asegurar que el provider global se actualice

class ConfigPanel:
    """Clase que maneja el panel de configuración (izquierdo)"""
    
    # Se le pasa el function_provider desde MainWindow
    def __init__(self, parent, main_window, function_provider_instance):
        self.parent = parent
        self.main_window = main_window
        self.function_provider = function_provider_instance  # Usar el provider de MainWindow
        set_function_provider(self.function_provider)  # Asegurarse de que math_functions use este provider
        
        self.interval_a = tk.DoubleVar(value=-43.90)
        self.interval_b = tk.DoubleVar(value=-35.70)
        self.delta_x = tk.DoubleVar(value=0.08)
        self.pop_size = tk.IntVar(value=20)
        self.num_generations = tk.IntVar(value=100)
        self.prob_crossover = tk.DoubleVar(value=0.90)
        self.prob_mutation_i = tk.DoubleVar(value=0.25)
        self.prob_mutation_g = tk.DoubleVar(value=0.25)
        self.is_minimizing = tk.BooleanVar(value=True)
        self.num_points = tk.StringVar(value="...")
        self.num_bits = tk.StringVar(value="...")
        self.max_decimal = tk.StringVar(value="...")
        self.selected_graph = tk.StringVar(value="none")
        self.graph_buttons = []
        
        self.create_config_panel()
        self.update_function_display()  # Para mostrar la función inicial del provider
        self.update_calculated_values()
        
    def open_function_editor(self):
        from ui.function_editor import FunctionEditor
        
        def on_function_accept(function_text, compiled_function):
            self.function_provider.set_function(function_text, compiled_function)
            set_function_provider(self.function_provider)  # Actualizar el provider global
            self.update_function_display()
            messagebox.showinfo("Función Actualizada", 
                              "La función objetivo ha sido actualizada para el visualizador y el AG de ejemplo.")
        
        FunctionEditor(self.parent, on_function_accept, initial_function=self.function_provider.function_text)
    
    def update_function_display(self):
        function_text = self.function_provider.function_text
        display_text = function_text.replace('*', '·')
        self.function_display.config(text=f"f(x) = {display_text}")
    
    def create_config_panel(self):
        canvas = tk.Canvas(self.parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        title_label = tk.Label(scrollable_frame, text="Configuración", 
                              font=("Arial", 16, "bold"), bg='white')
        title_label.pack(pady=10)
        
        function_frame = tk.LabelFrame(scrollable_frame, text="Función Objetivo (para AG de Ejemplo y Visualizador)", 
                                    font=("Arial", 12, "bold"), 
                                    bg='white', padx=10, pady=10)
        function_frame.pack(fill="x", padx=10, pady=5)
        
        self.function_display = tk.Label(function_frame, 
                                        text="",  # Se actualizará en update_function_display
                                        font=("Consolas", 10), bg='white',
                                        wraplength=380, justify="left")
        self.function_display.pack(fill="x", pady=5)
        
        edit_function_btn = tk.Button(function_frame, text="Editar Función", 
                                    command=self.open_function_editor,
                                    bg='#2196F3', fg='white', 
                                    font=("Arial", 11, "bold"))
        edit_function_btn.pack(fill="x", pady=5)
        
        config_frame = tk.LabelFrame(scrollable_frame, text="Parámetros (para AG de Ejemplo)", 
                                    font=("Arial", 12, "bold"), 
                                    bg='white', padx=10, pady=10)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_labeled_entry(config_frame, "Intervalo A:", self.interval_a)
        self.create_labeled_entry(config_frame, "Intervalo B:", self.interval_b)
        self.create_labeled_entry(config_frame, "Δx:", self.delta_x)
        self.create_labeled_entry(config_frame, "Población:", self.pop_size)
        self.create_labeled_entry(config_frame, "Generaciones:", self.num_generations)
        self.create_labeled_entry(config_frame, "Prob. Cruzamiento:", self.prob_crossover)
        self.create_labeled_entry(config_frame, "PMI (Individuo):", self.prob_mutation_i)
        self.create_labeled_entry(config_frame, "PMG (Gen):", self.prob_mutation_g)
        
        optimization_frame = tk.Frame(config_frame, bg='white')
        optimization_frame.pack(fill="x", pady=5)
        tk.Label(optimization_frame, text="Modo de optimización:", 
                bg='white', font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Radiobutton(optimization_frame, text="Minimizar", variable=self.is_minimizing, 
                      value=True, bg='white').pack(side="left", padx=5)
        tk.Radiobutton(optimization_frame, text="Maximizar", variable=self.is_minimizing, 
                      value=False, bg='white').pack(side="left", padx=5)
        
        info_frame = tk.LabelFrame(config_frame, text="Parámetros Calculados", 
                                  font=("Arial", 10, "bold"), bg='white')
        info_frame.pack(fill="x", pady=10)
        self.create_info_display(info_frame, "# Puntos:", self.num_points)
        self.create_info_display(info_frame, "# Bits:", self.num_bits)
        self.create_info_display(info_frame, "Máx. Decimal:", self.max_decimal)
        
        execute_btn = tk.Button(config_frame, text="EJECUTAR AG DE EJEMPLO",
                               command=self.run_example_algorithm_from_config,
                               bg='#4CAF50', fg='white', 
                               font=("Arial", 12, "bold"),
                               height=2)
        execute_btn.pack(fill="x", pady=20)
        
        separator = tk.Frame(scrollable_frame, height=2, bg='gray')
        separator.pack(fill="x", padx=10, pady=10)
        
        graph_frame = tk.LabelFrame(scrollable_frame, text="Seleccionar Gráfica", 
                                   font=("Arial", 12, "bold"), 
                                   bg='white', padx=10, pady=10)
        graph_frame.pack(fill="x", padx=10, pady=5)
        self.create_graph_button(graph_frame, "Función Objetivo", "objective")
        self.create_graph_button(graph_frame, "Evolución Mejor", "evolution_best")
        self.create_graph_button(graph_frame, "Evolución Población", "evolution_all")
        self.animation_btn = tk.Button(graph_frame, text="Evolución Animada", 
                                     command=self.start_animation,
                                     bg='white', relief='raised', bd=2,
                                     font=("Arial", 11), height=2,
                                     activebackground='#e0e0e0')
        self.animation_btn.pack(fill="x", pady=5)
        self.graph_buttons.append(self.animation_btn)
        
        actions_frame = tk.LabelFrame(scrollable_frame, text="Acciones", 
                                     font=("Arial", 12, "bold"), 
                                     bg='white', padx=10, pady=10)
        actions_frame.pack(fill="x", padx=10, pady=5)
        self.report_btn = tk.Button(actions_frame, text="Generar Reporte", 
                                   command=self.generate_report,
                                   bg='#FF9800', fg='white', 
                                   font=("Arial", 11, "bold"), height=1)
        self.report_btn.pack(fill="x", pady=5)
        self.download_animation_btn = tk.Button(actions_frame, text="Descargar Animación", 
                                             command=self.save_animation,
                                             bg='#2196F3', fg='white', 
                                             font=("Arial", 11, "bold"), height=1)
        self.download_animation_btn.pack(fill="x", pady=5)
        clear_btn = tk.Button(actions_frame, text="Limpiar Resultados", 
                             command=self.clear_results,
                             bg='#f44336', fg='white', 
                             font=("Arial", 11, "bold"), height=1)
        clear_btn.pack(fill="x", pady=5)
        
        self.disable_buttons()
        for var in [self.interval_a, self.interval_b, self.delta_x]:
            var.trace('w', lambda *args: self.update_calculated_values())
    
    def create_labeled_entry(self, parent, label, variable):
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=label, bg='white', width=20, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=variable, width=15).pack(side="right")
    
    def create_info_display(self, parent, label, variable):
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=1)
        tk.Label(frame, text=label, bg='white', width=15, anchor="w").pack(side="left")
        info_label = tk.Label(frame, textvariable=variable, bg='#f0f0f0', 
                             relief="sunken", bd=1, width=15)
        info_label.pack(side="right")

    def create_graph_button(self, parent, text, value):
        btn = tk.Button(parent, text=text, 
                       command=lambda: self.show_graph(value),
                       bg='white', relief='raised', bd=2,
                       font=("Arial", 11), height=2,
                       activebackground='#e0e0e0')
        btn.pack(fill="x", pady=5)
        self.graph_buttons.append(btn)

    def update_calculated_values(self):
        try:
            try:
                x_min = float(self.interval_a.get())
                x_max = float(self.interval_b.get())
                delta_x = float(self.delta_x.get())
            except (ValueError, tk.TclError):
                self.num_points.set("...")
                self.num_bits.set("...")
                self.max_decimal.set("...")
                return
            
            if x_max > x_min and delta_x > 0:
                if x_min == 0 and x_max == 31:
                    n_bits = 5
                elif x_min >= 0 and x_max == int(x_max) and delta_x == 1.0:
                    range_size = int(x_max - x_min) + 1
                    n_bits = int(np.ceil(np.log2(range_size)))
                else:
                    num_divisions = int((x_max - x_min) / delta_x)
                    n_bits = int(np.ceil(np.log2(num_divisions + 1)))
                
                max_decimal = 2**n_bits - 1
                num_points = max_decimal + 1
                
                self.num_points.set(str(num_points))
                self.num_bits.set(str(n_bits))
                self.max_decimal.set(str(max_decimal))
            else:
                self.num_points.set("...")
                self.num_bits.set("...")
                self.max_decimal.set("...")
        except Exception as e:
            self.num_points.set("...")
            self.num_bits.set("...")
            self.max_decimal.set("...")

    def enable_buttons(self):
        for btn in self.graph_buttons:
            btn.config(state="normal")
        self.report_btn.config(state="normal")
        self.download_animation_btn.config(state="normal")

    def disable_buttons(self):
        for btn in self.graph_buttons:
            btn.config(state="disabled")
        self.report_btn.config(state="disabled")
        self.download_animation_btn.config(state="disabled")

    def update_button_selection(self, selected_type):
        button_mapping = {
            "objective": 0,
            "evolution_best": 1,
            "evolution_all": 2
        }
        for i, btn in enumerate(self.graph_buttons[:-1]):
            if i == button_mapping.get(selected_type, -1):
                btn.config(bg='#cce0ff', relief='sunken')
            else:
                btn.config(bg='white', relief='raised')
        self.animation_btn.config(text="Evolución Animada", bg='white')
    
    def run_example_algorithm_from_config(self):
        """Recoge los parámetros y solicita la ejecución del AG de ejemplo"""
        x_min = self.interval_a.get()
        x_max = self.interval_b.get()
        delta_x = self.delta_x.get()
        
        if x_min >= x_max:
            tk.messagebox.showerror("Error", "El intervalo [a,b] no es válido. a debe ser menor que b.")
            return
        if delta_x <= 0:
            tk.messagebox.showerror("Error", "Δx debe ser mayor que 0.")
            return
        
        params = {
            'interval_a': x_min, 'interval_b': x_max, 'delta_x': delta_x,
            'pop_size': self.pop_size.get(), 
            'num_generations': self.num_generations.get(),
            'prob_crossover': self.prob_crossover.get(),
            'prob_mutation_i': self.prob_mutation_i.get(),
            'prob_mutation_g': self.prob_mutation_g.get(),
            'is_minimizing': self.is_minimizing.get()
        }
        self.main_window.run_example_algorithm(params)
    
    def show_graph(self, graph_type):
        if not self.main_window.ga_results:
            tk.messagebox.showwarning("Advertencia", "Primero debe ejecutar el AG de ejemplo o cargar resultados.")
            return
        self.update_button_selection(graph_type)
        self.main_window.visualization_panel.show_graph(
            graph_type, 
            self.main_window.ga_results, 
            self.main_window.population_history, 
            self.main_window.fitness_history, 
            self.main_window.best_fitness_history
        )
    
    def start_animation(self):
        if not self.main_window.ga_results:
            tk.messagebox.showwarning("Advertencia", "Primero debe ejecutar el AG de ejemplo o cargar resultados.")
            return
        if self.animation_btn.cget('text') == "Evolución Animada":
            self.animation_btn.config(text="Detener Animación", bg='#ffcccc')
            for btn in self.graph_buttons[:-1]:
                btn.config(bg='white', relief='raised')
            self.main_window.visualization_panel.start_animation(
                self.main_window.best_fitness_history,
                self.main_window.ga_results['is_minimizing']
            )
        else:
            self.animation_btn.config(text="Evolución Animada", bg='white')
            self.main_window.visualization_panel.stop_animation()

    def generate_report(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Guardar Reporte"
        )
        if not filename: return
        success = self.main_window.generate_report(filename)
        if success:
            if hasattr(self.main_window.report_generator, 'open_file'):
                self.main_window.report_generator.open_file(filename)
            else:
                try:
                    import os, subprocess
                    if os.name == 'nt': os.startfile(filename)
                    else: subprocess.call(('open', filename) if os.uname().sysname == 'Darwin' else ('xdg-open', filename))
                except Exception as e:
                    messagebox.showwarning("Abrir archivo", f"No se pudo abrir el reporte automáticamente: {e}")

    def save_animation(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("GIF files", "*.gif"), ("All files", "*.*")],
            title="Guardar Animación"
        )
        if not filename: return
        self.main_window.save_animation(filename)

    def clear_results(self):
        self.main_window.clear_results()