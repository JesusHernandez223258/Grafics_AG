# En un nuevo archivo, por ejemplo, "workers.py" o dentro de tu lógica de AG
from PySide6.QtCore import QObject, Signal, QThread

class GAWorker(QObject): # QObject para poder tener señales y slots
    progressUpdated = Signal(int, int, str)
    calculationFinished = Signal(dict)
    calculationError = Signal(str)

    def __init__(self, ga_instance, params):
        super().__init__()
        self.ga_instance = ga_instance
        self.params = params
        self._is_running = True

    def run(self): # Este método se ejecutará en el hilo secundario
        try:
            # Adaptar la llamada a ga_instance.run para que pueda
            # llamar a self.progressUpdated.emit(...)
            # Por ahora, asumimos que ga_instance.run no tiene callbacks de progreso internos
            # y el progreso se maneja "después" de cada generación si es necesario
            # o simplemente se muestra un progreso general en la UI antes de iniciar el hilo.

            # Para un progreso más granular, el método run del AG necesitaría
            # una forma de reportar el progreso (ej. un callback que emita la señal)
            # Si tu AG ya usa una ventana de progreso Tkinter, eso se ejecutará
            # en este hilo secundario, lo cual NO es ideal para la UI principal de Qt.
            # Lo ideal es que el AG no maneje UI directamente.

            print(f"[GAWorker] Iniciando ejecución del AG con parámetros: {self.params}")
            # --- MODIFICACIÓN NECESARIA EN TU AG.RUN ---
            # Tu AG.run toma 'progress_root_window'. Si es None, no muestra UI tk.
            # Pero para emitir señales Qt, AG.run necesitaría un callback o esta clase Worker
            # tendría que reimplementar el bucle de generaciones para emitir señales.
            # Por simplicidad, asumamos que AG.run no crea UI por ahora
            # y el progreso se indica en la UI principal *antes* de lanzar el hilo.
            
            # Si tu ga_instance.run es bloqueante y no tiene forma de emitir progreso:
            # No podrás tener progreso por generación desde aquí sin modificar ga_instance.run
            # Lo que haremos es emitir "finished" o "error".
            # El QProgressDialog en MainWindow será indeterminado o solo mostrará "Procesando..."

            results = self.ga_instance.run(
                x_min=self.params['interval_a'],
                x_max=self.params['interval_b'],
                delta_x=self.params['delta_x'],
                pop_size=self.params['pop_size'],
                max_generations=self.params['num_generations'],
                prob_crossover=self.params['prob_crossover'],
                prob_mutation_i=self.params['prob_mutation_i'],
                prob_mutation_g=self.params['prob_mutation_g'],
                is_minimizing=self.params['is_minimizing'],
                progress_root_window=None # IMPORTANTE: No pasar ventana Tkinter aquí
            )
            if self._is_running and results:
                self.calculationFinished.emit(results)
            elif not results:
                 self.calculationError.emit("El AG no devolvió resultados.")

        except Exception as e:
            if self._is_running:
                import traceback
                error_msg = f"Error en GAWorker: {str(e)}\n{traceback.format_exc()}"
                self.calculationError.emit(error_msg)
        finally:
            print("[GAWorker] Ejecución finalizada.")

    def stop(self):
        self._is_running = False