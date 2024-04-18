from flask import Flask, request
from Linear_Programming.solver import TimeTablingSolver

app = Flask(__name__)

@app.route('/solver', methods=['POST'])
def create_solver():
    data = request.get_json()

    subjects_name_list = data.get('subjects_name_list')
    dict_subjects_by_time = data.get('dict_subjects_by_time')
    teachers_names = data.get('teachers_names')
    classrooms_names = data.get('classrooms_names')
    groups_names = data.get('groups_names')
    dict_group_subject_time = data.get('dict_group_subject_time')
    shifts = data.get('shifts')
    days = data.get('days')
    dict_teachers_to_subjects = data.get('dict_teachers_to_subjects')

    solver = TimeTablingSolver(subjects_name_list, dict_subjects_by_time, teachers_names, classrooms_names, groups_names,
                               dict_group_subject_time, shifts, days, dict_teachers_to_subjects)

    return {"message": "Solver instance created successfully"}, 201

if __name__ == '__main__':
    app.run(debug=True)
