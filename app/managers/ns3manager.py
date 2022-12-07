import os
from subprocess import Popen, PIPE
from app.managers.filemanager import filemanager
import glob


class Ns3manager:
  def __init__(self):
    self.my_path = os.path.abspath('.')
    if os.getenv('NS3_WAF_PATH') is None:
      raise Exception('NS3_WAF_PATH environment variable not set.')
    else:
      self.waf_path = os.getenv('NS3_WAF_PATH')

  def run(self, file, uuid):
    # TODO niekedy v buducnosti... toto nie je skalovatelne, treba spravit nejaku priority queue, 
    #      ktora bude sem postupne hadzat scenare..
    # ?? jake formatovanie povedz
    print('!!! RUNNING', file)
    process = Popen([
      self.waf_path+'/waf',
       '--pyrun', 
       os.path.abspath(file)
      ], 
       cwd=self.waf_path, 
       stdout=PIPE, 
       stderr=PIPE
      )
    out, err = process.communicate()

    # Asi return value by bolo lepsie kontrolovat ale nwm jak to vytiahnut takto z hlavy
    if b'successfully' in out:
      # Simulation output is written into stderr for some reason
      output = err.decode().strip().split('\n')

      # move logs
      filemanager.move_output(self.waf_path, uuid)

      return output, None
    else:
      return [], err

ns3manager = Ns3manager()