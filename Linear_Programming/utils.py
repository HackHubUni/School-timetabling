import copy
# Usar deepcopy para clonar
class Teacher:
  def __init__(self, name: str):
    self.name = name


class UnknownTeacher(Teacher):
  def __init__(self):
    super().__init__('Unknown')


class Subject:
  def __init__(self, name: str, list_possibles_groups: list[str], dict_possibles_teachers: dict[str:Teacher]):
    """
    Initialize the class with the provided name, list of possible groups, and dictionary of possible teachers.
    Parameters:
        name (str): The name of the class.
        list_possibles_groups (list[str]): A list of possible groups for the class.
        dict_possibles_teachers (dict[str:Teacher]): A dictionary of possible teachers for the class.

    Returns:
        None
    """
    self.name = name
    self.list_possibles_groups: list[str] = copy.deepcopy(list_possibles_groups)
    self.dict_teachers: dict[str:Teacher] = copy.deepcopy(dict_possibles_teachers)
    self.groups_now: set[str] = set()
    self.unknown: Teacher = UnknownTeacher()
    self.teacher: Teacher = self.unknown
    self._teacher_name = None

  @property
  def teacher_name(self):
    return self.teacher.name

  def add_group(self, subject_name: str, group_name: str, teacher_name: str):
    if not self.name == subject_name:
      raise Exception(f"La asignatura {self.name} no es {subject_name}")
    if not (isinstance(self.teacher, UnknownTeacher) or self.teacher_name == teacher_name):
      raise Exception(
        f"El profesor {teacher_name} no es el que esta impartiendo ahora la asignatura {self.name} la imparte {self.teacher_name} ")
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
    self.possibles_subjects: dict[str:Subject] = copy.deepcopy(dict_subjects)
    self.subject: Subject = self.unknown
    self._subject_name = None

  @property
  def subject_name(self):
    return self.subject.name

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
    """
    Initialize the Schedule object with the given name, day, list of classroom names, and dictionary of subjects.
    """
    self.name: str = name
    self.day: str = day
    self.classrooms_name: list[str] = copy.deepcopy(classrooms_name)
    self.classrooms: dict[str:Classroom] = {}
    # Instance las aulas posibles para ese turno
    for item in self.classrooms_name:
      self.classrooms[item] = Classroom(item, copy.deepcopy(dict_subjects))
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
    if teacher_name not in self.teacher_by_subject:
      self.teacher_by_subject[teacher_name] = subject_name

    # Añadir en las aulas
    self.classrooms[classroom_name].add_subject_in_group_and_career(subject_name, group_name, teacher_name)


class Group:
  def __init__(self, name, subjects_by_time: dict[str, int]):
    self.name = name
    self.subjects_by_time: dict[str, int] = copy.deepcopy(subjects_by_time)
    self.count_now_subjects_by_time: dict[str, int] = {}
    # Inicializa lo que tengo de tiempo real hasta ahora en 0
    for subject_name in self.subjects_by_time.keys():
      self.count_now_subjects_by_time[subject_name] = 0

  def add_subject_shift(self, subject_name: str):
    if subject_name not in self.count_now_subjects_by_time:
      raise Exception(f"La asignatura {subject_name} no está definida para el aula {self.name}")
    self.count_now_subjects_by_time[subject_name] += 1

  def check_all_ok(self):
    for subject_name in self.subjects_by_time.keys():
      promise_time = self.subjects_by_time[subject_name]
      real_time = self.count_now_subjects_by_time[subject_name]
      if promise_time != real_time:
        raise Exception(
          f"En el grupo {self.name} la asignatura {subject_name} debería tener {promise_time} hora clase a la semana y tiene {real_time}")


