import os
from subprocess import Popen, PIPE
from app.managers.filemanager import filemanager
from app.managers.osmanager import l
import glob

class Ns3manager:
  def __init__(self):
    self.my_path = os.path.abspath('.')
    if os.getenv('NS3_PATH') is None:
      raise Exception('NS3_PATH environment variable not set.')
    else:
      self.ns3_path = os.getenv('NS3_PATH')

    if os.getenv('NS3_SCENARIO_PATH') is None:
      raise Exception('NS3_SCENARIO_PATH environment variable not set')
    else:
      self.ns3_scenario = os.getenv('NS3_SCENARIO_PATH')

    if os.getenv('SUMO_TRACE_EXPORTER') is None:
      raise Exception('SUMO_TRACE_EXPORTER environment variable not set')
    else:
      self.sumo_trace = os.getenv('SUMO_TRACE_EXPORTER')
    
  def generate_ns2_mobility(self, name):
    process = Popen([
      'python',
      f'{self.sumo_trace}',
      '--fcd-input',
      l(f'{self.my_path}/scenarios/{name}/sumoTrace.xml'),
      '--ns2mobility-output',
      l(f'{self.my_path}/scenarios/{name}/mobility.tcl')
    ], 
      stdout=PIPE,
      stderr=PIPE 
    )

    out, err = process.communicate()
    
    if process.returncode == 0:
      return True
    return False
  
  def simulate(self, name):
    process = Popen([
      l(f'{self.ns3_path}/ns3'),
      'run',
      l(f'" {self.ns3_scenario} --config={self.my_path}/scenarios/{name}/config.json --mobility={self.my_path}/scenarios/{name}/mobility.tcl --traceloc={self.my_path}/scenarios/{name}"')
    ],
      cwd=self.ns3_path,
      stdout=PIPE,
      stderr=PIPE
    )
    out, err = process.communicate()
    return err.decode().split('\n')
  
  def validate(self, name):
    process = Popen([
      l(f'{self.ns3_path}/ns3'),
      'run',
      l(f'" {self.ns3_scenario} --config={self.my_path}/scenarios/{name}/config.json --mobility={self.my_path}/scenarios/{name}/mobility.tcl --traceloc={self.my_path}/scenarios/{name} --validate=1"')
    ],
      cwd=self.ns3_path,
      stdout=PIPE,
      stderr=PIPE
    )
    out, err = process.communicate()

    if process.returncode == 0:
      return None
    return err.decode()

ns3manager = Ns3manager()
