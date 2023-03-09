from os import mkdir, path
from shutil import rmtree
import glob, os
import uuid
import json

class FileManager:
  def __init__(self):
    self.my_path = os.path.abspath('.')

  def path(self, name):
    return f'{self.my_path}/scenarios/{name}'

  def create_scenario(self, name):
    path = self.path(name)
    try:
      os.makedirs(path)
    except:
      return False
    return True
  
  def save_sumo(self, name, sumo_file):
    path = f'{self.path(name)}/sumoTrace.xml'
    sumo_file.save(path)
    return True
  
  def save_conf(self, name, conf):
    path = f'{self.path(name)}/config.json'
    with open(path, 'w') as f:
      json.dump(conf, f, indent=2) 
    return True

  def get_ns2tcl(self, name):
    return f'{self.path(name)}/mobility.tcl'
  
  def get_netanim_trace(self, name):
    path = f'{self.path(name)}/trace.xml'
    return path
  
  def get_all_scenarios(self):
    scenarios = []
    for f in glob.glob(f'{self.my_path}/scenarios/*'):
      for ff in glob.glob(f'{f}/*'):
        if ff.split('/')[-1] == 'config.json':
          scenarios.append(f.split('/')[-1])
    return scenarios
  
  def get_config(self, name):

    path = f'{self.path(name)}/config.json'
    data = ""
    with open(path, 'r') as f:
      data = f.read()
    config = json.loads(data)
    return config

filemanager = FileManager()
