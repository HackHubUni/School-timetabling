from ortools.constraint_solver.pywrapcp import IntVar
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel
from API.exceptions import LaunchingException, AddNewConstraintException
from src.utils import Calendar
from src.printer import to_data_frame


class TimeTablingSolverBase:


  def _check_exist_in_list(self, list_to_check: list[str | int], correct_list: list[str | int], type_name: str):
    """
      Este metodo chequea que para las restricciones que se añaden los profesores son de los que se añadieron en un principio
    :param list_to_check: La lista que entra para las nuevas restricciones
    :param correct_list:  La lista guardada en esta instancia de la clase
    :param type_name: Si es un profesor, asignatura,aula
    :return:
    """

    for item in list_to_check:
      if item not in correct_list:
        raise AddNewConstraintException(f'The {type_name}: {item} don t exists')

  def check_group_subject_time(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int]):
    dic_len = len(dict_subjects_by_time)
    list_len = len(subjects_name_list)
    if list_len != dic_len:
      raise LaunchingException(
        f'The len of the subjects_name_list:{list_len} and the len of the dict_subjects_by_time keys:{dic_len} ')
    for item in subjects_name_list:
      if item not in dict_subjects_by_time:
        raise LaunchingException(f'The subject {item} has not time in assign')




  def check_subject_group(self, dict_subjects_by_time: dict[str, int],
                          dict_group_subject_time: dict[str, dict[str, int]], groups_names: list[str]):
    """
    Chequea que en cada grupo se tengan asignaturas correctas y que estas tengan al menos el mínimo de horas estipulado
    :param dict_subjects_by_time:
    :param dict_group_subject_time:
    :param groups_names:
    :return:
    """
    #Comprobar que los nombres de los grupos coinciden osea que lo que este en el diccionario sea correcto
    self._check_exist_in_list(dict_group_subject_time.keys(),groups_names,"Group")



    #Comprueba por los grupos
    for group in groups_names:
      #Si el grupo no tiene materias
      if group not in dict_group_subject_time:
        raise LaunchingException(f'The group:{group} has not subjects assign')
      # Asignaturas por equipos
      dict_group_subject= dict_group_subject_time[group]
      # Ver por casa asignatura asignadas a los equipos
      for subject in dict_group_subject.keys():
        # Chequear que el tiempo que se le asigne a la asignatura en ese grupo sea mayor o igual al asignado global
        count_group_subject_time: int = dict_group_subject[subject]
        #Chequear que la asignatura asignada a este grupo exista dado que dict_subjects_by_time se verifico contra las
        # asignaturas anteriormente
        if subject not in dict_subjects_by_time:
          raise LaunchingException(f'In the group:{group} the subject: {subject} don t exists')
        min_time_subject: int = dict_subjects_by_time[subject]
        # Si el tiempo asignado a la asignatura es menor que el minimo de esta se lanza error
        if count_group_subject_time < min_time_subject:
          raise LaunchingException(
            f'In the group:{group} the subject {count_group_subject_time} hours and has a minimum of {min_time_subject} ')

  def check_subjects_names(self, list_name: list[str], set_total_names: set[str], teacher_name: str):
    for name in list_name:
      if name not in set_total_names:
        raise LaunchingException(f'The teacher:{teacher_name} has the subject:{name} and this don´t exists ')

  def check_teachers(self, teachers_names: list[str], dict_teachers_to_subjects: dict[str, list[str]],
                     subjects_name_list: list[str]):
    """
    Chequea que los todos profesores tienen asignaturas asignadas y que estas son validas
    :param teachers_names:
    :param dict_teachers_to_subjects:
    :return:
    """
    subjects_set: set[str] = set(subjects_name_list)
    len_teachers_list = len(teachers_names)
    len_subjects_set = len(subjects_set)
    len_dic = len(dict_teachers_to_subjects.keys())
    if len_teachers_list != len_dic:
      raise LaunchingException(
        f"The len of teachers are {len_teachers_list} and the len of teachers with subjects {len_dic}")
    for teacher in teachers_names:
      if teacher not in dict_teachers_to_subjects:
        raise LaunchingException(f'The teacher:{teacher} has not subjects')
      lis_teacher_subjects: list[str] = dict_teachers_to_subjects[teacher]

      # chequear que existan menos o igual cant asignaturas asignadas al profesor que las que realmente existen
      len_list_teacher_subjects = len(lis_teacher_subjects)
      if len_list_teacher_subjects > len_subjects_set:
        raise LaunchingException(
          f'The teacher:{teacher} can´t have more subjects assign:{len_list_teacher_subjects} that the really subjects:{len_subjects_set}')
      # Chequear que las asignaturas que tenga el profe sean validas
      self.check_subjects_names(lis_teacher_subjects, subjects_set, teacher)

  def check(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
            groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]],
            dict_teachers_to_subjects: dict[str, list[str]]):
    self.check_group_subject_time(subjects_name_list, dict_subjects_by_time)
    self.check_subject_group(dict_subjects_by_time, dict_group_subject_time, groups_names)
    self.check_teachers(teachers_names, dict_teachers_to_subjects, subjects_name_list)

  def __init__(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
               classrooms_names: list[str],
               groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
               days: list[int], dict_teachers_to_subjects: dict[str, list[str]]):

    # Chequear que los datos no tengan errores entre ellos
    self.check(subjects_name_list, dict_subjects_by_time, teachers_names, groups_names, dict_group_subject_time,
               dict_teachers_to_subjects)

    self.subjects_name_list: list[str] = subjects_name_list
    self.dict_subjects_by_time: dict[str:int] = dict_subjects_by_time
    self.teachers_names: list[str] = teachers_names
    self.classrooms_names: list[str] = classrooms_names
    self.groups_names: list[str] = groups_names
    self.dict_group_subject_time: dict[str, dict[str:int]] = dict_group_subject_time
    self.shifts: list[int] = shifts
    self.days: list[int] = days
    self.dict_teachers_to_subjects: dict[str, list[str]] = dict_teachers_to_subjects

    self._vars: dict = {}

  @property
  def vars(self):
    return self._vars

  @vars.setter
  def vars(self, value):
    self._vars = value


