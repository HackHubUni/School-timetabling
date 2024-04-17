from ortools.sat.python import cp_model
from Linear_Programming.utils import Calendar

def main():
    # Crear el modelo
    model = cp_model.CpModel()

    asignaturas = ["Programación", "AlgrebraCP", ]  # "AlgrebraCP", "Programación"]
    asignaturas_tiempo = {"Programación": 2, "AlgrebraCP": 2}
    profesores = ["Piad", "Paco"]  # "Paco", "Celia"]
    aulas = ["1", "2", "3", "Postgrado"]
    grupos = ["C111", "C112", "cvvv"]
    grupo_asignatura_tiempo = {}
    for item in grupos:
        grupo_asignatura_tiempo[item] = asignaturas_tiempo

    turnos = [1, 2]
    dias = [1, 2]

    asignaturas_profes = {
      "Piad": ["Programación"],
      # "Celia": ["AlgebraConf"],
      "Paco": ["AlgrebraCP"],

    }

    asignatura_list_profes= {
      "Programación":["Piad"],
      # "Celia": ["AlgebraConf"],
      "AlgrebraCP":["Paco"]

    }

    calendar = Calendar(asignaturas, profesores, asignatura_list_profes,grupo_asignatura_tiempo,len(dias),len(turnos),aulas,grupos )

    # Crear las variables
    # vars = {}
    # for profesor in profesores:
    #    for asignatura in asignaturas_profes[profesor]:
    #        for aula in aulas:
    #            for grupo in grupos:
    #                for turno in turnos:
    #                    for dia in dias:
    #                        vars[profesor, asignatura, aula, grupo, turno, dia] = model.NewBoolVar(
    #                            f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')
    vars = {}
    for dia in dias:
      for turno in turnos:
        for grupo in grupos:
          for asignatura in asignaturas:
            for aula in aulas:
              for profesor in profesores:
                vars[profesor, asignatura, aula, grupo, turno, dia] = model.NewBoolVar(
                  f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')

    # Que siempre se den todos los turnos de las asignaturas en cada grupo
    for asignatura in asignaturas:
      for grupo in grupos:
        s = sum(
          vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in profesores for aula in aulas
          for turno in turnos for dia in dias if asignatura in asignaturas_profes[profesor])
        model.add(s == asignaturas_tiempo[asignatura])

    # Que un grupo pueda estar en un turno en una sola aula
    for dia in dias:
      for turno in turnos:
        for grupo in grupos:
          s = sum(vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in profesores
                  for asignatura in asignaturas
                  for aula in aulas
                  if asignatura in asignaturas_profes[profesor])
          model.add(s <= 1)

    # Solo se puede asignar a un aula una materia un dia x
    for aula in aulas:
      for dia in dias:
        for turno in turnos:
              s = sum(
                vars[profesor, asignatura, aula, grupo, turno, dia] for grupo in grupos for profesor in profesores
                for asignatura in asignaturas if asignatura in asignaturas_profes[profesor])
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

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
      for profesor in profesores:
        for asignatura in asignaturas_profes[profesor]:
          for aula in aulas:
            for grupo in grupos:
              for turno in turnos:
                for dia in dias:
                  if solver.value(vars[profesor, asignatura, aula, grupo, turno, dia]) == 1:
                    to_print= f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}'
                    print(to_print)

                    try:
                        calendar.add(grupo,aula,profesor,str(dia),str(turno),asignatura)
                    except Exception as e:
                      raise Exception(f'En {to_print} se lanzo el error: \n { e}')


    #Chequea que se cumple la cantidad de horas clases por grupo de alas asignaturas por semana
    calendar.finish()
if __name__ == "__main__":
    main()
