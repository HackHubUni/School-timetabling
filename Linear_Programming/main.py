

from Linear_Programming.solver import solver
def main():
  subjects_name_list = ["Programación", "AlgrebraCP", "AlgebraConf"]  # "AlgrebraCP", "Programación"]
  dict_subjects_by_time = {"Programación": 2, "AlgrebraCP": 2, "AlgebraConf": 1}
  teachers_names = ["Piad", "Paco", "Celia"]  # "Paco", "Celia"]
  classrooms_names = ["1", "2", "3", "Postgrado"]
  groups_names = ["C111", "C112", "cvvv"]
  dict_group_subject_time = {}
  for item in groups_names:
    dict_group_subject_time[item] = dict_subjects_by_time

  shifts = [1, 2, 3]
  days = [1, 2]

  dict_teachers_to_subjects = {
    "Piad": ["Programación", "AlgrebraCP"],
    "Celia": ["AlgebraConf"],
    "Paco": ["AlgrebraCP"],

  }
  solver(subjects_name_list,dict_subjects_by_time,teachers_names,classrooms_names,groups_names,dict_group_subject_time,shifts,days,dict_teachers_to_subjects)

if __name__ == "__main__":
  main()
