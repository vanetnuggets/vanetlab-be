class BaseParser:
  def __init__(self):
    pass
  
  def comment(self, msg):
    return f'\n# {msg}'

  def comment(self, arr, msg):
    arr.append(f'\n# {msg}')
  
  def init(self, parent):
    self.daddy = parent