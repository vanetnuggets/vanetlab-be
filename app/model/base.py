class BaseModel:
  def __init__(self):
    self.essential = []
  
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

  def dumppy(self) -> str:
    return ""

  def dumpcc(self) -> str:
    return ""


