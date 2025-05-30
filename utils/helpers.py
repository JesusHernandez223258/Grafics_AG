#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones auxiliares para la aplicación
"""

import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

def show_progress_window(parent, title="Procesando...", message="Por favor espere...", progress_mode='indeterminate'):
    """Crea una ventana de progreso para operaciones largas
    
    Args:
        parent: Ventana padre
        title: Título de la ventana
        message: Mensaje a mostrar
        progress_mode: Modo de la barra de progreso ('determinate' o 'indeterminate')
        
    Returns:
        Tupla (ventana, barra_progreso, etiqueta) para manipular la ventana creada
    """
    progress_window = tk.Toplevel(parent)
    progress_window.title(title)
    progress_window.geometry("400x120")
    progress_window.configure(bg='#f0f0f0')
    progress_window.resizable(False, False)
    
    # Hacer que la ventana sea modal
    progress_window.transient(parent)
    progress_window.grab_set()
    
    # Componentes de la ventana
    tk.Label(progress_window, text=message, 
            font=("Arial", 12), bg='#f0f0f0').pack(pady=20)
    
    from tkinter import ttk
    progress_bar = ttk.Progressbar(progress_window, mode=progress_mode)
    progress_bar.pack(pady=10, padx=20, fill='x')
    
    if progress_mode == 'indeterminate':
        progress_bar.start(10)
    
    progress_label = tk.Label(progress_window, text="", 
                             font=("Arial", 10), bg='#f0f0f0')
    progress_label.pack()
    
    progress_window.update()
    
    return progress_window, progress_bar, progress_label

def open_file(filepath):
    """Abre un archivo con la aplicación predeterminada del sistema
    
    Args:
        filepath: Ruta al archivo a abrir
    
    Returns:
        bool: True si se pudo abrir el archivo, False en caso contrario
    """
    if not os.path.exists(filepath):
        return False
        
    try:
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', filepath])
        else:  # Linux y otros
            subprocess.run(['xdg-open', filepath])
        return True
    except Exception as e:
        messagebox.showwarning("Advertencia", 
                             f"No se pudo abrir el archivo automáticamente: {str(e)}")
        return False

def validate_numeric_input(value, min_value=None, max_value=None, allow_negative=True, allow_float=True):
    """Valida que un valor sea numérico y esté dentro de los límites especificados
    
    Args:
        value: Valor a validar
        min_value: Valor mínimo permitido (opcional)
        max_value: Valor máximo permitido (opcional)
        allow_negative: Si se permiten valores negativos
        allow_float: Si se permiten valores decimales
    
    Returns:
        tuple: (es_válido, valor_convertido)
    """
    try:
        # Convertir a número
        if allow_float:
            numeric_value = float(value)
        else:
            numeric_value = int(value)
            
        # Verificar si es negativo cuando no se permite
        if not allow_negative and numeric_value < 0:
            return False, None
            
        # Verificar límites
        if min_value is not None and numeric_value < min_value:
            return False, None
            
        if max_value is not None and numeric_value > max_value:
            return False, None
            
        return True, numeric_value
    except (ValueError, TypeError):
        return False, None