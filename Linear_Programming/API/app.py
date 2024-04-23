import os
import pickle
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from src.solver import TimeTablingSolver
from API.schema import SolverSchema, OptionalHardConstraints, TrueHardConstraints, FalseHardConstraints, \
  MaximizeSoftConstraintsSchema, MinimizeSoftConstraintsSchemaSchema
from API.utils import serialize_solver, check_schema, deserialize
from src.printer import send_excel
from src.to_json import groups_to_json

app = Flask(__name__)
solver_schema = SolverSchema()


# Aca se llama para crear un horario con las restricciones básicas
@app.route('/solver', methods=['POST'])
def create_solver():
  try:
    validated_data = check_schema(solver_schema)
  except ValidationError as e:
    return jsonify({"error": e.messages}), 400

  solver = TimeTablingSolver(**validated_data)

  # Serialize the solver in resources folder
  serialize_solver(solver)

  return {"message": "Solver instance created successfully"}, 201


# Para recuperar un dataframe del horario que se creo
@app.route('/dataframe', methods=['GET'])
def get_dataframe():
  # Deserializar la instancia de solver
  if os.path.exists('../resources/solver.pkl'):
    with open('../resources/solver.pkl', 'rb') as f:
      solver = pickle.load(f)
  else:
    return jsonify({"error": "Solver instance not found"}), 404

  try:
    df = solver.solve()
  except Exception as e:  # Catch any errors thrown by solver.solve()
    return jsonify({"error": str(e)}), 500
  if isinstance(df, str):
    return jsonify(df), 200
  df_json = df.to_json(orient='split')

  return jsonify(df_json)


# Para tener el esquema de como setean los datos

@app.route('/solver/schema', methods=['GET'])
def get_solver_schema():
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in solver_schema.fields.items()})


# Add optional HardConstraints Schema
@app.route('/solver/optional_hard_constrains_schema', methods=['GET'])
def get_optional_hard_constrains_schema():
  schema = OptionalHardConstraints()
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in schema.fields.items()})


# Add TrueHardConstraints Schema
@app.route('/solver/true_hard_constrains_schema', methods=['GET'])
def get_true_hard_constrains_schema():
  schema = TrueHardConstraints()
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in schema.fields.items()})


# Add FalseHardConstraints Schema
@app.route('/solver/false_hard_constrains_schema', methods=['GET'])
def get_false_hard_constrains_schema():
  schema = FalseHardConstraints()
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in schema.fields.items()})


# Add MaximizeSoftConstraintsSchema
@app.route('/solver/maximize_soft_constrains_schema', methods=['GET'])
def get_maximize_soft_constrains_schema():
  schema = MaximizeSoftConstraintsSchema()
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in schema.fields.items()})


@app.route('/solver/minimize_soft_constrains_schema', methods=['GET'])
def get_minimize_soft_constrains_schema():
  schema = MinimizeSoftConstraintsSchemaSchema()
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in schema.fields.items()})


# Para descargar los datos de los excel

@app.route('/download_excel')
def download_excel():
  solver: TimeTablingSolver = deserialize()

  df = solver.solve(return_dataFrame=True)

  # Si es un str es un error
  if isinstance(df, str):
    return jsonify({df}), 200
  print("va e entrar al send_excel")
  return send_excel(df)


@app.route('/get_json', methods=['GET'])
def get_json():

  solver: TimeTablingSolver = deserialize()

  groups = solver.solve(return_dataFrame=False)

  # Si es un str es un error
  if isinstance(groups, str):
    return jsonify(groups), 200

  # Convertir la lista de grupos a JSON
  json_grupos = groups_to_json(groups)

  # Devolver la respuesta en formato JSON
  return jsonify(json_grupos)


# To add optinals HardConstrainst

@app.route('/solver/add_hard_optional_constraints', methods=['POST'])
def add_hard_optional_constraints():
  schema = OptionalHardConstraints()

  validated_data = check_schema(schema)
  solver: TimeTablingSolver = deserialize()
  solver.add_optional_hard_constraints(**validated_data)
  serialize_solver(solver)
  return {"message": "Solver hard optionals constraints added"}, 201


# Condiciones hard opcionales se añaden
@app.route('/solver/TrueHardConstraints', methods=['POST'])
def true_hard_constraints():
  schema = TrueHardConstraints()
  validated_data = check_schema(schema)
  solver: TimeTablingSolver = deserialize()
  solver.add_True_hard_constraints(**validated_data)
  serialize_solver(solver)
  return {"message": "Solver hard optionals constraints added"}, 201


@app.route('/solver/FalseHardConstraints', methods=['POST'])
def false_hard_constraints():
  schema = FalseHardConstraints()
  validated_data = check_schema(schema)
  solver: TimeTablingSolver = deserialize()
  solver.add_False_hard_constraints(**validated_data)
  serialize_solver(solver)
  return {"message": "Solver hard optionals constraints added"}, 201


@app.route('/solver/MaximizeSoftConstraints', methods=['POST'])
def maximize_soft_constraints():
  schema = MaximizeSoftConstraintsSchema()
  validated_data = check_schema(schema)
  solver: TimeTablingSolver = deserialize()
  solver.add_Maximize_soft_constraints(**validated_data)
  serialize_solver(solver)
  return {"message": "Solver hard optionals constraints added"}, 201


@app.route('/solver/MinimizeSoftConstraints', methods=['POST'])
def minimize_soft_constraints():
  schema = MinimizeSoftConstraintsSchemaSchema()
  validated_data = check_schema(schema)
  solver: TimeTablingSolver = deserialize()
  solver.add_Minimize_soft_constraints(**validated_data)
  serialize_solver(solver)


if __name__ == '__main__':
  app.run(port=7000, debug=True)
