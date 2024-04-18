import pandas as pd
from pandas import DataFrame


def to_excel(df:DataFrame):
  # Asumiendo que 'Profesor', 'Asignatura' y 'Aula' son otras columnas en tu DataFrame que quieres incluir
  df['Info'] ='Profesor:'+ df['Teacher'] +"\n" "Asignatura:"+ df['Subject'] +"\n"+ "Aula:"+df['Classroom']
   # df['Teacher'] + ', ' + df['Subject'] + ', ' + df['Classroom']

  with pd.ExcelWriter('output.xlsx') as writer:
    for group in df['Group'].unique():
      # Filtrar el DataFrame por grupo
      df_group = df[df['Group'] == group]

      # Reorganizar el DataFrame para que los días sean las columnas y los turnos las filas
      # Ahora, cada celda contendrá la información de 'Info'
      df_pivot = df_group.pivot(index='Shift', columns='Day', values='Info')

      # Escribir el DataFrame reorganizado en una hoja de Excel
      df_pivot.to_excel(writer, sheet_name=group)
