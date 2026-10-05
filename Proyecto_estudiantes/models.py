class Estudiante:
    def __init__(self, id, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self.notas = notas if notas is not None else {}              # dict: materia -> [notas]
        self.materias = materias if materias is not None else set()  # set: sin repetidos

    def agregar_nota(self, materia, nota):
        self.notas.setdefault(materia, []).append(nota)  # crea la lista si la materia es nueva
        self.materias.add(materia)                       # inscribe la materia

    def promedio(self):
        todas = [n for lista in self.notas.values() for n in lista]
        return sum(todas) / len(todas) if todas else 0

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": sorted(self.materias),  # JSON no tiene sets, se guarda como lista
        }

    @classmethod
    def desde_diccionario(cls, d):
        return cls(
            d["id"], d["nombre"], d["apellido"], d["email"], d["carnet"],
            d.get("notas", {}),
            set(d.get("materias", [])),  # lista -> set otra vez
        )

    def __str__(self):
        materias = ", ".join(sorted(self.materias)) or "ninguna"
        return (f"[{self.id}] {self.nombre} {self.apellido} | {self.email} | "
                f"Carnet: {self.carnet} | Materias: {materias}")