class Calendar:

  def __add_to_dict_possibles_groups_by_subject(self, group_name: str, list_subjects: list[str]):
    """
    Añade al diccionario que tiene como llave el nombre de la asignatura los posibles grupos que pueden recibir esta
    :param group_name:
    :param list_subjects:
    :return:
    """
    for subject_name in list_subjects:
      if subject_name not in self.subjects_name:
        raise Exception(f"La asignatura {subject_name} no está en {self.subjects_name}")
      # Comprueba que no se hala guardado ya la asignatura
      if subject_name not in self.subject_to_set_possible_groups:
        my_set = set()
        my_set.add(group_name)
        self.subject_to_set_possible_groups[subject_name] = my_set
      else:
        self.subject_to_set_possible_groups[subject_name].add(group_name)

  def __start_teachers(self):
    for teachers_name in self.teachers_name:
      self.dict_teachers[teachers_name] = Teacher(teachers_name)

  def __start_groups(self):
    for group_name in self.groups_names:
      if group_name not in self.group_by_assign_by_week_time:
        raise Exception(f"El grupo {group_name} no tiene clases asignadas ")
      # El diccionario que tiene como llave el nombre de la asignatura y como valor el tiempo que debe impartirse
      # esta en una semana
      dictionary: dict[str:int] = self.group_by_assign_by_week_time[group_name]
      group = Group(group_name, copy.deepcopy(dictionary))
      self.dict_groups[group_name] = group
      # Ahora añadir en la asignatura que este es un grupo posible
      list_subjects_name = list(dictionary.keys())
      self.__add_to_dict_possibles_groups_by_subject(group_name, list_subjects_name)

  def __get_possibles_teacher_by_subject(self, subject_name: str) -> dict[str, Teacher]:
    """
    Dado un nombre de materia devuelve un diccionario que tiene el nombre del profesor y el profesor

    :param subject_name:
    :return dict[str,Teacher] :
    """
    res: dict[str, Teacher] = {}
    if subject_name not in self.possibles_teacher_by_subject:
      raise Exception(f"La asignatura: {subject_name} no tiene asignado profesores")
    list_possibles_teacher = self.possibles_teacher_by_subject[subject_name]
    for teacher_name in list_possibles_teacher:
      if teacher_name not in self.dict_teachers:
        raise Exception(f"El profesor {teacher_name} no existe")
      teacher = self.dict_teachers[teacher_name]
      res[teacher_name] = teacher
    if len(res) < 1:
      raise Exception(f"Se debe asignar al menos un profesor a la asignatura {subject_name}")
    return res

  def __start_subjects(self):
    for subject_name in self.subjects_name:
      # Seleccionar los profesores para la materia
      dict_teachers = self.__get_possibles_teacher_by_subject(subject_name)
      temp = Subject(subject_name, list(copy.deepcopy(self.subject_to_set_possible_groups[subject_name])), copy.deepcopy(dict_teachers))
      self.dict_subjects[subject_name] = temp

  def __start_shifts(self):
    for i in range(1, self.days_count + 1):
      for j in range(1, self.shifts_counts + 1):
        self.shifts[i, j] = Shifts(str(j), str(i), self.classrooms_name, copy.deepcopy(self.dict_subjects))
        # dia , turno

  def __start(self):
    self.__start_groups()
    self.__start_teachers()
    self.__start_subjects()
    self.__start_shifts()

  def __init__(self, subjects_name: list[str], teachers_name: list[str],
               possibles_teacher_by_subject: dict[str, list[str]],
               group_by_assign_by_week_time: dict[str, dict[str, int]],
               days_count=5, shifts_count=3,
               classroom_names: list[str] = ["1", "2", "postgrado"], groups_names: list[str] = ["C111", "C112"]):

    """
    Initialize the Scheduler object with the provided parameters.

    Parameters:
    - subjects_name: list of str, names of the subjects
    - teachers_name: list of str, names of the teachers
    - possibles_teacher_by_subject: dict[str, str], mapea una materia y da una lista de posibles profesores
    - group_by_assign_by_week_time: dict[str, dict[str, int]], tiene los grupos como key y en las llaves las asignaturas con su nombre y time
    - days_count: int, number of days in a week (default is 5)
    - shifts_count: int, number of shifts in a day (default is 3)
    - classroom_names: list of str, names of the classrooms (default is ["1", "2", "postgrado"])
    - groups_names: list of str, names of the groups (default is ["C111", "C112"])

    Returns:
    - None
    """
    self.days_count = days_count
    self.shifts_counts = shifts_count
    self.subjects_name: list[str] = subjects_name
    self.teachers_name: list[str] = teachers_name
    self.possibles_teacher_by_subject: dict[str, list[str]] = possibles_teacher_by_subject
    self.classrooms_name = classroom_names
    self.groups_names = groups_names
    self.group_by_assign_by_week_time: dict[str:list[tuple[str, int]]] = group_by_assign_by_week_time

    self.unknown = 'Unknown'
    self.dict_subjects: dict[str, Subject] = {}
    self.shifts: dict[tuple[int, int], Shifts] = {}
    self.dict_groups: dict[str, Group] = {}
    self.subject_to_set_possible_groups: dict[str, set[str]] = {}
    self.dict_teachers: dict[str, Teacher] = {}

    # Llamar el start para inicialiazar los dict
    self.__start()

  def __add_subject_to_group(self, subject_name: str, group_name: str):
    if group_name not in self.dict_groups:
      raise Exception(f"El grupo {group_name} no esta definido")
    if subject_name not in self.dict_subjects:
      raise Exception(f"La asignatura {subject_name} no está definida")

    # Añadir la asignatura al grupo
    group = self.dict_groups[group_name]
    # Se dice que se dio un turno de esta asignatura
    group.add_subject_shift(subject_name)

  def add(self, group_name: str, classroom_name: str, teacher_name: str, day_name: str, shift_name: str,
          subject_name: str):

    day_name = int(day_name)
    shift_name = int(shift_name)
    key = (day_name, shift_name)
    if not key in self.shifts:
      raise Exception("El dia o turno no es válido")

    shift = self.shifts[key]

    shift.add_subject_with_classroom(str(shift_name), classroom_name, subject_name, group_name, teacher_name)

    # Añadir al grupo que se dio un turno de la asignatura
    self.__add_subject_to_group(subject_name, group_name)

  def finish(self):
    """
    Para hacer las comprobaciones finales
    :return:
    """
    groups_names = self.dict_groups.keys()
    for group_name in groups_names:
      group = self.dict_groups[group_name]
      # Comprueba que cada grupo recibió la cant de clases acordadas
      group.check_all_ok()



