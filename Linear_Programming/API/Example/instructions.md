

Descripción breve:
En este solver se utiliza una biblioteca de Programación lineal
para resolver el problema del horario
se escogió la biblioteca ortools de google
que brinda unos modulos optimizados para
sat y algortimos para resolución de problemas binarios
dado que todo se puede resumir en
dar en un dia x un turno y una asignaruta en especifico
con un profesor en un aula a un grupo


El solver en su forma simple consta
de inicializar con los datos iniciales
que se envia a la url localhost generalmente por el
puerto 7000 /solver  osea esta url haciendo post
````
http://127.0.0.1:7000/solver
````

con el sgt schema:
````json
{
    "classrooms_names": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>",
    "days": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>",
    "dict_group_subject_time": "<fields.Dict(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid mapping type.'})>",
    "dict_subjects_by_time": "<fields.Dict(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid mapping type.'})>",
    "dict_teachers_to_subjects": "<fields.Dict(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid mapping type.'})>",
    "groups_names": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>",
    "shifts": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>",
    "subjects_name_list": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>",
    "teachers_names": "<fields.List(dump_default=<marshmallow.missing>, attribute=None, validate=None, required=True, load_only=False, dump_only=False, load_default=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': 'Not a valid list.'})>"
}

````

como ejemplo de json de post es
````json
"subjects_name_list": [
    "Programacion",
    "ProgramacionCp",
    "Algebra",
    "AlgebraCP",
    "Analisis",
    "AnalisisCp",
    "Logica",
    "LogicaCp",
    "CompilacionCon",
    "CompilacionCp",
    "RedesCon",
    "RedesCp",
    "OptimizacionCon",
    "OptimizacionCp",
    "AICon",
    "AICp"
  ],
  "dict_subjects_by_time": {
    "Programacion": 1,
    "ProgramacionCp": 2,
    "Algebra": 1,
    "AlgebraCP": 2,
    "Analisis": 1,
    "AnalisisCp": 2,
    "Logica": 1,
    "LogicaCp": 1,
    "CompilacionCon": 1,
    "CompilacionCp": 2,
    "RedesCon": 1,
    "RedesCp": 2,
    "OptimizacionCon": 1,
    "OptimizacionCp": 2,
    "AICon": 1,
    "AICp": 2
  },
  "teachers_names": [
    "Piad",
    "Idania",
    "Celia",
    "Yudivian",
    "DanielL",
    "OmarLogica",
    "CarmentL",
    "ErnestoAnalisis",
    "CristinaA",
    "MercedesA",
    "DalianisAlgebra",
    "PepeAL",
    "CayetanaAL",
    "PacoP",
    "HectorP",
    "CarlaP",
    "JuanPabloCom",
    "GustavoCom",
    "LiaCom",
    "DalmauRedesAI",
    "AntonioRedes",
    "GemaOPT",
    "DanaOPT",
    "ErnestoOPT",
    "PedroAI"
  ],
  "classrooms_names": [
    "1",
    "2",
    "3",
    "4",
    "5",
    "Postgrado"
  ],
  "groups_names": [
    "C111","C112","C113","C114","C115","C311","C312"
  ],
  "dict_group_subject_time": {
    "C111": {
      "Programacion": 1,
      "ProgramacionCp": 2,
      "Algebra": 1,
      "AlgebraCP": 2,
      "Analisis": 1,
      "AnalisisCp": 2,
      "Logica": 1,
      "LogicaCp": 1

    },
     "C112": {
      "Programacion": 1,
      "ProgramacionCp": 2,
      "Algebra": 1,
      "AlgebraCP": 2,
      "Analisis": 1,
      "AnalisisCp": 2,
      "Logica": 1,
      "LogicaCp": 1

    },
     "C113": {
      "Programacion": 1,
      "ProgramacionCp": 2,
      "Algebra": 1,
      "AlgebraCP": 2,
      "Analisis": 1,
      "AnalisisCp": 2,
      "Logica": 1,
      "LogicaCp": 1

    },
     "C114": {
      "Programacion": 1,
      "ProgramacionCp": 2,
      "Algebra": 1,
      "AlgebraCP": 2,
      "Analisis": 1,
      "AnalisisCp": 2,
      "Logica": 1,
      "LogicaCp": 1

    },
     "C115": {
      "Programacion": 1,
      "ProgramacionCp": 2,
      "Algebra": 1,
      "AlgebraCP": 2,
      "Analisis": 1,
      "AnalisisCp": 2,
      "Logica": 1,
      "LogicaCp": 1

    },
    "C311": {

      "CompilacionCon": 1,
      "CompilacionCp": 2,
      "RedesCon": 1,
      "RedesCp": 2,
      "OptimizacionCon": 1,
      "OptimizacionCp": 2,
      "AICon": 1,
      "AICp": 2
    },
    "C312": {

      "CompilacionCon": 1,
      "CompilacionCp": 2,
      "RedesCon": 1,
      "RedesCp": 2,
      "OptimizacionCon": 1,
      "OptimizacionCp": 2,
      "AICon": 1,
      "AICp": 2
    }
  },
  "shifts": [
    1,
    2,
    3
  ],
  "days": [
    1,
    2,
    3,
    4,
    5
  ],
  "dict_teachers_to_subjects": {
    "Piad": [
      "Programacion",
      "AICon"
    ],
    "Idania": [
      "Analisis"
    ],
    "Celia": [
      "Algebra"
    ],
    "Yudivian": [
      "Logica"
    ],
    "DanielL": [
      "LogicaCp"
    ],
    "OmarLogica": [
      "LogicaCp"
    ],
    "CarmentL": [
      "LogicaCp"
    ],
    "ErnestoAnalisis": [
      "AnalisisCp"
    ],
    "CristinaA": [
      "AnalisisCp"
    ],
    "MercedesA": [
      "AnalisisCp"
    ],
    "DalianisAlgebra": [
      "AlgebraCP"
    ],
    "PepeAL": [
      "AlgebraCP"
    ],
    "CayetanaAL": [
      "AlgebraCP"
    ],
    "PacoP": [
      "ProgramacionCp"
    ],
    "HectorP": [
      "ProgramacionCp"
    ],
    "CarlaP": [
      "ProgramacionCp"
    ],
    "JuanPabloCom": [
      "Programacion",
      "CompilacionCon"
    ],
    "GustavoCom": [
      "CompilacionCp"
    ],
    "LiaCom": [
      "CompilacionCp"
    ],
    "DalmauRedesAI": [
      "AICp",
      "RedesCon"
    ],
    "AntonioRedes": [
      "RedesCp"
    ],
    "GemaOPT": [
      "OptimizacionCon"
    ],
    "DanaOPT": [
      "OptimizacionCp"
    ],
    "ErnestoOPT": [
      "OptimizacionCp"
    ],
    "PedroAI": [
      "AICp"
    ]
  }
}
````

