from ortools.sat.python import cp_model

# Crear el modelo
model = cp_model.CpModel()

asignaturas = ["AlgebraConf", "Alge{braCP", "Programación"]
asignaturas_tiempo = {"AlgebraConf": 1, "AlgrebraCP": 1, "Programación": 2}
profesores = ["Piad", "Paco", "Celia"]
aulas = ["1", "2", "3", "Postgrado"]
grupos = ["C111", "C112", "D111"]
turnos = [1, 2, 3]
dias = [1, 2, 3, 4, 5]

asignaturas_profes = {
    "Piad": ["Programación"],
    "Celia": ["AlgebraConf"],
    "Paco": ["AlgebraCP"],

}
# Crear las variables
vars = {}
for profesor in profesores:
    for asignatura in asignaturas_profes[profesor]:
        for aula in aulas:
            for grupo in grupos:
                for turno in turnos:
                    for dia in dias:
                        vars[profesor, asignatura, aula, grupo, turno, dia] = model.NewBoolVar(
                            f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')

    # Restricciones

    # Todos los turnos de una asignatura deben darse a la semana
    # for asignatura in asignaturas:
    #    time_asig = asignaturas_tiempo[asignatura]
    #    for grupo in grupos:
    #        total = model.NewIntVar(0, 0, "Init")
    #        for dia in dias:
    #            for turno in turnos:
    #                for aula in aulas:
    #                    for profesor in profesores:
    #                        if not asignatura in asignaturas_profes[profesor]:
    #                            continue
    #                        total += vars[profesor, asignatura, aula, grupo, turno, dia]
    #       model.add(total == time_asig)

# Solo se puede asignar a un aula una materia un dia x
for aula in aulas:
    for dia in dias:
        for turno in turnos:
            for grupo in grupos:
                for profesor in profesores:
                    s = sum(
                        vars[profesor, asignatura, aula, grupo, turno, dia]
                        for asignatura in asignaturas if asignatura in asignaturas_profes[profesor])
                    model.add(s <= 1)

#for asignatura in asignaturas:
#    for grupo in grupos:
#        s = sum(
#            vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in profesores for aula in aulas
#            for turno in turnos for dia in dias if asignatura in asignaturas_profes[profesor])
#        model.add(s >= 1)
for asignatura in asignaturas:
    s = sum(
            vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in profesores for aula in aulas
            for turno in turnos for dia in dias for grupo in grupos if asignatura in asignaturas_profes[profesor])
    model.add(s >= 1)


# Crear el solucionador y resolver
solver = cp_model.CpSolver()
status = solver.Solve(model)
print(status)
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
                            if solver.value(vars[profesor, asignatura, aula, grupo, turno, dia]) == 0:
                                print(
                                    f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')
