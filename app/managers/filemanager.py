from os import mkdir, path
from shutil import rmtree
import glob, os
import uuid
import json

from app.managers.osmanager import l 

class FileManager:
  def __init__(self):
    self.my_path = os.path.abspath('.')

  def path(self, name):
    return l(f'{self.my_path}/scenarios/{name}')

  def create_scenario(self, name):
    path = self.path(name)
    try:
      os.makedirs(path)
    except:
      return False
    return True
  
  def save_sumo(self, name, sumo_file):
    path = l(f'{self.path(name)}/sumoTrace.xml')
    sumo_file.save(path)
    return True
  
  def save_conf(self, name, conf):
    self.create_scenario(name)
    path = l(f'{self.path(name)}/config.json')
    with open(path, 'w') as f:
      json.dump(conf, f, indent=2) 
    return True
  
  def save_tcl(self, name, lines):
    path = l(f'{self.path(name)}/mobility.tcl')
    with open(path, 'w') as f:
      f.writelines(lines)
    return True

  def get_ns2tcl(self, name):
    return l(f'{self.path(name)}/mobility.tcl')
  
  def get_netanim_trace(self, name):
    path = l(f'{self.path(name)}/trace.xml')
    return path
  
  def get_all_scenarios(self):
    scenarios = []
    for f in glob.glob(l(f'{self.my_path}/scenarios/*')):
      for ff in glob.glob(f'{f}/*'):
        if ff.split('/')[-1] == 'config.json':
          scenarios.append(f.split('/')[-1])
    return scenarios
  
  def exists_scenario(self, name):
    for f in glob.glob(l(f'{self.my_path}/scenarios/*')):
      scenario = f.split('/')[-1]
      if scenario == name:
        return True
    return False
  
  def get_config(self, name):

    path = l(f'{self.path(name)}/config.json')
    data = ""
    with open(path, 'r') as f:
      data = f.read()
    config = json.loads(data)
    return config
  
  def save_stdout(self, name, data):
    path = l(f'{self.path(name)/output.txt}')
    with open(path, 'w') as f:
      f.write('\n'.join(data))
    return

filemanager = FileManager()
