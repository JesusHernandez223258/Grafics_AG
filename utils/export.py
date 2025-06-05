#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones para exportar resultados (reportes y animaciones)
"""

import os
import datetime
import subprocess
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from utils.math_functions import binary_to_decimal, get_raw_function_value, get_function_provider

class ReportGenerator:
    """Clase para generar reportes de resultados"""
    
    def __init__(self):
        pass
    
    def generate(self, filename, ga_results, best_fitness_history):
        if ga_results['is_minimizing']:
            mode_text = "MINIMIZACIÓN"
        else:
            mode_text = "MAXIMIZACIÓN"
        
        # Usar la función textual que el AG usó (debe estar en los resultados)
        function_text_from_ga = ga_results.get('function_text_for_report', "Función no especificada por el AG")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write(f"REPORTE ALGORITMO GENÉTICO - {mode_text}\n")
            f.write(f"f(x) = {function_text_from_ga}\n")
            f.write("="*60 + "\n")
            f.write(f"Fecha y hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("PARÁMETROS DE CONFIGURACIÓN (DEL AG EJECUTADO):\n")
            f.write("-" * 30 + "\n")
            f.write(f"• Intervalo: [{ga_results['x_min']}, {ga_results['x_max']}]\n")
            delta_x_approx = (ga_results['x_max'] - ga_results['x_min']) / (2**ga_results['n_bits'] - 1) if (2**ga_results['n_bits'] - 1) != 0 else float('inf')
            f.write(f"• Δx (aprox): {delta_x_approx:.6f}\n")
            f.write(f"• Tamaño de población: {ga_results['pop_size']}\n")
            f.write(f"• Número de generaciones: {ga_results['generations']}\n")
            f.write(f"• Número de bits: {ga_results['n_bits']}\n")
            f.write(f"• Probabilidad de cruzamiento: {ga_results['prob_crossover']}\n")
            f.write(f"• PMI (Probabilidad de mutación individuo): {ga_results['prob_mutation_i']}\n")
            f.write(f"• PMG (Probabilidad de mutación gen): {ga_results['prob_mutation_g']}\n")
            f.write(f"• Modo de optimización: {mode_text}\n\n")
            
            f.write("RESULTADOS PRINCIPALES:\n")
            f.write("-" * 30 + "\n")
            f.write(f"• Mejor solución encontrada: x = {ga_results['best_x']:.6f}\n")
            f.write(f"• Mejor fitness (real): f(x) = {ga_results['best_fitness']:.6f}\n")
            f.write(f"• Individuo binario: {''.join(map(str, ga_results['best_individual']))}\n")
            f.write(f"• Mejora total (sobre fitness real): {ga_results['improvement']:.6f}\n")
            f.write(f"• Mejora promedio por generación: {ga_results['improvement']/ga_results['generations'] if ga_results['generations'] > 0 else 0:.6f}\n\n")
            
            f.write("ANÁLISIS DE CONVERGENCIA (SOBRE FITNESS REAL):\n")
            f.write("-" * 30 + "\n")
            if best_fitness_history:
                f.write(f"• Fitness inicial (real): {best_fitness_history[0]:.6f}\n")
                f.write(f"• Fitness final (real): {best_fitness_history[-1]:.6f}\n")
            else:
                f.write("• Fitness inicial (real): N/A\n")
                f.write("• Fitness final (real): N/A\n")
            
            significant_improvements = 0
            if ga_results['is_minimizing']:
                for i in range(1, len(best_fitness_history)):
                    if best_fitness_history[i] < best_fitness_history[i-1]:
                        significant_improvements += 1
            else:
                for i in range(1, len(best_fitness_history)):
                    if best_fitness_history[i] > best_fitness_history[i-1]:
                        significant_improvements += 1
            percent_productive = (significant_improvements/len(best_fitness_history))*100 if len(best_fitness_history) > 0 else 0
            f.write(f"• Generaciones con mejora: {significant_improvements}\n")
            f.write(f"• Porcentaje de generaciones productivas: {percent_productive:.1f}%\n\n")
            
            f.write("POBLACIÓN FINAL (FITNESS REALES):\n")
            f.write("-" * 30 + "\n")
            final_x_values = []
            for i, (individual, raw_fitness) in enumerate(zip(ga_results['final_population'], ga_results['final_fitness'])):
                x_val = binary_to_decimal(individual, 
                                         ga_results['x_min'], 
                                         ga_results['x_max'], 
                                         ga_results['n_bits'])
                final_x_values.append(x_val)
                binary_str = ''.join(map(str, individual))
                f.write(f"• Individuo {i+1}: {binary_str} -> x = {x_val:.6f}, f(x) = {raw_fitness:.6f}\n")
            
            if final_x_values:
                f.write(f"\n• Diversidad final (desviación estándar de x): {np.std(final_x_values):.6f}\n")
                f.write(f"• Rango de soluciones x: [{min(final_x_values):.6f}, {max(final_x_values):.6f}]\n\n")
            else:
                f.write("\n• Diversidad final (desviación estándar de x): N/A\n")
                f.write("• Rango de soluciones x: N/A\n\n")
            
            f.write("HISTORIAL DE MEJORES FITNESS (REALES):\n")
            f.write("-" * 30 + "\n")
            limit_display = 5
            if len(best_fitness_history) > 2 * limit_display:
                f.write(f"Primeras {limit_display} generaciones:\n")
                for i in range(limit_display):
                    f.write(f"  Gen {i+1}: {best_fitness_history[i]:.6f}\n")
                f.write("  ...\n")
                f.write(f"Últimas {limit_display} generaciones:\n")
                for i in range(len(best_fitness_history) - limit_display, len(best_fitness_history)):
                    f.write(f"  Gen {i+1}: {best_fitness_history[i]:.6f}\n")
            else:
                for i in range(len(best_fitness_history)):
                    f.write(f"  Gen {i+1}: {best_fitness_history[i]:.6f}\n")

            f.write("\nESTADÍSTICAS ADICIONALES:\n")
            f.write("-" * 30 + "\n")
            f.write(f"• Evaluaciones totales de la función: {ga_results['pop_size'] * ga_results['generations']}\n")
            f.write(f"• Tipo de selección (ejemplo AG): Emparejamiento aleatorio con poda\n")
            f.write(f"• Tipo de cruzamiento (ejemplo AG): 3 puntos aleatorios\n")
            f.write(f"• Tipo de mutación (ejemplo AG): Intercambio de genes\n\n")
            
            f.write("="*60 + "\nFIN DEL REPORTE\n" + "="*60 + "\n")
        return True

    def open_file(self, filename):
        import os
        import subprocess
        if not os.path.exists(filename):
            return False
        try:
            if os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'posix':
                import platform
                if platform.system() == 'Darwin':
                    subprocess.call(('open', filename))
                else:
                    subprocess.call(('xdg-open', filename))
            return True
        except Exception as e:
            print(f"Error opening file: {e}")
            return False

class AnimationGenerator:
    def __init__(self):
        pass

    def generate(self, filename, best_fitness_history, is_minimizing):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import numpy as np

        try:
            fig = plt.figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Generación', fontsize=12)
            ax.set_ylabel('Mejor Fitness (Valor real)', fontsize=12)
            ax.set_title('Evolución del Mejor Individuo', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)

            y_vals = best_fitness_history
            min_fitness = min(y_vals) if y_vals else 0
            max_fitness = max(y_vals) if y_vals else 1
            padding = (max_fitness - min_fitness) * 0.1 if (max_fitness - min_fitness) > 0 else 1
            ax.set_ylim(min_fitness - padding, max_fitness + padding)
            ax.set_xlim(-1, len(best_fitness_history) if best_fitness_history else 1)

            line, = ax.plot([], [], 'g-', linewidth=2, marker='o', markersize=6)
            gen_text = ax.text(0.02, 0.95, 'Generación: 0', transform=ax.transAxes, fontsize=10,
                               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            initial_fitness_text = f'Fitness: {best_fitness_history[0]:.4f}' if best_fitness_history else 'Fitness: N/A'
            fitness_text = ax.text(0.02, 0.87, initial_fitness_text, transform=ax.transAxes, fontsize=10,
                                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

            improvements_indices = []
            if best_fitness_history:
                for i in range(1, len(best_fitness_history)):
                    condition = best_fitness_history[i] < best_fitness_history[i-1] if is_minimizing else best_fitness_history[i] > best_fitness_history[i-1]
                    if condition:
                        improvements_indices.append(i)

            def init():
                line.set_data([], [])
                gen_text.set_text('Generación: 0')
                fitness_text.set_text(initial_fitness_text)
                return line, gen_text, fitness_text

            def animate_frame(i):
                if not best_fitness_history:
                    return line, gen_text, fitness_text
                x_data = list(range(i + 1))
                y_data = best_fitness_history[:i + 1]
                line.set_data(x_data, y_data)
                gen_text.set_text(f'Generación: {i + 1}')
                fitness_text.set_text(f'Fitness: {best_fitness_history[i]:.4f}')
                if i in improvements_indices:
                    ax.scatter([i], [best_fitness_history[i]], color='orange', s=100, zorder=5)
                return line, gen_text, fitness_text

            num_frames = len(best_fitness_history) if best_fitness_history else 0
            if num_frames == 0:
                plt.close(fig)
                return {"success": False, "message": "No hay datos para generar la animación."}

            anim = animation.FuncAnimation(fig, animate_frame, init_func=init, frames=num_frames, interval=200, blit=True)

            if filename.endswith('.mp4'):
                writer = animation.FFMpegWriter(fps=5)
                anim.save(filename, writer=writer)
            elif filename.endswith('.gif'):
                writer = animation.PillowWriter(fps=5)
                anim.save(filename, writer=writer)
            else:
                writer = animation.FFMpegWriter(fps=5)
                anim.save(f"{filename}.mp4", writer=writer)

            plt.close(fig)
            return {"success": True, "message": f"Animación guardada exitosamente en:\n{filename}"}

        except Exception as e:
            plt.close('all')
            msg = str(e)
            if "MovieWriter" in msg or "ffmpeg" in msg.lower():
                msg = ("Para guardar animaciones en formato MP4, necesita tener FFmpeg instalado.\n"
                       "Visite: https://www.ffmpeg.org/download.html\n\n"
                       "Alternativamente, intente guardar como GIF (.gif)\n\n" + msg)
            return {"success": False, "message": f"No se pudo generar la animación: {msg}"}