
class Base:
  def __init__(self,name:str|int):
    self.name=name
class Course:
  def __init__(self,name:int):
    self.name=name

class Group(Base):
  def __init__(self,name:str):
    super().__init__(name)


class Teacher(Base):
  def __init__(self, name: str):
    super().__init__(name)


class Subject(Base):
  def __init__(self, name: str,lis_groups:list[Group],list_teacher:list[Teacher]):
    super().__init__(name)
    self.groups=lis_groups
    self.teachers=list_teacher

