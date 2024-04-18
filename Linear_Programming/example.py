import copy
from enum import Enum
from Linear_Programming.solver import TimeTablingSolver
from Linear_Programming.printer import to_excel

class Subjects(Enum):
  Programacion = "Programación"
  ProgramaciónCp = "ProgramaciónCp"
  Algebra = "Algebra"
  AlgebraCP = "AlgebraCP"
  Analisis = "Analisis"
  AnalisisCp = "AnalisisCp"
  Logica = "Logica"
  LogicaCp = "LogicaCp"

  def __str__(self):
    return self.value


class Teachers(Enum):
  Piad = "Piad"
  Idania = "Idania"
  Celia = "Celia"
  Yudivian = "Yudivian"
  DanielL = "DanielL"
  OmarL = "OmarLogica"
  CarmenL = "CarmentL"
  ErnestoA = "ErnestoAnalisis"
  CristinaA = "CristinaA"
  MercedesA = "MercedesA"
  DalianisAL = "DalianisAlgebra"
  PepeAl = "PepeAL"
  CayetanaAL = "CayetanaAL"
  PacoP = "PacoP"
  HectorP = "HectorP"
  CarlaP = "CarlaP"

  def __str__(self):
    return self.value



import pandas as pd

def main():
  subjects_name_list = [Subjects.Programacion,
                        Subjects.ProgramaciónCp,
                        Subjects.Algebra,
                        Subjects.AlgebraCP,
                        Subjects.Analisis,
                        Subjects.AnalisisCp,
                        Subjects.Logica,
                        Subjects.LogicaCp, ]
  subjects_name_list =[str(x) for x in subjects_name_list]

  dict_subjects_by_time = {Subjects.Programacion: 1,
                           Subjects.ProgramaciónCp: 2,
                           Subjects.Algebra: 1,
                           Subjects.AlgebraCP: 2,
                           Subjects.Analisis: 1,
                           Subjects.AnalisisCp: 2,
                           Subjects.Logica: 1,
                           Subjects.LogicaCp: 1
                           }

  dict_subjects_by_time = {str(x): dict_subjects_by_time[x] for x in dict_subjects_by_time.keys()}

  teachers_names = [
    Teachers.Piad,
    Teachers.Idania,
    Teachers.Celia,
    Teachers.Yudivian,
    Teachers.DanielL,
    Teachers.OmarL,
    Teachers.CarmenL,
    Teachers.ErnestoA,
    Teachers.CristinaA,
    Teachers.MercedesA,
    Teachers.DalianisAL,
    Teachers.PepeAl,
    Teachers.CayetanaAL,
    Teachers.PacoP,
    Teachers.HectorP,
    Teachers.CarlaP,

  ]
  teachers_names = [str(x) for x in teachers_names]

  classrooms_names = [ f'{x}'for x in range(1,6)]+["Postgrado"]

  groups_names = [f"C11{x}" for x in range(1, 7)]

  dict_group_subject_time = {}

  for item in groups_names:
    dict_group_subject_time[item] = dict_subjects_by_time

  shifts = [1, 2, 3]
  days = [x for x in range(1, 6)]

  dict_teachers_to_subjects = {

    Teachers.Piad: [Subjects.Programacion],
    Teachers.Idania: [Subjects.Analisis],
    Teachers.Celia: [Subjects.Algebra],
    Teachers.Yudivian: [Subjects.Logica],
    Teachers.DanielL: [Subjects.LogicaCp],
    Teachers.OmarL: [Subjects.LogicaCp],
    Teachers.CarmenL: [Subjects.LogicaCp],
    Teachers.ErnestoA: [Subjects.AnalisisCp],
    Teachers.CristinaA: [Subjects.AnalisisCp],
    Teachers.MercedesA: [Subjects.AnalisisCp],
    Teachers.DalianisAL: [Subjects.AlgebraCP],
    Teachers.PepeAl: [Subjects.AlgebraCP],
    Teachers.CayetanaAL: [Subjects.AlgebraCP],
    Teachers.PacoP: [Subjects.ProgramaciónCp],
    Teachers.HectorP: [Subjects.ProgramaciónCp],
    Teachers.CarlaP: [Subjects.ProgramaciónCp],

  }

  dict_teachers_to_subjects = {str(x):[str(y)for y in dict_teachers_to_subjects[x]] for x in dict_teachers_to_subjects.keys()}

  solver=TimeTablingSolver(subjects_name_list, dict_subjects_by_time, teachers_names, classrooms_names, groups_names,
         dict_group_subject_time, shifts, days, dict_teachers_to_subjects)

  solver.add_optional_hard_constraints(teachers_names,[str(Subjects.Algebra)],classrooms_names,groups_names,shifts,[1],len(groups_names))
  a=copy.deepcopy(subjects_name_list)
  a.remove(str(Subjects.Algebra))
  solver.add_False_hard_constraints(teachers_names,a,classrooms_names,groups_names,shifts,[1])

  df=solver.solve()

  to_excel(df)




if __name__ == "__main__":
  main()
