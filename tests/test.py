import sys, os, time
from subprocess import Popen, PIPE

sys.path.append(os.path.dirname(os.path.abspath(f'{__file__}/..')))
from app.parser.parser import parser

class Test:
  i = 0
  def __init__(self, file, name):
    self.name = name
    self.waf = os.getenv('NS3_WAF_PATH')
    self.file = file

  def parse(self):
    self.code = parser.parse(self.file)
    # print('[+] Scenario successfully parsed.')
  
  def _check_ran(self):
    if self.code == None:
      print('[!] Scenario not parsed yet.')
      return False
    return True

  def print(self):
    if self._check_ran() == False:
      return
    for i, x in enumerate(self.code.split('\n')):
      print(f'{x}')

  def run(self, quick):
    if self._check_ran() == False:
      return

    with open('__scenario.py', 'w') as f:
      f.write(self.code)
    
    process = Popen([self.waf+'/waf', '--pyrun', os.path.abspath('__scenario.py')], cwd=self.waf, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    os.remove('__scenario.py')
    
    if quick == False:
      print('=============================================================')
      print(out.decode(), err.decode())
      print('=============================================================')
  
    error = False
    if 'finished successfully' not in out.decode():
      error = True
    if 'SIG' in err.decode():
      error = True
    # TODO nejaky test aj na beh simulacie.. zatial len SIG
    Test.i += 1
    return error

  def all(self, quick=True):
    # print(' --- Running testfile: {self.file} ---')
    self.parse()
    if quick == False:
      self.print()
    err = self.run(quick)
    if err:
      print(f'[𐄂] Test n.{Test.i} - {self.name} failed.')
    else:
      print(f'[✔] Test n.{Test.i} - {self.name} passed.' )
    return err