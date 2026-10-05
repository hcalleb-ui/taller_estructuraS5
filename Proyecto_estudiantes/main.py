from views import ControladorEstudiantes
from shared.herramientas import limpiar_pantalla, pausar, pedir_texto, pedir_entero

ctrl = ControladorEstudiantes()


def mostrar_menu():
    print("------------ SISTEMA DE ESTUDIANTES ------------")
    print("1. Crear estudiante")
    print("2. Listar estudiantes")
    print("3. Buscar estudiante")
    print("4. Editar estudiante")
    print("5. Eliminar estudiante")
    print("6. Agregar nota")
    print("7. Ver promedio")
    print("8. Materias en común")
    print("9. Materias ofertadas")
    print("0. Salir")
    print("------------------------------------------------")
    return pedir_texto("Opción: ")


def main():
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu()
        print()

        if opcion == "1":
            nombre = pedir_texto("Nombre: ")
            apellido = pedir_texto("Apellido: ")
            email = pedir_texto("Email: ")
            carnet = pedir_texto("Carnet: ")
            ok, mensaje = ctrl.crear_estudiante(nombre, apellido, email, carnet)
            print(mensaje)

        elif opcion == "2":
            lista = ctrl.obtener_todos()
            if not lista:
                print("No hay estudiantes registrados.")
            for e in lista:
                print(e)

        elif opcion == "3":
            texto = pedir_texto("Buscar (nombre, apellido o carnet): ")
            resultados = ctrl.buscar_estudiantes(texto)
            if not resultados:
                print("Sin resultados.")
            for e in resultados:
                print(e)

        elif opcion == "4":
            id = pedir_entero("ID del estudiante: ")
            if id is None:
                print("ID inválido.")
            else:
                print("Deja vacío lo que no quieras cambiar.")
                nombre = pedir_texto("Nuevo nombre: ")
                apellido = pedir_texto("Nuevo apellido: ")
                email = pedir_texto("Nuevo email: ")
                carnet = pedir_texto("Nuevo carnet: ")
                ok, mensaje = ctrl.actualizar_estudiante(id, nombre, apellido, email, carnet)
                print(mensaje)

        elif opcion == "5":
            id = pedir_entero("ID del estudiante: ")
            if id is None:
                print("ID inválido.")
            else:
                ok, mensaje = ctrl.eliminar_estudiante(id)
                print(mensaje)

        elif opcion == "6":
            id = pedir_entero("ID del estudiante: ")
            if id is None:
                print("ID inválido.")
            else:
                materia = pedir_texto("Materia: ")
                nota = pedir_texto("Nota (0-20): ")
                ok, mensaje = ctrl.agregar_nota(id, materia, nota)
                print(mensaje)

        elif opcion == "7":
            id = pedir_entero("ID del estudiante: ")
            if id is None:
                print("ID inválido.")
            else:
                ok, resultado = ctrl.promedio_estudiante(id)
                print(f"Promedio: {resultado:.2f}" if ok else resultado)

        elif opcion == "8":
            a = pedir_entero("ID del primer estudiante: ")
            b = pedir_entero("ID del segundo estudiante: ")
            if a is None or b is None:
                print("ID inválido.")
            else:
                ok, resultado = ctrl.estudiantes_en_comun(a, b)
                if not ok:
                    print(resultado)
                elif resultado:
                    print("Materias en común:", ", ".join(sorted(resultado)))
                else:
                    print("No comparten materias.")

        elif opcion == "9":
            materias = ctrl.materias_ofertadas()
            print("Materias ofertadas:", ", ".join(sorted(materias)) or "ninguna")

        elif opcion == "0":
            print("Hasta luego. Gracias por preferirnos ")
            break

        else:
            print("Opción no válida.")

        pausar()


if __name__ == "__main__":
    main()