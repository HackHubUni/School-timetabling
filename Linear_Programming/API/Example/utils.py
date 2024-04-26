import copy
from enum import Enum
from src.solver import TimeTablingSolver
from src.printer import to_excel


class Subjects(Enum):
  Programacion = "Programacion"
  ProgramaciónCp = "ProgramacionCp"

  Algebra = "Algebra"
  AlgebraCP = "AlgebraCP"

  Analisis = "Analisis"
  AnalisisCp = "AnalisisCp"

  Logica = "Logica"
  LogicaCp = "LogicaCp"

  # 2 año

  Discreta1Con = "Discreta1Con"
  Discreta1Cp = "Discreta1Cp"

  NumericaCon = "NumericaCon"
  NumericaCp = "NumericaCp"

  EdoCon = "EdoCon"
  EdoCP = "EdoCP"

  SOCon = "SOCon"
  SOCP = "SOCp"

  # 3er año

  CompilacionCon = "CompilacionCon"
  CompilacionCp = "CompilacionCp"

  RedesConf = "RedesCon"
  RedesCp = "RedesCp"

  OptimizacionCon = "OptimizacionCon"
  OptimizacionCp = "OptimizacionCp"

  IACon = "AICon"
  IACp = "AICp"

  # 4to

  MLCon = "MLCon"
  MLCp = "MLCp"

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

  # 3ro
  JuanPabloCom = "JuanPabloCom"
  GustavoCom = "GustavoCom"
  LiaCom = "LiaCom"

  DalmauRedesAI = "DalmauRedesAI"
  AntonioRedes = "AntonioRedes"

  GemaOPT = "GemaOPT"
  DaneOPT = "DanaOPT"
  ErnestoOPT = "ErnestoOPT"

  PedroAI = "PedroAI"

  def __str__(self):
    return self.value


def main():
  subjects_name_list = [Subjects.Programacion,
                        Subjects.ProgramaciónCp,
                        Subjects.Algebra,
                        Subjects.AlgebraCP,
                        Subjects.Analisis,
                        Subjects.AnalisisCp,
                        Subjects.Logica,
                        Subjects.LogicaCp,

                        # 3ero
                        Subjects.CompilacionCon,
                        Subjects.CompilacionCp,

                        Subjects.RedesConf,
                        Subjects.RedesCp,

                        Subjects.OptimizacionCon,
                        Subjects.OptimizacionCp,

                        Subjects.IACon,
                        Subjects.IACp,

                        ]
  subjects_name_list = [str(x) for x in subjects_name_list]

  dict_subjects_by_time_1ero = {Subjects.Programacion: 1,
                                Subjects.ProgramaciónCp: 2,
                                Subjects.Algebra: 1,
                                Subjects.AlgebraCP: 2,
                                Subjects.Analisis: 1,
                                Subjects.AnalisisCp: 2,
                                Subjects.Logica: 1,
                                Subjects.LogicaCp: 1
                                }

  dict_subjects_by_time_1ero = {str(x): dict_subjects_by_time_1ero[x] for x in dict_subjects_by_time_1ero.keys()}

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

    Teachers.JuanPabloCom,
    Teachers.GustavoCom,
    Teachers.LiaCom,

    Teachers.DalmauRedesAI,
    Teachers.AntonioRedes,

    Teachers.GemaOPT,
    Teachers.DaneOPT,
    Teachers.ErnestoOPT,

    Teachers.PedroAI,

  ]
  teachers_names = [str(x) for x in teachers_names]

  classrooms_names = [f'{x}' for x in range(1, 6)] + ["Postgrado"]

  groups_names_1ero = [f"C11{x}" for x in range(1,2)]

  dict_group_subject_time = {}

  for item in groups_names_1ero:
    dict_group_subject_time[item] = dict_subjects_by_time_1ero

  groups_names_3ero = [f'C31{x}' for x in range(1, 2)]

  dict_subjects_by_time_3ero = {Subjects.CompilacionCon: 1,
                                Subjects.CompilacionCp: 2,

                                Subjects.RedesConf: 1,
                                Subjects.RedesCp: 2,

                                Subjects.OptimizacionCon: 1,
                                Subjects.OptimizacionCp: 2,

                                Subjects.IACon: 1,
                                Subjects.IACp: 2,
                                }
  dict_subjects_by_time_3ero = {str(x): dict_subjects_by_time_3ero[x] for x in dict_subjects_by_time_3ero.keys()}
  for item in groups_names_3ero:
    dict_group_subject_time[item] = dict_subjects_by_time_3ero

  shifts = [1, 2, 3]
  days = [x for x in range(1, 6)]

  dict_subjects_by_time=dict_subjects_by_time_1ero|dict_subjects_by_time_3ero

  groups_names=groups_names_1ero+groups_names_3ero


  dict_teachers_to_subjects = {

    Teachers.Piad: [Subjects.Programacion, Subjects.IACon],
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

    Teachers.JuanPabloCom: [Subjects.Programacion, Subjects.CompilacionCon],
    Teachers.GustavoCom: [Subjects.CompilacionCp],
    Teachers.LiaCom: [Subjects.CompilacionCp],

    Teachers.DalmauRedesAI: [Subjects.IACp, Subjects.RedesConf],
    Teachers.AntonioRedes: [Subjects.RedesCp],

    Teachers.GemaOPT: [Subjects.OptimizacionCon],
    Teachers.DaneOPT: [Subjects.OptimizacionCp],
    Teachers.ErnestoOPT: [Subjects.OptimizacionCp],

    Teachers.PedroAI: [Subjects.IACp],

  }
  dict_teachers_to_subjects = {str(x): [str(y) for y in dict_teachers_to_subjects[x]] for x in
                               dict_teachers_to_subjects.keys()}

  data = {
    "subjects_name_list": subjects_name_list,
    "dict_subjects_by_time": dict_subjects_by_time,
    "teachers_names": teachers_names,
    "classrooms_names": classrooms_names,
    "groups_names": groups_names_1ero,
    "dict_group_subject_time": {group: dict_subjects_by_time for group in groups_names},
    "shifts": shifts,
    "days": days,
    "dict_teachers_to_subjects": dict_teachers_to_subjects
  }

  import json

  json_data = json.dumps(data)

  with open('data.json', 'w') as f:
    json.dump(data, f)


if __name__ == "__main__":
  main()
