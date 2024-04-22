from marshmallow import Schema, fields


class AddBooleanHardConstraintsBase(Schema):


  teachers_name = fields.List(fields.Str(), required=True)
  subjects_name = fields.List(fields.Str(), required=True)
  classrooms_name = fields.List(fields.Str(), required=True)
  groups_name = fields.List(fields.Str(), required=True)
  shifts_int = fields.List(fields.Int(), required=True)
  days_int = fields.List(fields.Int(), required=True)


class OptionalHardConstraints(AddBooleanHardConstraintsBase):
  # A cuanto tiene que ser igual
  count_to_be_equals = fields.Int()


class TrueHardConstraints(AddBooleanHardConstraintsBase):
  pass


class FalseHardConstraints(AddBooleanHardConstraintsBase):
  pass


class SoftConstraintsSchema(AddBooleanHardConstraintsBase):
  alpha_value = fields.Int()


class MaximizeSoftConstraintsSchema(SoftConstraintsSchema):
  pass


class MinimizeSoftConstraintsSchemaSchema(SoftConstraintsSchema):
  pass


class SolverSchema(Schema):
  subjects_name_list = fields.List(fields.Str(), required=True)
  dict_subjects_by_time = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)
  teachers_names = fields.List(fields.Str(), required=True)
  classrooms_names = fields.List(fields.Str(), required=True)
  groups_names = fields.List(fields.Str(), required=True)
  dict_group_subject_time = fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(), values=fields.Int()),
                                        required=True)
  shifts = fields.List(fields.Int(), required=True)
  days = fields.List(fields.Int(), required=True)
  dict_teachers_to_subjects = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()), required=True)

  # hard constraits
  # optional_hard_constraints = fields.List(fields.Nested(optional_hard_constraints()))
