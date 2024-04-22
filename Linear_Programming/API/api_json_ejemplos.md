curl -X POST -H "Content-Type: application/json" -d '{
    "subjects_name_list": [...],
    "dict_subjects_by_time": {...},
    "teachers_names": [...],
    "classrooms_names": [...],
    "groups_names": [...],
    "dict_group_subject_time": {...},
    "shifts": [...],
    "days": [...],
    "dict_teachers_to_subjects": {...}
}' http://localhost:5000/solver