class ClassroomRestriction(TimeTablingSolverBase):
  def __init__(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
               classrooms_names: list[str],
               groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
               days: list[int], dict_teachers_to_subjects: dict[str, list[str]], model: CpModel):
    super().__init__(subjects_name_list, dict_subjects_by_time, teachers_names,
                     classrooms_names,
                     groups_names, dict_group_subject_time, shifts,
                     days, dict_teachers_to_subjects)

    self.model = model

    self.start()

  def start(self):
    self.create_vars()
    self.vars_natural_restriction()

  def create_vars(self):
    """
    Crea la variable necesaria para indicar que
    se debe de asignar en un turno a un aula una
     sola asignatura
    """
    # Solo se puede asignar a un aula una materia un dia x
    # Crear variables para esto

    for day in self.days:
      for shift in self.shifts:
        for subject in self.subjects_name_list:
          for classroom in self.classrooms_names:
            self.vars[day, shift, subject, classroom] = self.model.NewBoolVar(
              f'Variable auxiliar: aula:{classroom},asignatura:{subject},turno:{shift},dia:{day}   '
            )

  def vars_natural_restriction(self):
    # Que en un turno de un dia x en un aula solo se puede dar una materia
    for day in self.days:
      for shift in self.shifts:
        for classroom in self.classrooms_names:
          s = sum(self.vars[day, shift, subject, classroom]
                  for subject in self.subjects_name_list
                  )
          self.model.add(s <= 1)


