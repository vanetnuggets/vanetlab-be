import os

class OSManager:
  os = "unix"

  def __init__(self):
    if os.name == 'nt':
      self.os = 'nt'
    else:
      self.os = 'unix'
  
  def windows(self):
    return self.os == 'nt'
  
  def linux(self):
    return self.os == 'unix'
  
osmanager = OSManager()

def l(s):
  if osmanager.windows():
    return s.replace('/', '\\')
  return s