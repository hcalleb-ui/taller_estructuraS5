import os


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona Enter para continuar...")


def pedir_texto(mensaje):
    return input(mensaje).strip()


def pedir_entero(mensaje):
    """Pide un número entero. Devuelve None si el usuario escribe algo que no es número."""
    try:
        return int(input(mensaje))
    except ValueError:
        return None