class TeacherRestriction(TimeTablingSolverBase):
  def __init__(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
               classrooms_names: list[str],
               groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
               days: list[int], dict_teachers_to_subjects: dict[str, list[str]], model: CpModel):
    super().__init__(subjects_name_list, dict_subjects_by_time, teachers_names,
                     classrooms_names,
                     groups_names, dict_group_subject_time, shifts,
                     days, dict_teachers_to_subjects)

    self.model = model

    self.start()

  #  self._vars: dict[tuple[int, int, str, str], IntVar] = {}

  # @property
  # def vars(self):
  #  return self._vars

  # @vars.setter
  # def vars(self, value):
  #  self._vars = value

  def start(self):
    # Crear las variables para el tipo de restriction del profe en una sola aula
    self.create_vars()
    # Declarar la restriccion sobre las variables anteriores que un profesor en un
    # turno puede estar a lo sumo
    # en un aula
    self.vars_natural_restriction()

  def create_vars(self):
    # Variable para decir que un profesor puede estar en una sola aula en un turno en específico
    for day in self.days:
      for shift in self.shifts:
        for teacher in self.teachers_names:
          for classroom in self.classrooms_names:
            self.vars[day, shift, teacher, classroom] = self.model.NewBoolVar(
              f'Variable auxiliar: profesor:{teacher},aula:{classroom},turno:{shift},dia:{day}   '
            )

  def vars_natural_restriction(self):
    """
    Aca toma de la variables inicializadas en esta clase y dice
    que un profesor en un dia,turno puede estar a lo sumo en un aula
    :return:
    """
    # Que un profesor solo puede estar en un aula a la vez
    for day in self.days:
      for shift in self.shifts:
        for teacher in self.teachers_names:
          s = sum(self.vars[day, shift, teacher, classroom]
                  for classroom in self.classrooms_names
                  )
          self.model.add(s <= 1)


class OptionalRestrictions(TimeTablingSolverBase):
  def __init__(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
               classrooms_names: list[str],
               groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
               days: list[int], dict_teachers_to_subjects: dict[str, list[str]], model: CpModel):
    super().__init__(subjects_name_list, dict_subjects_by_time, teachers_names,
                     classrooms_names,
                     groups_names, dict_group_subject_time, shifts,
                     days, dict_teachers_to_subjects)

    self.model = model


