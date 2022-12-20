from app.parser.helpers.concat_helper import add

class BaseModel:
  def __init__(self):
    self.essential = []
    self.imports = []
    self.parser = None
  
  def check_essential(self):
    for x in self.essential:
      if getattr(self, x) is None:
        return False
    return True

  def get_missing(self):
    missing = []
    for x in self.essential:
      val = getattr(self, x)
      if val is None:
        missing.append(x)
    return missing    
  
  def add_imports(self, arr):
    for imp in self.imports:
      if self.parser.daddy.check_import(imp) == False:
        add(arr, imp)

  def add_imports(self, arr):
    for imp in self.imports:
      if self.parser.daddy.check_import(imp) == False:
        add(arr, imp)

  def dumppy(self) -> str:
    return ""

  def dumpcc(self) -> str:
    return ""