Se puede visualizar el schema con el get en el:
````
http://127.0.0.1:7000/solver/schema
````

para obtener un json la respuesta hacer get al
````
http://127.0.0.1:7000/get_json
````
se muestra un ejemplo:
````json
[
    {
        "calendar": {
            "(1, 1)": {
                "classroom": "1",
                "day": 1,
                "shift": 1,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            },
            "(1, 3)": {
                "classroom": "Postgrado",
                "day": 1,
                "shift": 3,
                "subject": "AlgebraCP",
                "teacher": "PepeAL"
            },
            "(2, 2)": {
                "classroom": "Postgrado",
                "day": 2,
                "shift": 2,
                "subject": "LogicaCp",
                "teacher": "CarmentL"
            },
            "(2, 3)": {
                "classroom": "2",
                "day": 2,
                "shift": 3,
                "subject": "AnalisisCp",
                "teacher": "MercedesA"
            },
            "(3, 1)": {
                "classroom": "2",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 2)": {
                "classroom": "2",
                "day": 3,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "CarlaP"
            },
            "(3, 3)": {
                "classroom": "4",
                "day": 3,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            },
            "(4, 2)": {
                "classroom": "Postgrado",
                "day": 4,
                "shift": 2,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(5, 1)": {
                "classroom": "5",
                "day": 5,
                "shift": 1,
                "subject": "Analisis",
                "teacher": "Idania"
            },
            "(5, 2)": {
                "classroom": "5",
                "day": 5,
                "shift": 2,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(5, 3)": {
                "classroom": "5",
                "day": 5,
                "shift": 3,
                "subject": "AnalisisCp",
                "teacher": "MercedesA"
            }
        },
        "name": "C111"
    },
    {
        "calendar": {
            "(1, 1)": {
                "classroom": "5",
                "day": 1,
                "shift": 1,
                "subject": "AnalisisCp",
                "teacher": "ErnestoAnalisis"
            },
            "(1, 2)": {
                "classroom": "2",
                "day": 1,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "CarlaP"
            },
            "(2, 1)": {
                "classroom": "1",
                "day": 2,
                "shift": 1,
                "subject": "LogicaCp",
                "teacher": "DanielL"
            },
            "(2, 2)": {
                "classroom": "2",
                "day": 2,
                "shift": 2,
                "subject": "Analisis",
                "teacher": "Idania"
            },
            "(2, 3)": {
                "classroom": "1",
                "day": 2,
                "shift": 3,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(3, 1)": {
                "classroom": "2",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 2)": {
                "classroom": "1",
                "day": 3,
                "shift": 2,
                "subject": "AnalisisCp",
                "teacher": "CristinaA"
            },
            "(3, 3)": {
                "classroom": "4",
                "day": 3,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            },
            "(4, 2)": {
                "classroom": "2",

                "day": 4,
                "shift": 2,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(5, 2)": {
                "classroom": "Postgrado",
                "day": 5,
                "shift": 2,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(5, 3)": {
                "classroom": "3",
                "day": 5,
                "shift": 3,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            }
        },
        "name": "C112"
    },
    {
        "calendar": {
            "(1, 1)": {
                "classroom": "5",
                "day": 1,
                "shift": 1,
                "subject": "AnalisisCp",
                "teacher": "ErnestoAnalisis"
            },
            "(1, 2)": {
                "classroom": "1",
                "day": 1,
                "shift": 2,
                "subject": "LogicaCp",
                "teacher": "CarmentL"
            },
            "(1, 3)": {
                "classroom": "5",
                "day": 1,
                "shift": 3,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(2, 1)": {
                "classroom": "5",
                "day": 2,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 1)": {
                "classroom": "1",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "PepeAL"
            },
            "(3, 2)": {
                "classroom": "2",
                "day": 3,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "CarlaP"
            },
            "(3, 3)": {
                "classroom": "4",
                "day": 3,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            },
            "(4, 2)": {
                "classroom": "3",
                "day": 4,
                "shift": 2,
                "subject": "Analisis",
                "teacher": "Idania"
            },
            "(5, 1)": {
                "classroom": "3",
                "day": 5,
                "shift": 1,
                "subject": "AnalisisCp",
                "teacher": "ErnestoAnalisis"
            },
            "(5, 2)": {
                "classroom": "5",
                "day": 5,
                "shift": 2,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(5, 3)": {
                "classroom": "3",
                "day": 5,
                "shift": 3,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            }
        },
        "name": "C114"
    },
    {
        "calendar": {
            "(1, 1)": {
                "classroom": "5",
                "day": 1,
                "shift": 1,
                "subject": "AnalisisCp",
                "teacher": "ErnestoAnalisis"
            },
            "(1, 3)": {
                "classroom": "1",
                "day": 1,
                "shift": 3,
                "subject": "LogicaCp",
                "teacher": "OmarLogica"
            },
            "(2, 2)": {
                "classroom": "1",
                "day": 2,
                "shift": 2,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 1)": {
                "classroom": "2",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 2)": {
                "classroom": "1",
                "day": 3,
                "shift": 2,
                "subject": "AnalisisCp",
                "teacher": "MercedesA"
            },
            "(3, 3)": {
                "classroom": "Postgrado",

                "day": 3,
                "shift": 3,
                "subject": "ProgramacionCp",
                "teacher": "PacoP"
            },
            "(4, 1)": {
                "classroom": "5",
                "day": 4,
                "shift": 1,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(4, 2)": {
                "classroom": "Postgrado",
                "day": 4,
                "shift": 2,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(4, 3)": {
                "classroom": "4",
                "day": 4,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            },
            "(5, 2)": {
                "classroom": "2",
                "day": 5,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            },
            "(5, 3)": {
                "classroom": "4",
                "day": 5,
                "shift": 3,
                "subject": "Analisis",
                "teacher": "Idania"
            }
        },
        "name": "C115"
    },
    {
        "calendar": {
            "(1, 3)": {
                "classroom": "1",
                "day": 1,
                "shift": 3,
                "subject": "LogicaCp",
                "teacher": "OmarLogica"
            },
            "(2, 1)": {
                "classroom": "2",
                "day": 2,
                "shift": 1,
                "subject": "ProgramacionCp",
                "teacher": "PacoP"
            },
            "(2, 2)": {
                "classroom": "2",
                "day": 2,
                "shift": 2,
                "subject": "Analisis",
                "teacher": "Idania"
            },
            "(2, 3)": {
                "classroom": "Postgrado",
                "day": 2,
                "shift": 3,
                "subject": "AlgebraCP",
                "teacher": "PepeAL"
            },
            "(3, 1)": {
                "classroom": "2",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "DalianisAlgebra"
            },
            "(3, 2)": {
                "classroom": "1",
                "day": 3,
                "shift": 2,
                "subject": "AnalisisCp",
                "teacher": "CristinaA"
            },
            "(3, 3)": {
                "classroom": "4",
                "day": 3,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            },
            "(4, 1)": {
                "classroom": "1",
                "day": 4,
                "shift": 1,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            },
            "(4, 2)": {
                "classroom": "Postgrado",
                "day": 4,
                "shift": 2,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(5, 2)": {
                "classroom": "5",
                "day": 5,
                "shift": 2,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(5, 3)": {
                "classroom": "5",
                "day": 5,
                "shift": 3,
                "subject": "AnalisisCp",
                "teacher": "CristinaA"
            }
        },
        "name": "C116"
    },
    {
        "calendar": {
            "(1, 1)": {
                "classroom": "5",
                "day": 1,
                "shift": 1,
                "subject": "AnalisisCp",
                "teacher": "ErnestoAnalisis"
            },
            "(1, 3)": {
                "classroom": "1",
                "day": 1,
                "shift": 3,
                "subject": "LogicaCp",
                "teacher": "CarmentL"
            },
            "(2, 1)": {
                "classroom": "4",
                "day": 2,

                "shift": 1,
                "subject": "Analisis",
                "teacher": "Idania"
            },
            "(2, 2)": {
                "classroom": "5",
                "day": 2,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "PacoP"
            },
            "(2, 3)": {
                "classroom": "1",
                "day": 2,
                "shift": 3,
                "subject": "Logica",
                "teacher": "Yudivian"
            },
            "(3, 1)": {
                "classroom": "1",
                "day": 3,
                "shift": 1,
                "subject": "AlgebraCP",
                "teacher": "PepeAL"
            },
            "(3, 2)": {
                "classroom": "2",
                "day": 3,
                "shift": 2,
                "subject": "ProgramacionCp",
                "teacher": "HectorP"
            },
            "(3, 3)": {
                "classroom": "5",
                "day": 3,
                "shift": 3,
                "subject": "AlgebraCP",
                "teacher": "CayetanaAL"
            },
            "(4, 1)": {
                "classroom": "5",
                "day": 4,
                "shift": 1,
                "subject": "Algebra",
                "teacher": "Celia"
            },
            "(4, 3)": {
                "classroom": "1",
                "day": 4,
                "shift": 3,
                "subject": "AnalisisCp",
                "teacher": "MercedesA"
            },
            "(5, 3)": {
                "classroom": "Postgrado",
                "day": 5,
                "shift": 3,
                "subject": "Programacion",
                "teacher": "Piad"
            }
        },
        "name": "C113"
    }
]