class TimeTablingSolver(TimeTablingSolverBase):

  def _list_para_dataframe(self, teacher, subject, classroom, group, shift, day) -> list[dict]:
    data = []
    # Agregar los datos a la lista como un diccionario
    data.append({
      'Teacher': teacher,
      'Subject': subject,
      'Classroom': classroom,
      'Group': group,
      'Shift': shift,
      'Day': day
    })
    return data

  def _get_dic_subjects_to_teachers(self, teachers: list[str], subjects: list[str],
                                    dict_teachers_to_subjects: dict[str, list[str]]) -> dict[str, list[str]]:
    answer: dict[str, list[str]] = {}
    # Inicializar el diccionario
    for subject_name in subjects:
      answer[subject_name] = []

    # Cada asignatura agregarle los profes
    for teacher_name in teachers:
      subjects_list: list[str] = dict_teachers_to_subjects[teacher_name]
      for subject_name in subjects_list:
        answer[subject_name].append(teacher_name)

    return answer

  def __init__(self, subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
               classrooms_names: list[str],
               groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
               days: list[int], dict_teachers_to_subjects: dict[str, list[str]]):

    super().__init__(subjects_name_list, dict_subjects_by_time, teachers_names,
                     classrooms_names,
                     groups_names, dict_group_subject_time, shifts,
                     days, dict_teachers_to_subjects)

    self.dict_subjects_to_teachers = self._get_dic_subjects_to_teachers(teachers_names, subjects_name_list,
                                                                        dict_teachers_to_subjects)

    # Crear el modelo
    self.model = cp_model.CpModel()

    # El obj calendar para que vaya testeando que las soluciones satisfacen las restricciones
    self.calendar = Calendar(self.subjects_name_list, self.teachers_names, self.dict_subjects_to_teachers,
                             self.dict_group_subject_time, len(self.days),
                             len(self.shifts),
                             self.classrooms_names, self.groups_names)

    # Llamar a las restricciones del profesor

    # Argumentos para instanciar las clases para las restricciones que llevan mas variables
    args = (
      self.subjects_name_list, self.dict_subjects_by_time, self.teachers_names, self.classrooms_names,
      self.groups_names,
      self.dict_group_subject_time, self.shifts, self.days, self.dict_teachers_to_subjects, self.model)
    # Instanciar las restricciones del profesor
    self._teacher_restrictions = TeacherRestriction(*args)
    # Instanciar las restricciones del aula
    self._classroom_restrictions = ClassroomRestriction(*args)
    # self.vars: dict[tuple[str, str, str, str, int, int], "IntVar"] = {}

    # Call Start
    self.start()

  @property
  def teacher_restrictions(self):
    return self._teacher_restrictions

  #  @property
  #  def vars(self):
  #    return self.vars
  #
  #  @vars.setter
  #  def vars(self, value):
  #    self.vars = value

  def start(self):
    self._create_problems_vars()

    # LLamar las restricciones hard

    self.start_hard_restrictions()

    # A las de teste

  def start_hard_restrictions(self):
    """
    Inicializa las restricciones hard

    :return:
    """
    # Restricciones hard como que para todos los grupos deben dar la cant de horas clase por asignatura
    self._global_hard_restrictions()
    # Restricciones hard para que cada profesor solo pueda estar en un aula en un turno x
    self._teacher_hard_restrictions()
    # Restricciones hard para que en un aula solo se pueda dar una asignatura simultaneamente
    self._classroom_hard_restrictions()

  def _create_problems_vars(self):
    """
    Instancia el problema original.
    :return:
    """

    self.vars: dict[tuple[str, str, str, str, int, int], "IntVar"] = {}
    for day in self.days:
      for shift in self.shifts:
        for group in self.groups_names:
          for subject in self.subjects_name_list:
            for classroom in self.classrooms_names:
              for teacher in self.teachers_names:
                self.vars[teacher, subject, classroom, group, shift, day] = self.model.NewBoolVar(
                  f'profesor:{teacher},asignatura:{subject},aula:{classroom},grupo:{group},turno:{shift},dia:{day}')

  def get_var(self, teacher_name: str, subject_name: str, classroom_name: str, group_name: str, shift_int: int,
              day_int: int):
    try:
      if not (isinstance(shift_int, int) and isinstance(day_int, int)):
        raise Exception(f"El turno:{type(shift_int)} o el dia:{type(day_int)} no se ha dado como entero")
      if not (teacher_name, subject_name, classroom_name, group_name, shift_int, day_int) in self.vars:
        raise Exception(
          f"La llave {(teacher_name, subject_name, classroom_name, group_name, shift_int, day_int)} , no se encuentra en las variables globales")
      return self.vars[teacher_name, subject_name, classroom_name, group_name, shift_int, day_int]
    except Exception as e:

      raise Exception(f'Error en get_vars: {str(e)}')

  def _global_hard_restrictions(self):
    """
    Restricciones hard globales
    """
    # Que siempre se den todos los turnos de las asignaturas en cada grupo
    for subject in self.subjects_name_list:
      for group in self.groups_names:
        s = sum(
          self.vars[profesor, subject, aula, group, turno, dia] for profesor in self.teachers_names for aula in
          self.classrooms_names
          for turno in self.shifts for dia in self.days if subject in self.dict_teachers_to_subjects[profesor])
        self.model.add(s == self.dict_subjects_by_time[subject])

      # Que un grupo pueda estar en un turno en una sola aula dando una sola asignatura
      for day in self.days:
        for shift in self.shifts:
          for group in self.groups_names:
            s = sum(self.vars[profesor, asignatura, aula, group, shift, day] for profesor in self.teachers_names
                    for asignatura in self.subjects_name_list
                    for aula in self.classrooms_names
                    if asignatura in self.dict_teachers_to_subjects[profesor])
            self.model.add(s <= 1)

  def _teacher_hard_restrictions(self):
    """
    Aca se inicializa la restricción que un profesor en un turno puede estar en una sola aula al mismo tiempo
    :return:
    """

    # Aca son el and digo que para todos los grupos deben darse todos los turnos pero deben de satisfacer que un profe debe estar en un solo aula
    for subject in self.subjects_name_list:
      for group in self.groups_names:
        for teacher in self.teachers_names:
          for classroom in self.classrooms_names:
            for shift in self.shifts:
              for day in self.days:
                if subject in self.dict_teachers_to_subjects[teacher]:
                  self.model.AddBoolAnd([self.vars[teacher, subject, classroom, group, shift, day],
                                         # Variables para restricciones del profesor
                                         self.teacher_restrictions.vars[day, shift, teacher, classroom]]).OnlyEnforceIf(
                    # el onlyEnforceIf asegura que ese and sea verdadero tal que se cumpla en el anterior
                    self.vars[teacher, subject, classroom, group, shift, day])

  def _classroom_hard_restrictions(self):
    # Aca se le hace el and para que se asegura que solo se puede tener una materia en un turno por aula

    for subject in self.subjects_name_list:
      for group in self.groups_names:
        for teacher in self.teachers_names:
          for classroom in self.classrooms_names:
            for shift in self.shifts:
              for day in self.days:
                if subject in self.dict_teachers_to_subjects[teacher]:
                  self.model.AddBoolAnd([self.vars[teacher, subject, classroom, group, shift, day],
                                         self._classroom_restrictions.vars[
                                           day, shift, subject, classroom]]).OnlyEnforceIf(
                    # el onlyEnforceIf asegura que ese and sea verdadero tal que se cumpla el el anterior

                    self.vars[teacher, subject, classroom, group, shift, day])

  def solve(self, show_all_exceptions: bool = True):
    """
    Resuelve el problema del horario
    :return:
    """

    # Crear el solucionador y resolver
    solver = cp_model.CpSolver()
    status = solver.Solve(self.model)

    if status == cp_model.INFEASIBLE:
      # print("No se puede resolver")
      ## Analizar el estado del modelo
      # print("Código de estado:", solver.status_name())
      # print("Número de nodos explorados:", solver.NumBranches())
      # print("Tiempo de ejecución:", solver.WallTime())
      return f'"No se puede resolver",\n "Código de estado:", {solver.status_name()} \n "Número de nodos explorados:", {solver.NumBranches(),},"Tiempo de ejecución:", {solver.WallTime()}'

    lis = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
      for teacher in self.teachers_names:
        for subject in self.dict_teachers_to_subjects[teacher]:
          for classroom in self.classrooms_names:
            for group in self.groups_names:
              for shift in self.shifts:
                for day in self.days:
                  if solver.value(self.vars[teacher, subject, classroom, group, shift, day]) == 1:
                    to_print = f'profesor:{teacher},asignatura:{subject},aula:{classroom},grupo:{group},turno:{shift},dia:{day}'
                    # print(to_print)
                    lis += self._list_para_dataframe(teacher, subject, classroom, group, shift, day)
                    if show_all_exceptions:
                      self.calendar.add(group, classroom, teacher, str(day), str(shift), subject)
                    else:
                      try:
                        self.calendar.add(group, classroom, teacher, str(day), str(shift), subject)
                      except Exception as e:
                        raise Exception(f'En {to_print} se lanzo el error: \n {e}')

    # Chequea que se cumple la cantidad de horas clases por grupo de a las asignaturas por semana
    self.calendar.finish()
    return to_data_frame(lis)



  def _check_constraints(self, teachers_name: list[str], subjects_name: list[str],
                         classrooms_name: list[str], groups_name: list[str]
                         , shifts_int: list[int], days_int: list[int]):
    """
    Chequea que las restricciones tengan sus valores en la entrada original
    :param teachers_name:
    :param subjects_name:
    :param classrooms_name:
    :param groups_name:
    :param shifts_int:
    :param days_int:
    :return:
    """
    self._check_exist_in_list(teachers_name, self.teachers_names, "Teacher")
    self._check_exist_in_list(subjects_name, self.subjects_name_list, "Subject")
    self._check_exist_in_list(classrooms_name, self.classrooms_names, "Classroom")
    self._check_exist_in_list(groups_name, self.groups_names, "Group")
    self._check_exist_in_list(shifts_int, self.shifts, "Shift")
    self._check_exist_in_list(days_int, self.days, "Day")

  def _create_sum_for_optional_hard_restriction(self, teachers_name: list[str], subjects_name: list[str],
                                                classrooms_name: list[str], groups_name: list[str]
                                                , shifts_int: list[int], days_int: list[int]):
    """Crea la sumatoria de las combinaciones
     de las listas que se le pasan para que despues se puedan asignar
      si se debe cumplir la restriccion s==1 o no s==0"""
    self._check_constraints(teachers_name, subjects_name, classrooms_name, groups_name, shifts_int, days_int)
    try:
      s = sum(self.get_var(teacher_name, subject_name, classroom_name, group_name, shift_int, day_int)
              for teacher_name in teachers_name for subject_name in subjects_name for classroom_name in classrooms_name
              for group_name in groups_name for shift_int in shifts_int for day_int in days_int
              if subject_name in self.dict_teachers_to_subjects[teacher_name])

      return s
    except Exception as e:

      raise Exception(f"Error en crear la suma para las opciones bases: {str(e)}")

  # Chequear los profesores
  def add_optional_hard_constraints(self, teachers_name: list[str], subjects_name: list[str],
                                    classrooms_name: list[str], groups_name: list[str]
                                    , shifts_int: list[int], days_int: list[int], count_to_be_equals: int):
    """Se da una lista de anterior que tiene añade una condición hard que la
     combinatoria de lo que está en las listas suma el count_to_be_equals osea se tiene que cumplir
     OJO:Peligroso de usar se recomienda usar el add_False_hard_constraints para si se quiere restringir o el
     add_True_hard_constraints si se quiere obligar a que suceda

     """
    self._check_constraints(teachers_name, subjects_name, classrooms_name, groups_name, shifts_int, days_int)

    try:

      s = self._create_sum_for_optional_hard_restriction(teachers_name, subjects_name, classrooms_name, groups_name,
                                                         shifts_int, days_int)
      if not isinstance(count_to_be_equals, int):
        raise Exception(f"No es un numero es un {type(count_to_be_equals)}")
      self.model.add(s == count_to_be_equals)
      if count_to_be_equals<0:
        raise AddNewConstraintException(f'count_to_be_equals has to be >=0 and it s be {count_to_be_equals}')
    except Exception as e:
      raise Exception(f'El error en agregar restricciones opcionales: {str(e)}')

  def add_False_hard_constraints(self, teachers_name: list[str], subjects_name: list[str],
                                 classrooms_name: list[str], groups_name: list[str]
                                 , shifts_int: list[int], days_int: list[int]):
    """Se da una lista de anterior que tiene añade una condición hard que la
     combinatoria de lo que está en las listas suma 0 osea se tiene que cumplir"""

    self.add_optional_hard_constraints(teachers_name, subjects_name, classrooms_name, groups_name,
                                       shifts_int, days_int, 0)

  def add_True_hard_constraints(self, teachers_name: list[str], subjects_name: list[str],
                                classrooms_name: list[str], groups_name: list[str]
                                , shifts_int: list[int], days_int: list[int]):
    """Se da una lista de anterior que tiene añade una condición hard que la
     combinatoria de lo que está en las listas suma 1 osea se tiene que cumplir"""

    self.add_optional_hard_constraints(teachers_name, subjects_name, classrooms_name, groups_name,
                                       shifts_int, days_int, 1)

  def add_Maximize_soft_constraints(self, teachers_name: list[str], subjects_name: list[str],
                                    classrooms_name: list[str], groups_name: list[str]
                                    , shifts_int: list[int], days_int: list[int], alpha_value: int):
    if alpha_value <= 0:
      raise Exception(f"El alpha_value debe ser estrictamente positivo y es {alpha_value}")
    """
    Agrega una condición suave osea que trata de optimizar para que se cumpla
    Al maximizar un valor positivo da prioridad a este que se cumpla
    """

    s = self._create_sum_for_optional_hard_restriction(teachers_name, subjects_name, classrooms_name, groups_name,
                                                       shifts_int, days_int)

    self.model.Maximize(alpha_value * s)

  def add_Minimize_soft_constraints(self, teachers_name: list[str], subjects_name: list[str],
                                    classrooms_name: list[str], groups_name: list[str]
                                    , shifts_int: list[int], days_int: list[int], alpha_value: int):
    """
        Agrega una condición suave osea que trata de optimizar para que se cumpla
        Al minimizar un valor positivo da prioridad a este que no se cumpla o se cumpla lo menor posible
        """

    if alpha_value <= 0:
      raise Exception(f"El alpha_value debe ser estrictamente positivo y es {alpha_value}")

    s = self._create_sum_for_optional_hard_restriction(teachers_name, subjects_name, classrooms_name, groups_name,
                                                       shifts_int, days_int)

    self.model.Minimize(alpha_value * s)
