import os

from flask_restx import Namespace, Resource, fields
from API.schema import SolverSchema, OptionalHardConstraints, TrueHardConstraints, FalseHardConstraints, \
  MaximizeSoftConstraintsSchema, MinimizeSoftConstraintsSchemaSchema
from API.utils import serialize_solver, check_schema, deserialize
from src.printer import send_excel
from src.solver import TimeTablingSolver

import os
import pickle
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from src.solver import TimeTablingSolver
from API.schema import SolverSchema, OptionalHardConstraints, TrueHardConstraints, FalseHardConstraints, \
  MaximizeSoftConstraintsSchema, MinimizeSoftConstraintsSchemaSchema
from API.utils import serialize_solver, check_schema, deserialize
from src.printer import send_excel



app = Flask(__name__)
solver_schema = SolverSchema()


from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='1.0', title='Mi API', description='Una descripción de la API', doc='/swagger/')
# Define un espacio de nombres

# Define un espacio de nombres
ns = Namespace('miapi', description='Operaciones de Mi API')

# Define una ruta dentro del espacio de nombres
@ns.route('/ruta')
class MiRecurso(Resource):
    def get(self):
        return {'mensaje': '¡Hola, mundo!'}

# Aca se llama para crear un horario con las restricciones básicas
@ns.route('/solver', methods=['POST'])
class CreateSolver(Resource):
    def post(self):
        try:
            validated_data = check_schema(SolverSchema())
        except ValidationError as e:
            return {"error": e.messages}, 400

        solver = TimeTablingSolver(**validated_data)

        # Serialize the solver in resources folder
        serialize_solver(solver)

        return {"message": "Solver instance created successfully"}, 201

#Para recuperar un dataframe del horario que se creo
@ns.route('/dataframe', methods=['GET'])
class GetDataframe(Resource):
    def get(self):
        # Deserializar la instancia de solver
        if os.path.exists('../resources/solver.pkl'):
            with open('../resources/solver.pkl', 'rb') as f:
                solver = pickle.load(f)
        else:
            return {"error": "Solver instance not found"}, 404

        try:
            df = solver.solve()
        except Exception as e:  # Catch any errors thrown by solver.solve()
            return {"error": str(e)}, 500
        if isinstance(df, str):
            return {df}, 200
        df_json = df.to_json(orient='split')

        return df_json

#Para tener el esquema de como setean los datos
@ns.route('/solver/schema', methods=['GET'])
class GetSolverSchema(Resource):
    def get(self):
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in SolverSchema().fields.items()}

#Add optional HardConstraints Schema
@ns.route('/solver/optional_hard_constrains_schema', methods=['GET'])
class GetOptionalHardConstrainsSchema(Resource):
    def get(self):
        schema=OptionalHardConstraints()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}

#Para descargar los datos de los excel
@ns.route('/download_excel')
class DownloadExcel(Resource):
    def get(self):
        try:
            solver = deserialize()
            try:
                df = solver.solve()
            except Exception as e:  # Catch any errors thrown by solver.solve()
                return {"error": str(e)}, 500
            # Si es un str es un error
            if isinstance(df, str):
                return {df}, 200

            return send_excel(df)
        except Exception as e:
            return {"error": "Solver instance not found"}, 404

# To add optinals HardConstrainst
@ns.route('/solver/add_hard_optional_constraints', methods=['POST'])
class AddHardOptionalConstraints(Resource):
    def post(self):
        schema = OptionalHardConstraints()

        validated_data = check_schema(schema)
        solver:TimeTablingSolver = deserialize()
        solver.add_optional_hard_constraints(**validated_data)
        serialize_solver(solver)
        return {"message": "Solver hard optionals constraints added"}, 201

#Condiciones hard opcionales se añaden
@ns.route('/solver/TrueHardConstraints', methods=['POST'])
class TrueHardConstraints(Resource):
    def post(self):
        schema = TrueHardConstraints()
        validated_data = check_schema(schema)
        solver:TimeTablingSolver = deserialize()
        solver.add_True_hard_constraints(**validated_data)
        serialize_solver(solver)
        return {"message": "Solver hard optionals constraints added"}, 201

@ns.route('/solver/FalseHardConstraints', methods=['POST'])
class FalseHardConstraints(Resource):
    def post(self):
        schema = FalseHardConstraints()
        validated_data = check_schema(schema)
        solver:TimeTablingSolver = deserialize()
        solver.add_False_hard_constraints(**validated_data)
        serialize_solver(solver)
        return {"message": "Solver hard optionals constraints added"}, 201


@ns.route('/solver/MaximizeSoftConstraints', methods=['POST'])
class MaximizeSoftConstraints(Resource):
    def post(self):
        schema = MaximizeSoftConstraintsSchema()
        validated_data = check_schema(schema)
        solver:TimeTablingSolver = deserialize()
        solver.add_Maximize_soft_constraints(**validated_data)
        serialize_solver(solver)
        return {"message": "Solver hard optionals constraints added"}, 201

@ns.route('/solver/MinimizeSoftConstraints', methods=['POST'])
class MinimizeSoftConstraints(Resource):
    def post(self):
        schema = MinimizeSoftConstraintsSchemaSchema()
        validated_data = check_schema(schema)
        solver:TimeTablingSolver = deserialize()
        solver.add_Minimize_soft_constraints(**validated_data)
        serialize_solver(solver)
        return {"message": "Solver hard optionals constraints added"}


# Asegúrate de que 'ns' es el espacio de nombres que creaste
@ns.route('/solver/optional_hard_constrains_schema', methods=['GET'])
class GetOptionalHardConstrainsSchema(Resource):
    def get(self):
        schema=OptionalHardConstraints()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}

@ns.route('/solver/true_hard_constrains_schema', methods=['GET'])
class GetTrueHardConstrainsSchema(Resource):
    def get(self):
        schema=TrueHardConstraints()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}

@ns.route('/solver/false_hard_constrains_schema', methods=['GET'])
class GetFalseHardConstrainsSchema(Resource):
    def get(self):
        schema=FalseHardConstraints()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}

@ns.route('/solver/maximize_soft_constrains_schema', methods=['GET'])
class GetMaximizeSoftConstrainsSchema(Resource):
    def get(self):
        schema=MaximizeSoftConstraintsSchema()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}

@ns.route('/solver/minimize_soft_constrains_schema', methods=['GET'])
class GetMinimizeSoftConstrainsSchema(Resource):
    def get(self):
        schema=MinimizeSoftConstraintsSchemaSchema()
        # Return the fields of the schema instead of trying to serialize the schema instance itself
        return {field: str(type_) for field, type_ in schema.fields.items()}



# Asegúrate de que 'api' es la instancia de Api que creaste
api.add_namespace(ns)
if __name__ == '__main__':
  app.run(port=7000, debug=True)
