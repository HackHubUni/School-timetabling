from ortools.sat.python import cp_model

# Crear el modelo
model = cp_model.CpModel()

asignaturas = ["AlgebraConf", "AlgebraCP", "Programación"]
asignaturas_tiempo = {"AlgebraConf": 1, "AlgebraCP": 1, "Programación": 2} # Corregido el nombre de la asignatura
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

# Solo se puede asignar a un aula una materia un día x
for aula in aulas:
    for dia in dias:
        for turno in turnos:
            for grupo in grupos:
                for profesor in profesores:
                    s = sum(
                        vars[profesor, asignatura, aula, grupo, turno, dia]
                        for asignatura in asignaturas if asignatura in asignaturas_profes[profesor])
                    model.add(s <= 1)

# Cada asignatura debe ser impartida al menos una vez
for asignatura in asignaturas:
    s = sum(
            vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in profesores for aula in aulas
            for turno in turnos for dia in dias for grupo in grupos if asignatura in asignaturas_profes[profesor])
    model.add(s ==asignaturas_tiempo[asignatura] )

# Agregar suposiciones
assumptions = []
for profesor in profesores:
    for asignatura in asignaturas_profes[profesor]:
        for aula in aulas:
            for grupo in grupos:
                for turno in turnos:
                    for dia in dias:
                        assumptions.append(vars[profesor, asignatura, aula, grupo, turno, dia])

# Agregar las suposiciones al modelo
model.AddAssumptions(assumptions)

# Crear el solucionador y resolver
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Verificar las suposiciones
if status == cp_model.INFEASIBLE:
    print("No se puede resolver")
    # Analizar el estado del modelo
    print("Código de estado:", solver.status_name())
    print("Número de nodos explorados:", solver.NumBranches())
    print("Tiempo de ejecución:", solver.WallTime())
    # Verificar las suposiciones
    for i, assumption in enumerate(assumptions):
        if not solver.AssumptionValue(assumption):
            print(f"La suposición {i} es falsa.")
else:
    print("El modelo es feasible.")
    for profesor in profesores:
        for asignatura in asignaturas_profes[profesor]:
            for aula in aulas:
                for grupo in grupos:
                    for turno in turnos:
                        for dia in dias:
                            if solver.value(vars[profesor, asignatura, aula, grupo, turno, dia]) == 1:
                                print(
                                    f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')



