import os
import pickle
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from Linear_Programming.solver import TimeTablingSolver
from schema import SolverSchema
from printer import send_excel

app = Flask(__name__)
solver_schema = SolverSchema()


@app.route('/solver', methods=['POST'])
def create_solver():
  data = request.get_json()
  print(data)
  try:
    validated_data = solver_schema.load(data)
  except ValidationError as e:
    return jsonify({"error": e.messages}), 400

  solver = TimeTablingSolver(**validated_data)

  # Ensure the resources directory exists
  os.makedirs('resources', exist_ok=True)

  # Serialize and save the solver instance
  with open('resources/solver.pkl', 'wb') as f:
    pickle.dump(solver, f)

  return {"message": "Solver instance created successfully"}, 201


@app.route('/dataframe', methods=['GET'])
def get_dataframe():
  # Deserializar la instancia de solver
  if os.path.exists('resources/solver.pkl'):
    with open('resources/solver.pkl', 'rb') as f:
      solver = pickle.load(f)
  else:
    return jsonify({"error": "Solver instance not found"}), 404

  try:
    df = solver.solve()
  except Exception as e:  # Catch any errors thrown by solver.solve()
    return jsonify({"error": str(e)}), 500
  if isinstance(df,str):
    return jsonify({df}),200
  df_json = df.to_json(orient='split')

  return jsonify(df_json)


@app.route('/solver/schema', methods=['GET'])
def get_solver_schema():
  # Return the fields of the schema instead of trying to serialize the schema instance itself
  return jsonify({field: str(type_) for field, type_ in solver_schema.fields.items()})


@app.route('/download_excel')
def download_excel():
  # Deserializar la instancia de solver
  if os.path.exists('resources/solver.pkl'):
    with open('resources/solver.pkl', 'rb') as f:
      solver = pickle.load(f)
  else:
    return jsonify({"error": "Solver instance not found"}), 404

  try:
    df = solver.solve()
  except Exception as e:  # Catch any errors thrown by solver.solve()
    return jsonify({"error": str(e)}), 500
  #Si es un str es un error
  if isinstance(df, str):
    return jsonify({df}), 200

  return send_excel(df)


if __name__ == '__main__':
  app.run(port=7000, debug=True)
