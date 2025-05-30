#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel de visualización de gráficas
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.math_functions import binary_to_decimal

class VisualizationPanel:
    """Clase que maneja el panel de visualización (derecho)"""
    
    def __init__(self, parent, main_window):
        """Inicializa el panel de visualización"""
        self.parent = parent
        self.main_window = main_window
        
        # Referencias para gráficas
        self.graph_container = None
        self.current_canvas = None
        self.current_figure = None
        
        # Variables para animación
        self.is_animating = False
        self.animation_generation = 0
        self.ax = None
        self.line = None
        self.gen_text = None
        self.fitness_text = None
        
        # Crear interfaz
        self.create_visualization_panel()
    
    def create_visualization_panel(self):
        """Crea el panel de visualización"""
        # Frame para la gráfica con borde
        self.graph_container = tk.Frame(self.parent, bg='white', relief='sunken', bd=2)
        self.graph_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mensaje inicial
        self.create_welcome_message()
    
    def create_welcome_message(self):
        """Crea el mensaje de bienvenida"""
        welcome_frame = tk.Frame(self.graph_container, bg='white')
        welcome_frame.pack(expand=True)
        
        welcome_text = """
        Algoritmo Genético
        Con función objetivo personalizable
        
        1. Configure o edite la función objetivo
        2. Configure los parámetros
        3. Seleccione modo (Maximizar o Minimizar)
        4. Ejecute el algoritmo
        5. Seleccione una gráfica para visualizar
        """
        
        tk.Label(welcome_frame, text=welcome_text, 
                font=("Arial", 16), bg='white',
                justify="center").pack(expand=True)
    
    def clear_graph_area(self):
        """Limpia el área de gráficas"""
        # Detener cualquier animación en curso
        self.is_animating = False
            
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        
        if self.current_figure:
            plt.close(self.current_figure)
            self.current_figure = None
    
    def show_graph(self, graph_type, ga_results, population_history, fitness_history, best_fitness_history):
        """Muestra la gráfica seleccionada"""
        # Limpiar área de gráficas
        self.clear_graph_area()
        
        # Crear la gráfica correspondiente
        self.current_figure = Figure(figsize=(14, 9), dpi=100)
        
        if graph_type == "objective":
            self.create_objective_graph(ga_results)
        elif graph_type == "evolution_best":
            self.create_evolution_best_graph(ga_results, best_fitness_history)
        elif graph_type == "evolution_all":
            self.create_evolution_all_graph(ga_results, population_history, fitness_history)
        
        # Mostrar la gráfica ocupando todo el espacio
        self.current_canvas = FigureCanvasTkAgg(self.current_figure, 
                                               master=self.graph_container)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=0, pady=0)
    
    def create_objective_graph(self, ga_results):
        """Crea la gráfica de la función objetivo"""
        ax = self.current_figure.add_subplot(111)
        
        x_min = ga_results['x_min']
        x_max = ga_results['x_max']
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Obtener la función personalizada para la etiqueta
        from utils.math_functions import get_function_provider
        function_provider = get_function_provider()
        function_text = function_provider.function_text
        
        # Mejorar la presentación
        display_text = function_text
        display_text = display_text.replace('*', '·')
        display_text = display_text.replace('pi', 'π')
        
        # Usar el raw_function_value (siempre es positivo)
        y_vals = [get_function_provider().get_raw_function_value(x) for x in x_vals]
        
        # Determinar el texto del modo
        mode_text = "Minimizando" if ga_results['is_minimizing'] else "Maximizando"
        
        ax.plot(x_vals, y_vals, 'b-', linewidth=3, 
               label=f'f(x) = {display_text}')
        ax.axvline(ga_results['best_x'], color='red', linestyle='--', 
                  linewidth=3, label=f'Mejor: x = {ga_results["best_x"]:.3f}')
        ax.scatter([ga_results['best_x']], [ga_results['objective_function_raw']], 
                  color='red', s=200, zorder=5, 
                  label=f'f(x) = {ga_results["objective_function_raw"]:.3f}')
        
        ax.set_xlabel('x', fontsize=16)
        ax.set_ylabel('f(x)', fontsize=16)
        ax.set_title(f'Función Objetivo y Mejor Solución ({mode_text})', fontsize=18, fontweight='bold')
        ax.legend(fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=12)
        
        # Ajustar márgenes para aprovechar todo el espacio
        self.current_figure.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
    
    def create_evolution_best_graph(self, ga_results, best_fitness_history):
        """Crea la gráfica de evolución del mejor individuo"""
        ax = self.current_figure.add_subplot(111)
        
        generations = range(len(best_fitness_history))
        y_vals = best_fitness_history.copy()
        
        ax.plot(generations, y_vals, 'g-', 
               linewidth=3, marker='o', markersize=8)
        
        # Determinar mejoras según modo de optimización
        if ga_results['is_minimizing']:
            # Para minimización, mejora cuando el valor disminuye
            for i in range(1, len(best_fitness_history)):
                if best_fitness_history[i] < best_fitness_history[i-1]:
                    ax.scatter(i, y_vals[i], 
                              color='orange', s=120, zorder=5)
            
            # Determinar mejora total (minimización: mejora cuando disminuye)
            improvement = best_fitness_history[0] - best_fitness_history[-1]
            mode_text = "Minimizando"
        else:
            # Para maximización, mejora cuando el valor aumenta
            for i in range(1, len(best_fitness_history)):
                if best_fitness_history[i] > best_fitness_history[i-1]:
                    ax.scatter(i, y_vals[i], 
                              color='orange', s=120, zorder=5)
            
            # Determinar mejora total (maximización: mejora cuando aumenta)
            improvement = best_fitness_history[-1] - best_fitness_history[0]
            mode_text = "Maximizando"
        
        ax.set_xlabel('Generación', fontsize=16)
        ax.set_ylabel('Mejor Fitness (Valor real de f(x))', fontsize=16)
        ax.set_title(f'Evolución del Mejor Individuo ({mode_text})', fontsize=18, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=12)
        
        # Añadir estadísticas
        ax.text(0.02, 0.98, f'Mejora total: {improvement:.4f}', 
               transform=ax.transAxes, fontsize=14, 
               verticalalignment='top', 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Ajustar márgenes
        self.current_figure.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
    
    def create_evolution_all_graph(self, ga_results, population_history, fitness_history):
        """Crea la gráfica de evolución de toda la población"""
        ax = self.current_figure.add_subplot(111)
        
        # Preparar datos
        all_x_values = []
        generation_numbers = []
        all_fitness_values = []
        
        for gen, (gen_pop, fitness_scores) in enumerate(zip(population_history, fitness_history)):
            for individual, fitness in zip(gen_pop, fitness_scores):
                x_val = binary_to_decimal(individual, 
                                         ga_results['x_min'], 
                                         ga_results['x_max'], 
                                         ga_results['n_bits'])
                all_x_values.append(x_val)
                generation_numbers.append(gen)
                all_fitness_values.append(fitness)
        
        # Crear scatter plot
        scatter = ax.scatter(all_x_values, generation_numbers, 
                           c=all_fitness_values, cmap='viridis', 
                           alpha=0.7, s=60)
        
        # Colorbar
        cbar = self.current_figure.colorbar(scatter, ax=ax)
        cbar.set_label('Fitness (Valor real de f(x))', fontsize=14)
        
        # Línea del mejor de cada generación
        best_x_history = []
        for gen_pop, fitness_scores in zip(population_history, fitness_history):
            if ga_results['is_minimizing']:
                # Para minimización, el mejor es el mínimo
                best_idx = fitness_scores.index(min(fitness_scores))
            else:
                # Para maximización, el mejor es el máximo
                best_idx = fitness_scores.index(max(fitness_scores))
                
            best_x = binary_to_decimal(gen_pop[best_idx], 
                                      ga_results['x_min'], 
                                      ga_results['x_max'], 
                                      ga_results['n_bits'])
            best_x_history.append(best_x)
        
        ax.plot(best_x_history, range(len(best_x_history)), 
               'r-', linewidth=3, alpha=0.8, label='Trayectoria del mejor')
        
        # Determinar el texto del modo
        mode_text = "Minimizando" if ga_results['is_minimizing'] else "Maximizando"
        
        ax.set_xlabel('x', fontsize=16)
        ax.set_ylabel('Generación', fontsize=16)
        ax.set_title(f'Evolución de Toda la Población ({mode_text})', fontsize=18, fontweight='bold')
        ax.legend(fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=12)
        
        # Ajustar márgenes
        self.current_figure.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.15)
    
    def start_animation(self, best_fitness_history, is_minimizing):
        """Inicia la animación paso a paso de la evolución"""
        # Limpiar área de gráficas
        self.clear_graph_area()
        
        # Crear la figura para la animación
        self.current_figure = Figure(figsize=(14, 9), dpi=100)
        self.ax = self.current_figure.add_subplot(111)
        
        # Determinar el texto del modo
        mode_text = "Minimizando" if is_minimizing else "Maximizando"
        
        # Configuración inicial de la gráfica
        self.ax.set_xlabel('Generación', fontsize=16)
        self.ax.set_ylabel('Mejor Fitness (Valor real de f(x))', fontsize=16)
        self.ax.set_title(f'Evolución del Mejor Individuo - Animación ({mode_text})', 
                         fontsize=18, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        
        y_vals = best_fitness_history.copy()
        
        # Configurar límites para mantener la gráfica estable
        min_fitness = min(y_vals)
        max_fitness = max(y_vals)
        padding = (max_fitness - min_fitness) * 0.1 if max_fitness > min_fitness else 1
        self.ax.set_ylim(min_fitness - padding, max_fitness + padding)
        self.ax.set_xlim(-1, len(best_fitness_history))
        
        # Crear línea para la animación (inicialmente vacía)
        self.line, = self.ax.plot([], [], 'g-', linewidth=3, marker='o', markersize=8)
        
        # Añadir etiqueta de generación actual
        self.gen_text = self.ax.text(0.02, 0.98, 'Generación: 0', 
                                    transform=self.ax.transAxes, fontsize=14,
                                    verticalalignment='top',
                                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Añadir etiqueta de fitness actual
        self.fitness_text = self.ax.text(0.02, 0.90, f'Fitness: {best_fitness_history[0]:.4f}', 
                                        transform=self.ax.transAxes, fontsize=14,
                                        verticalalignment='top',
                                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Ajustar márgenes
        self.current_figure.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        
        # Mostrar la gráfica
        self.current_canvas = FigureCanvasTkAgg(self.current_figure, 
                                               master=self.graph_container)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=0, pady=0)
        
        # Iniciar animación
        self.animation_generation = 0
        self.is_animating = True
        self.animate_step(best_fitness_history, is_minimizing)
    
    def animate_step(self, best_fitness_history, is_minimizing):
        """Ejecuta un paso de la animación"""
        if not self.is_animating or self.animation_generation >= len(best_fitness_history):
            self.is_animating = False
            return
        
        # Actualizar datos
        x_data = list(range(self.animation_generation + 1))
        y_data = best_fitness_history[:self.animation_generation + 1]
        
        # Actualizar línea
        self.line.set_data(x_data, y_data)
        
        # Actualizar textos informativos
        self.gen_text.set_text(f'Generación: {self.animation_generation + 1}')
        self.fitness_text.set_text(f'Fitness: {best_fitness_history[self.animation_generation]:.4f}')
        
        # Resaltar mejoras según modo de optimización
        if self.animation_generation > 0:
            if is_minimizing:
                # Para minimización, mejora cuando el valor disminuye
                if best_fitness_history[self.animation_generation] < best_fitness_history[self.animation_generation-1]:
                    self.ax.scatter([self.animation_generation], 
                                   [y_data[self.animation_generation]], 
                                   color='orange', s=120, zorder=5)
            else:
                # Para maximización, mejora cuando el valor aumenta
                if best_fitness_history[self.animation_generation] > best_fitness_history[self.animation_generation-1]:
                    self.ax.scatter([self.animation_generation], 
                                   [y_data[self.animation_generation]], 
                                   color='orange', s=120, zorder=5)
        
        # Actualizar canvas
        self.current_canvas.draw()
        
        # Incrementar contador
        self.animation_generation += 1
        
        # Programar siguiente paso (velocidad ajustable)
        delay_ms = 200  # Velocidad de la animación
        if self.is_animating:
            self.parent.after(delay_ms, lambda: self.animate_step(best_fitness_history, is_minimizing))
    
    def stop_animation(self):
        """Detiene la animación en curso"""
        self.is_animating = False