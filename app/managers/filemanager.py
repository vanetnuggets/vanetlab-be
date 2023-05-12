from os import mkdir, path
from shutil import rmtree
import glob, os
import uuid
import json
import shutil
from app.config import RO_SCENARIOS
import app.managers.tcl_parser
import zipfile

from app.managers.osmanager import l 

class FileManager:
  def __init__(self):
    self.my_path = os.path.abspath('.')
    self.ns3_path = os.getenv('NS3_PATH')
  
  def get_run_path(self) -> str:
    return l(f'{self.my_path}/run')

  def path(self, name):
    return l(f'{self.my_path}/scenarios/{name}')
  
  def size(self, name, file):
    return os.path.getsize(l(f'{self.path(name)}/{file}'))

  def summary(self, name):
    print(name)
    summ = {}
    summ['mobility'] = {
      'name': 'mobility.tcl',
      'size': self.size(name, 'mobility.tcl')
    }

    summ['output'] = {
      'name': 'output.txt',
      'size': self.size(name, 'output.txt')
    }

    summ['trace'] = {
      'name': 'trace.xml',
      'size': self.size(name, 'trace.xml')
    }
    
    summ['ascii'] = {
      'name': f'{name}_ascii_traces.zip',
      'size': self.size(name, f'{name}_ascii_traces.zip')
    }

    summ['pcap'] = {
      'name': f'{name}_pcap.zip',
      'size': self.size(name, f'{name}_pcap.zip')
    }

    return summ

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
  
  def save_conf(self, name, conf, save_to=None):
    """ Saves a config to the filesystem
      @name (str) name of scenario to save to
      @conf (json) configuration to save
      @save_to (str) special variable, saves to `run` folder if specified 
    """
    # cannot overwrite default scenario
    if name in RO_SCENARIOS:
      return False

    self.create_scenario(name)
    path = l(f'{self.path(name)}/config.json')
    if save_to != None:
      # TODO generalizovat
      path = l(f'{self.get_run_path()}/config.json')
  
    with open(path, 'w') as f:
      json.dump(conf, f, indent=2) 
    return True
  
  def save_tcl(self, name, lines, save_to=None):
    path = l(f'{self.path(name)}/mobility.tcl')
    if save_to == 'run':
      path = l(f'{self.get_run_path()}/mobility.tcl')
    with open(path, 'w') as f:
      f.write('\n'.join(lines))
    return True

  def get_ns2tcl(self, name):
    return l(f'{self.path(name)}/mobility.tcl')
  
  def get_netanim_trace(self, name):
    path = l(f'{self.path(name)}/trace.xml')
    return path
  
  def get_all_scenarios(self):
    """ browses $APP/scenarios/* for all directories and returns a list of names 
    of scenarios that have `config.json` file and therefore can be loaded along with
    information whether the scenario is read-only (example scenarios) or can be modified 
    based on `RO_SCENARIOS` variable in config.
    """
    scenarios = []
    for f in glob.glob(l(f'{self.my_path}/scenarios/*')):
      for ff in glob.glob(f'{f}/*'):
        if ff.split(l('/'))[-1] == 'config.json':
          name = f.split(l('/'))[-1]
          scenarios.append({
            'name': name,
            'read-only': True if name in RO_SCENARIOS else False 
          })
    return scenarios
  
  def exists_scenario(self, name):
    for f in glob.glob(l(f'{self.my_path}/scenarios/*')):
      scenario = f.split(l('/'))[-1]
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
    path = l(f'{self.get_run_path()}/output.txt')
    with open(path, 'w') as f:
      f.write('\n'.join(data))
    return
  
  def prepare_simulation(self, name, config):
      """ moves all simulation files into 'run' directory to be run in 'simulate' method. 
      moved files are saved into permanent storage in `save_simulation_output` method
        @config (json): config json from post request body
      """

      self.save_conf("", config, save_to='run')
      app.managers.tcl_parser.tcl_parser.conf_to_tcl(name, config, save_to='run')

      return

  def save_simulation_output(self, sim_name) -> None:
    """ move all files from 'run' folder into its own simulation folder
      @sim_name (str): name of scenario to which the files are moved
    """
    run_path = self.get_run_path()
    sim_path = self.path(sim_name)
    ns3_path = self.ns3_path
    
    if ns3_path[-1] != '/':
        ns3_path += '/'

    # tuto najprv movni pcapy z ns3 config do run config ptm zipni vsetky pcap-y
    with zipfile.ZipFile(run_path + '/' + sim_name + '_pcap.zip', 'w') as zf:
      for fname in os.listdir(self.ns3_path):
        if '.pcap' in fname:
          zf.write(self.ns3_path + fname)

    # tuto zipni vsetky ascii traces 
    with zipfile.ZipFile(run_path + '/' + sim_name + '_ascii_traces.zip', 'w') as zf:
      for fname in os.listdir(run_path):
        if '_asciitrace.txt' in fname:
          zf.write(run_path + '/' + fname)
    
    # vymaz vsetky pcap-y a .txtcka
    for fname in os.listdir(self.ns3_path):
      if '_asciitrace.txt' in fname or '.pcap' in fname:
        os.remove(ns3_path + fname)

    for fname in os.listdir(run_path):
      if fname[0] == '.':
        continue

      file_path_src = os.path.join(run_path, fname)
      file_path_dst = os.path.join(sim_path, fname)

      shutil.move(file_path_src, file_path_dst)
      
      
    return

  def clean_simulation_output(self) -> None:
    """ remove all files from the 'run' folder so they won't mix with next simulation output
    should not need to be called because `save_simulation_output` moves it anyways
    """
    path = self.get_run_path()
    shutil.rmtree(path)
  
  def get_file(self, name, file):
    path = l(f'{self.path(name)}/{file}')
    return path

  def delete_scenario(self, name):
    if name in RO_SCENARIOS:
      return False
  
    if not self.exists_scenario(name):
      return False
    path = self.path(name)
    shutil.rmtree(path)
    return True

filemanager = FileManager()
