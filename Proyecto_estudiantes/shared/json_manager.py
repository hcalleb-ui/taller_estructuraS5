import json
import os


def leer_json(ruta):
    """Lee un archivo JSON y devuelve una lista. Si no existe o está vacío, devuelve []."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        return []


def guardar_json(ruta, datos):
    """Guarda una lista de diccionarios en un archivo JSON."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)