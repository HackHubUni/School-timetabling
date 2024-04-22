from marshmallow import Schema, fields

class SolverSchema(Schema):
    subjects_name_list = fields.List(fields.Str(), required=True)
    dict_subjects_by_time = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)
    teachers_names = fields.List(fields.Str(), required=True)
    classrooms_names = fields.List(fields.Str(), required=True)
    groups_names = fields.List(fields.Str(), required=True)
    dict_group_subject_time = fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(), values=fields.Int()), required=True)
    shifts = fields.List(fields.Int(), required=True)
    days = fields.List(fields.Int(), required=True)
    dict_teachers_to_subjects = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()), required=True)