````

para obtener un excel
hacer get en
```

http://127.0.0.1:7000/download_excel
```

lo anterior solo resuelve el problema con
restricciones basicas
como puede ser que en un aula solo pueda
darse una asignatura al mismo tiempo en un turno
o que para un grupo se tiene que satisfacer la cant
de horas clases semanales de la asignatura
que un profesor no este dando dos asignaturas al mismo tiempo
ni en dos aulas distintas asi como un grupo no puede en un turno estar en dos aulas distintas

Se propone dos formas las restricciones fuertes que
obligatoriamente deben de cumplirse
que despues de creado el solver
con el  post a
````
http://127.0.0.1:7000/solver
````

se debe hacer post a
TODO:Explicar aca que las opcionales llevan un count_to_be_equals
y lo de la combinatoria iwrnviaprunpo

````
http://127.0.0.1:7000/solver/add_hard_optional_constraints
````

````json
{
    "subjects_name": [
        "Programacion"
    ],
    "teachers_name": [
        "Piad"
    ],
    "classrooms_name": [
       "1"
    ],
    "groups_name": [
        "C111"
    ],
    "shifts_int": [
        1
    ],
    "days_int": [
        1
    ],
    "count_to_be_equals":1

}
````

aca es para que se de progrmación
con piad en el aula 1 el dia 1 en el turno 1
obligado



