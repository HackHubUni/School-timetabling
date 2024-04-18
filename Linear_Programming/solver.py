from ortools.constraint_solver.pywrapcp import IntVar
from ortools.sat.python import cp_model
from Linear_Programming.utils import Calendar


def _get_dic_subjects_to_teachers(teachers: list[str], subjects: list[str],
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


def solver(subjects_name_list: list[str], dict_subjects_by_time: dict[str:int], teachers_names: list[str],
           classrooms_names: list[str],
           groups_names: list[str], dict_group_subject_time: dict[str, dict[str:int]], shifts: list[int],
           days: list[int], dict_teachers_to_subjects: dict[str, list[str]]):
  """
  Generates a schedule for assigning teachers to subjects in classrooms for different groups and shifts.

  Parameters:
  - subjects_name_list (list[str]): List of subject names to be scheduled.
  - dict_subjects_by_time (dict[str:int]): Dictionary mapping subjects to the number of times they need to be scheduled.
  - teachers_names (list[str]): List of teacher names available for scheduling.
  - classrooms_names (list[str]): List of classroom names available for scheduling.
  - groups_names (list[str]): List of group names to schedule the subjects for.
  - dict_group_subject_time (dict[str,dict[str:int]]): Nested dictionary mapping group names to subjects and the number of times each subject needs to be scheduled.
  - shifts (list[int]): List of shift numbers available for scheduling.
  - days (list[int]): List of day numbers available for scheduling.
  - dict_teachers_to_subjects (dict[str,list[str]]): Dictionary mapping teacher names to the subjects they can teach.

  Returns:
  - None
  """

  # Crear el modelo
  model = cp_model.CpModel()

  dict_subjects_to_teachers = _get_dic_subjects_to_teachers(teachers_names, subjects_name_list,
                                                            dict_teachers_to_subjects)

  calendar = Calendar(subjects_name_list, teachers_names, dict_subjects_to_teachers, dict_group_subject_time, len(days),
                      len(shifts),
                      classrooms_names, groups_names)

  variables: dict[tuple[str, str, str, str, int, int], "IntVar"] = {}
  for dia in days:
    for turno in shifts:
      for grupo in groups_names:
        for asignatura in subjects_name_list:
          for aula in classrooms_names:
            for profesor in teachers_names:
              variables[profesor, asignatura, aula, grupo, turno, dia] = model.NewBoolVar(
                f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')

  # Variable para decir que un profesor puede estar en una sola aula en un turno en especifico
  variables_aux = {}
  for day in days:
    for shift in shifts:
      for teacher in teachers_names:
        for classroom in classrooms_names:
          variables_aux[day, shift, teacher, classroom] = model.NewBoolVar(
            f'Variable auxiliar: profesor:{teacher},aula:{classroom},turno:{shift},dia:{day}   '
          )

  # Que un profesor solo puede estar en un aula a la vez
  for day in days:
    for shift in shifts:
      for teacher in teachers_names:
        s = sum(variables_aux[day, shift, teacher, classroom]
                for classroom in classrooms_names
                )
        model.add(s <= 1)

  #Que siempre se den todos los turnos de las asignaturas en cada grupo
  for asignatura in subjects_name_list:
   for grupo in groups_names:
     s = sum(
       variables[profesor, asignatura, aula, grupo, turno, dia] for profesor in teachers_names for aula in
       classrooms_names
       for turno in shifts for dia in days if asignatura in dict_teachers_to_subjects[profesor])
     model.add(s == dict_subjects_by_time[asignatura])

  #Aca son el and digo que para todos los grupos deben darse todos los turnos pero deben de satisfacer que un profe debe estar en un solo aula
  for asignatura in subjects_name_list:
    for grupo in groups_names:
      for profesor in teachers_names:
        for aula in classrooms_names:
          for turno in shifts:
            for dia in days:
              if asignatura in dict_teachers_to_subjects[profesor]:
                model.AddBoolAnd([variables[profesor, asignatura, aula, grupo, turno, dia],
                                  variables_aux[dia, turno, profesor, aula]]).OnlyEnforceIf( #el onlyEnforceIf asegura que ese and sea verdadero tal que se cumpla el el anterior
                  variables[profesor, asignatura, aula, grupo, turno, dia])
  # Que un grupo pueda estar en un turno en una sola aula
  for dia in days:
    for turno in shifts:
      for grupo in groups_names:
        s = sum(variables[profesor, asignatura, aula, grupo, turno, dia] for profesor in teachers_names
                for asignatura in subjects_name_list
                for aula in classrooms_names
                if asignatura in dict_teachers_to_subjects[profesor])
        model.add(s <= 1)

  # Solo se puede asignar a un aula una materia un dia x
  #Crear variables para esto



  for aula in classrooms_names:
    for dia in days:
      for turno in shifts:
        s = sum(
          variables[profesor, asignatura, aula, grupo, turno, dia] for grupo in groups_names for profesor in
          teachers_names
          for asignatura in subjects_name_list if asignatura in dict_teachers_to_subjects[profesor])
        model.add(s <= 1)



  # Crear el solucionador y resolver
  solver = cp_model.CpSolver()
  status = solver.Solve(model)

  if status == cp_model.INFEASIBLE:
    print("No se puede resolver")
    # Analizar el estado del modelo
    print("Código de estado:", solver.status_name())
    print("Número de nodos explorados:", solver.NumBranches())
    print("Tiempo de ejecución:", solver.WallTime())
    return

  if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for profesor in teachers_names:
      for asignatura in dict_teachers_to_subjects[profesor]:
        for aula in classrooms_names:
          for grupo in groups_names:
            for turno in shifts:
              for dia in days:
                if solver.value(variables[profesor, asignatura, aula, grupo, turno, dia]) == 1:
                  to_print = f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}'
                  print(to_print)
                  if False:
                    calendar.add(grupo, aula, profesor, str(dia), str(turno), asignatura)
                  else:
                    try:
                      calendar.add(grupo, aula, profesor, str(dia), str(turno), asignatura)
                    except Exception as e:
                      raise Exception(f'En {to_print} se lanzo el error: \n {e}')

  # Chequea que se cumple la cantidad de horas clases por grupo de alas asignaturas por semana
  calendar.finish()
