
class Base:
  def __init__(self,name:str|int):
    self.name=name
class Course:
  def __init__(self,name:int):
    self.name=name

class Subject(Base):
  def __init__(self,name:str):
    super().__init__(name)


class Teacher(Base):
  def __init__(self, name: str):
    super().__init__(name)


class Turno:
  def __init__(self,dia:int,turno:int,teacher:str,subject:str,classroom:str):
    self.day=dia
    self.shift=turno
    self.teacher:str=teacher
    self.subject:str=subject
    self.classroom:str=classroom

  def to_dict(self):
    return {
        'day': self.day,
        'shift': self.shift,
        'teacher': self.teacher,
        'subject': self.subject,
        'classroom': self.classroom
    }


class Group(Base):
  def __init__(self, name: str):
    self.name:str=name
    self.calendar:dict[tuple[int,int],Turno]={}

  def add(self,dia:int,turno:int,teacher:str,subject:str,classroom:str):
    tup=(dia,turno)
    if tup in self.calendar:
      raise Exception(f"El turno{turno} el dia{dia} estaba satisfecho ")
    self.calendar[tup]=Turno(dia,turno,teacher,subject,classroom)

  def to_dict(self):
    return {
        'name': self.name,
        'calendar': {str(k): v.to_dict() for k, v in self.calendar.items()}
    }



import json



def groups_to_json(groups: dict[str,Group]):
  # Obtener solo los valores del diccionario
  group_values:list[Group] = groups.values()
  groups_dict = [group.to_dict() for group in group_values]
  #return json.dumps(groups_dict)
  return  groups_dict