TODO:Explicar que se relaja en el
de true que osea lo que se ponga ahi
obliga a que se cumpla
en esta url en un post
````
http://127.0.0.1:7000/solver/TrueHardConstraints
````

con un json asi
````json
{
  "teachers_name": ["JuanPabloCom"
    ],
  "subjects_name": ["CompilacionCon",
    "CompilacionCp",
    "RedesCon",
    "RedesCp",
    "OptimizacionCon",
    "OptimizacionCp",
    "AICon",
    "AICp"],
  "classrooms_name": [ "1",
    "2",
    "3",
    "4",
    "5",
    "Postgrado"],
  "groups_name": ["C311"],
  "shifts_int": [1, 2, 3],
  "days_int": [5]


}
````

aca es que juan pablo debe dar un turno
de compilacion al C311 en cualquier aula
a cualquier turno del dia 5



analgo el json para que en nunca suceda algo
en la url:

````
http://127.0.0.1:7000/solver/FalseHardConstraints
````

explicar despues lo de las softconstrainst

es que se trata de por todos los medios de que sucesa
pero que si no se puede sigue habiendo horario

para que se trate de hacer cumplir se debe introducir
con un post en este url
````
http://127.0.0.1:7000/solver/MaximizeSoftConstraints
````

este es el json a llenar

````json
{
  "teachers_name": ["JuanPabloCom",
    "GustavoCom",
    "LiaCom",
    "DalmauRedesAI",
    "AntonioRedes",
    "GemaOPT",
    "DanaOPT",
    "ErnestoOPT",
    "PedroAI"],
  "subjects_name": ["CompilacionCon"
    ],
  "classrooms_name": [ "1",

    "3"
    ],
  "groups_name": ["C311"],
  "shifts_int": [ 2 ],
  "days_int": [1],
  "alpha_value":50

}
````

analogo arriba
el alpha value es que tanto quieres que
se le de peso o prioridad siempre tiene que ser positivo

para que trate que no se cumpla
con la url :

````
http://127.0.0.1:7000/solver/MinimizeSoftConstraints
````

igual el alpha_value tiene que ser positivo mayor que 0











OJOOOO:
en la url despues de hacer inicializar con el post del solver
hacer get aca y devuelve todo en una tabla
````
http://127.0.0.1:7000/dataframe
````
