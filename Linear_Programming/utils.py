import enum

# Crear una lista de valores
valores = ['Unknown']

# Crear el enumerado de forma dinámica
MiEnum = enum.Enum('Tags', valores)

# Imprimir los valores del enumerado
for valor in MiEnum:
    print(valor)


class Teacher:
    def __init__(self, name: str):
        self.name = name


class UnknownTeacher(Teacher):
    def __init__(self):
        super().__init__('Unknown')


class Subject:
    def __init__(self, name: str, list_possibles_groups: list[str], dict_teachers: dict[str:Teacher]):
        self.name = name
        self.list_possibles_groups: list[str] = list_possibles_groups
        self.dict_teachers: dict[str:Teacher] = dict_teachers
        self.groups_now: set[str] = set()
        self.unknown: Teacher = UnknownTeacher()
        self.teacher: Teacher = self.unknown
        self.teacher_name = self.teacher.name

    def add_group(self, subject_name: str, group_name: str, teacher_name: str):
        if not self.name == subject_name:
            raise Exception(f"La asignatura {self.name} no es {subject_name}")
        if not (isinstance(self.teacher, UnknownTeacher) or self.teacher_name == teacher_name):
            raise Exception(
                f"El profesor {teacher_name} no es el que esta impartiendo ahora la asignatura {self.teacher_name} ")
        # Si el profe es unknown cambiar el profe por el actual
        if isinstance(self.teacher, UnknownTeacher):
            if not teacher_name in self.dict_teachers:
                raise Exception(f"El profesor {teacher_name} no esta declarado para dar la asignatura {self.name}")
            self.teacher = self.dict_teachers[teacher_name]

        if not group_name in self.list_possibles_groups:
            raise Exception(f"El grupo {group_name} no está entre los posibles grupos {self.list_possibles_groups}")
        self.groups_now.add(group_name)


class UnknownSubject(Subject):
    def __init__(self):
        super().__init__('Unknown', [], [])


class Classroom:
    def __init__(self, name: str, dict_subjects: dict[str:Subject]):
        """
        Initializes the object with the provided name and dictionary of subjects.

        Parameters:
            name (str): The name of the object.
            dict_subjects (dict[str:Subject]): A dictionary containing subjects.

        Returns:
            None
        """
        self.name = name
        self.unknown = UnknownSubject()
        self.possibles_subjects: dict[str:Subject] = dict_subjects
        self.subject: Subject = self.unknown
        self.subject_name = self.subject.name

    def add_subject_in_group_and_career(self, subject_name: str, group_name: str, teacher_name: str):
        # Comprobar que la asignatura sea valida para poner
        if not (isinstance(self.subject, UnknownSubject) or self.subject_name == subject_name):
            raise Exception(
                f"En el aula {self.name} se da la asignatura {self.subject_name} y se quiere dar {subject_name} ")
        # Comprobar si es unknown entonces verificar que en dicha aula se pueda dar esa asignatura
        if isinstance(self.subject, UnknownSubject):
            if not subject_name in self.possibles_subjects:
                raise Exception(f"La asignatura {subject_name} no es posible darla en el aula {self.name}")
            # Sea asigna la materia a dar
            self.subject: Subject = self.possibles_subjects[subject_name]

        # Añadir el grupo a la materia
        self.subject.add_group(subject_name, group_name, teacher_name)


class Shifts:
    def __init__(self, name: str, day: str, classrooms_name: list[str], dict_subjects: dict[str:Subject]):
        self.name = name
        self.day = day
        self.classrooms_name = classrooms_name
        self.classrooms: dict[str:Classroom] = {}
        # Instanciar las aulas posibles para ese turno
        for item in self.classrooms_name:
            self.classrooms[item] = Classroom(item, dict_subjects)
        self.teacher_by_subject: dict[str, str] = {}
        """Diccionario que a cada nombre de profesor le asigna una materia a dar 
        esto es para comprobar que un profe en un turno no de más de 1 clase a la vez"""

    def add_subject_with_classroom(self, shift_name: str, classroom_name: str, subject_name: str,
                                   group_name: str, teacher_name: str):
        # Si no es el mismo turno lanza excepción
        if not self.name == str(shift_name):
            raise Exception(f'Este es el turno {self.name} y se quiere añadir en el turno {shift_name}')
        # Si esa aula no se asignó a ese turno lanzar excepción
        if not classroom_name in self.classrooms:
            raise Exception(f'El aula {classroom_name} no está en este turno')

        # Comprobar que el profesor o no está asignado a ninguna materia o da la misma materia a asignar
        if teacher_name in self.teacher_by_subject and self.teacher_by_subject[teacher_name] != subject_name:
            raise Exception(
                f"El profesor {teacher_name} imparte la clase: {self.teacher_by_subject[teacher_name]} no la clase: {subject_name} ")
        # Si no esta en el diccionario añadirlo
        if not teacher_name in self.teacher_by_subject:
            self.teacher_by_subject[teacher_name] = subject_name

        # Añadir en las aulas
        self.classrooms[classroom_name].add_subject_in_group_and_career(subject_name, group_name, teacher_name)


class Calendar:
    def start(self):
        for i in range(1, self.days_count + 1):
            for j in range(1, self.shifts_counts + 1):
                self.shifts[i, j] = Shifts(str(j), str(i), self.classrooms_name)
                # dia , turno

    def __init__(self, subjects_name: list[str], teachers_name: list[str],
                 teacher_by_subject: dict[str, str], days_count=5, shifts_count=3,
                 classroom_names: list[str] = ["1", "2", "postgrado"]):

        self.days_count=days_count
        self.shifts_counts=shifts_count
        self.subjects_name: list[str] = subjects_name
        self.teachers_name:list[str]=teachers_name
        self.teacher_by_subject:dict[str,str]=teacher_by_subject
        self.classrooms_name = classroom_names

        self.unknown = 'Unknown'
        self.dict_subjects:dict[str,Subject]={}
        self.shifts: dict[tuple[int, int]:Shifts] = {}



    def add(self, grupo: str, aula: str, profesor: str, dia: str, turno: str, asignatura: str):
        dia = int(dia)
        turno = int(turno)
        key = (dia, turno)
        if not key in self.shifts:
            raise Exception("El dia o turno no es válido")

        shift = self.shifts[key]
        shift.add_subject_with_classroom(str(turno), aula, asignatura, grupo)
