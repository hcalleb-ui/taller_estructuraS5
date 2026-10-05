import os
from models import Estudiante
from shared.json_manager import leer_json, guardar_json

RUTA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "estudiantes.json")


class ControladorEstudiantes:
    def __init__(self):
        self.estudiantes = []
        self.emails = set()    # sets para detectar repetidos rápido
        self.carnets = set()
        self._cargar()

    # ---------- Persistencia ----------
    def _cargar(self):
        datos = leer_json(RUTA_JSON)
        self.estudiantes = [Estudiante.desde_diccionario(d) for d in datos]
        self.emails = {e.email for e in self.estudiantes}
        self.carnets = {e.carnet for e in self.estudiantes}

    def _guardar(self):
        guardar_json(RUTA_JSON, [e.a_diccionario() for e in self.estudiantes])

    # ---------- Auxiliares ----------
    def _siguiente_id(self):
        return max((e.id for e in self.estudiantes), default=0) + 1

    def _buscar_por_id(self, id):
        for e in self.estudiantes:
            if e.id == id:
                return e
        return None

    # ---------- CRUD ----------
    def crear_estudiante(self, nombre, apellido, email, carnet):
        if not nombre or not apellido:
            return False, "Nombre y apellido son obligatorios."
        if email in self.emails:
            return False, "Ese email ya está registrado."
        if carnet in self.carnets:
            return False, "Ese carnet ya está registrado."
        est = Estudiante(self._siguiente_id(), nombre, apellido, email, carnet)
        self.estudiantes.append(est)
        self.emails.add(email)
        self.carnets.add(carnet)
        self._guardar()
        return True, f"Estudiante creado con id {est.id}."

    def obtener_todos(self):
        return self.estudiantes

    def buscar_estudiantes(self, texto):
        texto = texto.lower()
        return [e for e in self.estudiantes
                if texto in e.nombre.lower()
                or texto in e.apellido.lower()
                or texto in e.carnet.lower()]

    def actualizar_estudiante(self, id, nombre=None, apellido=None, email=None, carnet=None):
        est = self._buscar_por_id(id)
        if est is None:
            return False, "No existe un estudiante con ese id."
        if email and email != est.email and email in self.emails:
            return False, "Ese email ya está registrado."
        if carnet and carnet != est.carnet and carnet in self.carnets:
            return False, "Ese carnet ya está registrado."
        if nombre:
            est.nombre = nombre
        if apellido:
            est.apellido = apellido
        if email:
            self.emails.discard(est.email)
            est.email = email
            self.emails.add(email)
        if carnet:
            self.carnets.discard(est.carnet)
            est.carnet = carnet
            self.carnets.add(carnet)
        self._guardar()
        return True, "Estudiante actualizado."

    def eliminar_estudiante(self, id):
        est = self._buscar_por_id(id)
        if est is None:
            return False, "No existe un estudiante con ese id."
        self.estudiantes.remove(est)
        self.emails.discard(est.email)
        self.carnets.discard(est.carnet)
        self._guardar()
        return True, "Estudiante eliminado."

    # ---------- Funciones nuevas de la tarea ----------
    def agregar_nota(self, id, materia, nota):
        est = self._buscar_por_id(id)
        if est is None:
            return False, "No existe un estudiante con ese id."
        materia = materia.strip().title()
        if not materia:
            return False, "La materia no puede estar vacía."
        try:
            nota = float(nota)
        except (ValueError, TypeError):
            return False, "La nota debe ser un número."
        if not 0 <= nota <= 20:
            return False, "La nota debe estar entre 0 y 20."
        est.agregar_nota(materia, nota)
        self._guardar()
        return True, f"Nota {nota} agregada en {materia}."

    def promedio_estudiante(self, id):
        est = self._buscar_por_id(id)
        if est is None:
            return False, "No existe un estudiante con ese id."
        return True, est.promedio()

    def materias_ofertadas(self):
        todas = set()
        for e in self.estudiantes:
            todas |= e.materias  # unión de conjuntos
        return todas

    def estudiantes_en_comun(self, id_a, id_b):
        a = self._buscar_por_id(id_a)
        b = self._buscar_por_id(id_b)
        if a is None or b is None:
            return False, "Uno de los dos ids no existe."
        return True, a.materias & b.materias  # intersección de conjuntos