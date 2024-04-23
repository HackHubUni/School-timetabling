import os
import pickle
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from src.solver import TimeTablingSolver
from API.schema import *
from API.utils import serialize_solver, check_schema, deserialize
from src.printer import send_excel

app = Flask(__name__)
solver_schema = SolverSchema()


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
    return jsonify({df}), 200
  df_json = df.to_json(orient='split')

  return jsonify(df_json)


@app.route('/solver/schema', methods=['GET'])
def get_solver_schema():
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in solver_schema.fields.items()})


@app.route('/download_excel')
def download_excel():

  try:
    solver = deserialize()
    print(type(solver))
    df = solver.solve()
    

    # Si es un str es un error
    if isinstance(df, str):
      return jsonify({df}), 200
    
    return send_excel(df)
  except Exception as e:
    return jsonify({"error": "Solver instance not found"}), 404



# To add optinals HardConstrainst

@app.route('/x', methods=['POST'])
def add_hard_optional_constraints():
  schema = optional_hard_constraints()
  try:

    validated_data = check_schema(schema)
    solver:TimeTablingSolver = deserialize()
    print(validated_data)
    solver.add_optional_hard_constraints(**validated_data)
    print("Added")
    serialize_solver(solver)
    return {"message": "Solver hard optionals constraints added"}, 201

  except Exception as e:
    print(str(e))
    return jsonify({"error": str(e)}), 500

 #Condiciones hard opcionales se añaden
@app.route('/solver/TrueHardConstraints', methods=['POST'])
def true_hard_constraints():
  schema = TrueHardConstraints()
  try:
    validated_data = check_schema(schema)
    solver:TimeTablingSolver = deserialize()
    solver.add_True_hard_constraints(**validated_data)
    serialize_solver(solver)

  except Exception as e:
    return jsonify({"error": e}), 500

@app.route('/solver/FalseHardConstraints', methods=['POST'])
def false_hard_constraints():
  schema = FalseHardConstraints()
  try:
    validated_data = check_schema(schema)
    solver:TimeTablingSolver = deserialize()
    solver.add_False_hard_constraints(**validated_data)
    serialize_solver(solver)

  except Exception as e:
    return jsonify({"error": e}), 500


@app.route('/solver/MaximizeSoftConstraints', methods=['POST'])
def maximize_soft_constraints():
  schema = MaximizeSoftConstraints()
  try:
    validated_data = check_schema(schema)
    solver:TimeTablingSolver = deserialize()
    solver.add_Maximize_soft_constraints(**validated_data)
    serialize_solver(solver)

  except Exception as e:
    return jsonify({"error": e}), 500

@app.route('/solver/MinimizeSoftConstraints', methods=['POST'])
def minimize_soft_constraints():
  schema = MinimizeSoftConstraints()
  try:
    validated_data = check_schema(schema)
    solver:TimeTablingSolver = deserialize()
    solver.add_Minimize_soft_constraints(**validated_data)
    serialize_solver(solver)

  except Exception as e:
    return jsonify({"error": e}), 500






if __name__ == '__main__':
  app.run(port=7000, debug=True)
