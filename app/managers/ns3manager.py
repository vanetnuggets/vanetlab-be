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
      'python3',
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
    
    # check whether output is empty - the trace exporter script is dogshit and does not scream
    # when it gets broken input file it just creates an empty file so we check it manually
    mob_path = l(f'{self.my_path}/scenarios/{name}/mobility.tcl')
    if os.stat(mob_path).st_size == 0:
      return False

    return True

  def get_run_path(self) -> str:
      return l(f'{self.my_path}/run')

  def simulate(self, name):   
    print(l(f'" {self.ns3_scenario} --config={self.get_run_path()}/config.json --mobility={self.get_run_path()}/mobility.tcl --traceloc={self.get_run_path()}"'))

    process = Popen([
      l(f'{self.ns3_path}/ns3'),
      'run',
      l(f'" {self.ns3_scenario} --config={self.get_run_path()}/config.json --mobility={self.get_run_path()}/mobility.tcl --traceloc={self.get_run_path()}"')
    ],
      cwd=self.get_run_path(),
      stdout=PIPE,
      stderr=PIPE
    )
    out, err = process.communicate()
    
    data2 = out.decode().split('\n')
    print('\n'.join(data2))

    data = err.decode().split('\n')
    print('\n'.join(data))

    

    filemanager.save_stdout(name, data)
    filemanager.save_simulation_output(name)

    return None
    
  def validate(self, name):
    process = Popen([
      l(f'{self.ns3_path}/ns3'),
      'run',
      l(f'" {self.ns3_scenario} --config={self.get_run_path()}/config.json --mobility={self.get_run_path()}/mobility.tcl --traceloc={self.get_run_path()} --validate=1"')
    ],
      cwd=self.ns3_path,
      stdout=PIPE,
      stderr=PIPE
    )
    out, err = process.communicate()

    if process.returncode == 0:
      return None
    return err.decode() + out.decode()

ns3manager = Ns3manager()
