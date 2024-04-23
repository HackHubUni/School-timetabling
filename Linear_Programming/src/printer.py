import os
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from pandas import DataFrame
from flask import send_file, jsonify


def to_data_frame(data):
  # Crear un DataFrame a partir de la lista
  df = pd.DataFrame(data)
  return df
  # Mostrar el DataFrame
  # print(df)


def to_excel(df: DataFrame):
  # Asumiendo que 'Profesor', 'Asignatura' y 'Aula' son otras columnas en tu DataFrame que quieres incluir
  df['Info'] = 'Profesor:' + df['Teacher'] + "\n" "Asignatura:" + df['Subject'] + "\n" + "Aula:" + df['Classroom']
  # df['Teacher'] + ', ' + df['Subject'] + ', ' + df['Classroom']

  with pd.ExcelWriter('../API/output.xlsx') as writer:
    for group in df['Group'].unique():
      # Filtrar el DataFrame por grupo
      df_group = df[df['Group'] == group]

      # Reorganizar el DataFrame para que los días sean las columnas y los turnos las filas
      # Ahora, cada celda contendrá la información de 'Info'
      df_pivot = df_group.pivot(index='Shift', columns='Day', values='Info')

      # Escribir el DataFrame reorganizado en una hoja de Excel
      df_pivot.to_excel(writer, sheet_name=group)

__folder_path='../temp'



#def send_excel(df: DataFrame):
#  print("Entre")
#  df['Info'] = 'Profesor:' + df['Teacher'] + "\n" "Asignatura:" + df['Subject'] + "\n" + "Aula:" + df['Classroom']
#  os.makedirs(__folder_path, exist_ok=True)
#  # Get the directory of the current file (printer.py)
#  #dir_path = os.path.dirname(os.path.realpath(__file__))
#  dir_path=__folder_path
#  # Construct the file path
#  #file_path = os.path.join(dir_path, 'output.xlsx')
#  file_path=f'{__folder_path}/output.xlsx'
#  with pd.ExcelWriter(file_path) as writer:
#    print("ENtro en el with")
#    for group in df['Group'].unique():
#      df_group = df[df['Group'] == group]
#      df_pivot = df_group.pivot(index='Shift', columns='Day', values='Info')
#      df_pivot.to_excel(writer, sheet_name=group)
#
#  if os.path.exists(file_path) and os.access(file_path, os.R_OK):
#    # El archivo existe y es legible
#    print(48484)
#
#
#   return send_file(file_path, as_attachment=True)


import os
import pandas as pd
import tempfile
from flask import send_file, jsonify


def send_excel(df: pd.DataFrame):
  print("Entre")
  df['Info'] = 'Profesor:' + df['Teacher'] + "\n" + "Asignatura:" + df['Subject'] + "\n" + "Aula:" + df['Classroom']

  # Crear un directorio temporal
  temp_dir = tempfile.mkdtemp()

  # Construir la ruta del archivo Excel dentro del directorio temporal
  file_name = 'output.xlsx'
  file_path = os.path.join(temp_dir, file_name)

  with pd.ExcelWriter(file_path) as writer:
    print("ENtro en el with")
    for group in df['Group'].unique():
      df_group = df[df['Group'] == group]
      df_pivot = df_group.pivot(index='Shift', columns='Day', values='Info')
      df_pivot.to_excel(writer, sheet_name=group)

  # Verificar si el archivo existe y es legible
  if os.path.exists(file_path) and os.access(file_path, os.R_OK):
    # El archivo existe y es legible
    print(48484)
    return send_file(file_path, as_attachment=True)
  else:
    # El archivo no existe o no es legible
    if not os.path.exists(file_path):
      return jsonify({"error": "File not found"}), 404
    else:
      return jsonify({"error": "File is not readable"}), 403









