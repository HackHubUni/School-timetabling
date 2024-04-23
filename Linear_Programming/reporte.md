
## Llamando a http://localhost:7000/solver/schema con el metodo GET nos devuelve la estructura de request que es la siguiente:

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

## Luego haciendo la solicitud post a http://localhost:7000/solver :

### si no se inserta ningun valor obtenemos lo siguiente:

{
    "error": {
        "classrooms_names": [
            "Not a valid list."
        ],
        "days": [
            "Not a valid list."
        ],
        "dict_group_subject_time": [
            "Not a valid mapping type."
        ],
        "dict_subjects_by_time": [
            "Not a valid mapping type."
        ],
        "dict_teachers_to_subjects": [
            "Not a valid mapping type."
        ],
        "groups_names": [
            "Not a valid list."
        ],
        "shifts": [
            "Not a valid list."
        ],
        "subjects_name_list": [
            "Not a valid list."
        ],
        "teachers_names": [
            "Not a valid list."
        ]
    }
}

### si introducimos los parametros correctamente:

#### Por ejemplo:

{
    "subjects_name_list": [
        "Programación",
        "AlgebraConf",
        "AlgebraCP"
    ],
    "dict_subjects_by_time": {
        "Programación": 2,
        "AlgebraConf": 1,
        "AlgebraCP": 2
    },
    "teachers_names": [
        "Piad",
        "Celia",
        "Juan"
    ],
    "classrooms_names": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ],
    "groups_names": [
        "C111",
        "C112"
    ],
    "dict_group_subject_time": {
        "C111": {
            "Programación": 2,
            "AlgebraConf": 1,
            "AlgebraCP": 2
        },
        "C112": {
            "Programación": 2,
            "AlgebraConf": 1,
            "AlgebraCP": 2
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
            "Programación"
        ],
        "Celia": [
            "AlgebraConf"
        ],
        "Juan": [
            "AlgebraCP"
        ]
    }
}

### Nos devuelve:

{
    "message": "Solver instance created successfully"
}


### Haciendo GET a http://localhost:7000/dataframe se obtiene:

"{\"columns\":[\"Teacher\",\"Subject\",\"Classroom\",\"Group\",\"Shift\",\"Day\"],\"index\":[0,1,2,3,4,5,6,7,8,9],\"data\":[[\"Piad\",\"Programaci\ón\",\"1\",\"C111\",3,1],[\"Piad\",\"Programaci\ón\",\"2\",\"C112\",3,2],[\"Piad\",\"Programaci\ón\",\"3\",\"C111\",2,1],[\"Piad\",\"Programaci\ón\",\"6\",\"C112\",2,5],[\"Celia\",\"AlgebraConf\",\"1\",\"C111\",1,1],[\"Celia\",\"AlgebraConf\",\"1\",\"C112\",2,1],[\"Juan\",\"AlgebraCP\",\"2\",\"C111\",3,3],[\"Juan\",\"AlgebraCP\",\"4\",\"C112\",2,2],[\"Juan\",\"AlgebraCP\",\"5\",\"C111\",2,5],[\"Juan\",\"AlgebraCP\",\"6\",\"C112\",3,1]]}"


