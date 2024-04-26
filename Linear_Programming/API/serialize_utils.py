import os
import pickle
from flask import Flask, request, jsonify
from marshmallow import ValidationError
__folder_path__='../resources'
def serialize_solver(solver):
  # Ensure the resources directory exists
  os.makedirs(__folder_path__, exist_ok=True)

  # Serialize and save the solver instance
  with open(f'{__folder_path__}/solver.pkl', 'wb') as f:
    pickle.dump(solver, f)


def deserialize():
  # Deserializar la instancia de solver
  if os.path.exists(f'{__folder_path__}/solver.pkl'):
    with open(f'{__folder_path__}/solver.pkl', 'rb') as f:
      solver = pickle.load(f)
      return solver
  else:
    raise Exception("No se puede tomar el solver serializado ")


def check_schema(solver_schema):
  data = request.get_json()


  validated_data = solver_schema.load(data)
  return  validated_data


