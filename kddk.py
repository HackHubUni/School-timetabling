from ortools.sat.python import cp_model

# Crear el modelo
model = cp_model.CpModel()

# Datos del problema
profesores = ["Profesor1", "Profesor2", "Profesor3"]
cursos = ["Curso1", "Curso2", "Curso3", "Curso4", "Curso5"]
aulas = ["Aula1", "Aula2", "Aula3"]
franjas_horarias = ["Franja1", "Franja2", "Franja3", "Franja4"]

# Asignaturas que cada profesor puede enseñar
asignaturas_profesores = {
    "Profesor1": ["Curso1", "Curso2"],
    "Profesor2": ["Curso3", "Curso4"],
    "Profesor3": ["Curso5"]
}

# Crear las variables
variables = {}
for profesor in profesores:
    for curso in asignaturas_profesores[profesor]:
        for aula in aulas:
            for franja in franjas_horarias:
                variables[profesor, curso, aula, franja] = model.NewBoolVar('p%s_c%s_a%s_f%s' % (profesor, curso, aula, franja))

# Cada curso debe ser asignado exactamente una vez
for curso in cursos:
    model.Add(sum(variables[profesor, curso, aula, franja] for profesor in profesores for aula in aulas for franja in franjas_horarias if curso in asignaturas_profesores[profesor]) == 1)

# Cada aula solo puede tener un curso a la vez
for aula in aulas:
    for franja in franjas_horarias:
        model.Add(sum(variables[profesor, curso, aula, franja] for profesor in profesores for curso in cursos if curso in asignaturas_profesores[profesor]) <= 1)

# Cada profesor solo puede enseñar un curso a la vez
for profesor in profesores:
    for franja in franjas_horarias:
        model.Add(sum(variables[profesor, curso, aula, franja] for curso in asignaturas_profesores[profesor] for aula in aulas) <= 1)

# Crear el solucionador y resolver
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Imprimir la solución
if status == cp_model.OPTIMAL:
    for profesor in profesores:
        for curso in asignaturas_profesores[profesor]:
            for aula in aulas:
                for franja in franjas_horarias:
                    if solver.Value(variables[profesor, curso, aula, franja]) == 1:
                        print('%s imparte %s en %s durante %s' % (profesor, curso, aula, franja))