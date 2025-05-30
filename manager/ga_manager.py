# ===== ./manager/ga_manager.py =====

"""
Gestor de Algoritmos Genéticos (GA Manager)
-------------------------------------------
Este módulo centraliza la selección y carga de diferentes implementaciones
de algoritmos genéticos para el visualizador.

Para integrar un nuevo algoritmo genético:
1.  Cree una nueva carpeta para su algoritmo (ej. `my_new_ga/`).
2.  Dentro de esa carpeta, cree un archivo Python (ej. `my_ga_implementation.py`).
3.  Implemente su clase de algoritmo genético en ese archivo.
    Consulte `manager/README_FOR_NEW_ALGORITHMS.md` para la interfaz requerida.
4.  Importe su clase de AG en este archivo (`ga_manager.py`).
5.  Registre su AG en el diccionario `AVAILABLE_ALGORITHMS` abajo,
    asociando un nombre único (string) con su clase.
"""

# Importaciones de las clases de los Algoritmos Genéticos disponibles
# Asegúrate de que estas rutas sean correctas según tu estructura de proyecto
from example_ga.genetic_algorithm import GeneticAlgorithm as ExampleGeneticAlgorithm
from algorithm.genetic_algorithm import GeneticAlgorithm as StandardGeneticAlgorithm # Asumiendo que creas este

# Diccionario para registrar los algoritmos disponibles
# La clave es un nombre legible/identificador, el valor es la clase del AG.
AVAILABLE_ALGORITHMS = {
    "example_ga": ExampleGeneticAlgorithm,
    "standard_ga": StandardGeneticAlgorithm,
    # "nombre_unico_otro_ag": OtroAGClase, # Descomentar y añadir nuevos AGs aquí
}

def get_ga_instance(algorithm_name: str):
    """
    Obtiene una instancia del algoritmo genético especificado.

    Args:
        algorithm_name (str): El nombre del algoritmo registrado en AVAILABLE_ALGORITHMS.

    Returns:
        Una instancia de la clase del algoritmo genético, o None si no se encuentra.

    Raises:
        ValueError: Si el nombre del algoritmo no está registrado.
    """
    ga_class = AVAILABLE_ALGORITHMS.get(algorithm_name)
    if ga_class:
        return ga_class()
    else:
        raise ValueError(f"Algoritmo '{algorithm_name}' no encontrado. "
                         f"Opciones disponibles: {list(AVAILABLE_ALGORITHMS.keys())}")

def get_available_ga_names() -> list:
    """
    Devuelve una lista con los nombres de los algoritmos genéticos disponibles.
    """
    return list(AVAILABLE_ALGORITHMS.keys())

if __name__ == '__main__':
    print("Algoritmos Genéticos Disponibles:")
    for name in get_available_ga_names():
        print(f"- {name}")

    print("\nProbando instanciar 'example_ga':")
    try:
        instance = get_ga_instance("example_ga")
        print(f"Instancia creada: {instance}")
    except ValueError as e:
        print(e)

    print("\nProbando instanciar 'standard_ga':")
    try:
        instance = get_ga_instance("standard_ga")
        print(f"Instancia creada: {instance}")
    except ValueError as e:
        print(e)

    print("\nProbando instanciar un AG no existente:")
    try:
        instance = get_ga_instance("non_existent_ga")
        print(f"Instancia creada: {instance}")
    except ValueError as e:
        print(e)