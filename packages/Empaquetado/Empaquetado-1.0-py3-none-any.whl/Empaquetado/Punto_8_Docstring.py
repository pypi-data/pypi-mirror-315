"""
Este proyecto se encarga de obtener la última hora de acceso a una carpeta específica.

La función obtiene el tiempo de último acceso a un directorio específico y lo muestra en formato de hora local.

Dependencias:
- os: para interactuar con el sistema de archivos.
- time: para convertir el tiempo en segundos a un formato legible.

Autor: Fiorella Salas
Fecha: 12/12/2024
Versión: 1.0
"""

import os, time

# Función para obtener la última hora de acceso a la carpeta
def obtener_ultima_hora_acceso():
    """
    Obtiene la última hora de acceso a una carpeta específica.

    Esta función utiliza el módulo 'os' para obtener la última hora de acceso de un directorio 
    dado y la convierte en un formato legible para el usuario.

    Parámetros:
    Ninguno

    Retorna:
    None o la última hora de acceso a la carpeta en formato legible (hora local).

    Ejemplo de uso:
    obtener_ultima_hora_acceso()

    Excepciones:
    Lanza una excepción si el directorio no existe o si ocurre algún otro error al intentar 
    obtener la hora de acceso.
    """
    try:
        directorio = f"C:/Examen_Fiorella_Salas"
        # Obtener la última hora de acceso al directorio
        tiempo_acceso = os.path.getatime(directorio)

        # Convertir el tiempo en segundos desde el momento a hora local
        ultima_hora = time.ctime(tiempo_acceso)

        print(f"La última hora de acceso a la carpeta {directorio} fue: {ultima_hora}")
        
    except Exception as e:
        print(f"No se pudo obtener la última hora de acceso para el directorio {directorio}. Error: {e}")

obtener_ultima_hora_acceso()