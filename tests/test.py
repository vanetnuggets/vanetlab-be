import sys, os, time
from subprocess import Popen, PIPE

print(os.path.dirname(os.path.abspath(f'{__file__}/..')))
sys.path.append(os.path.dirname(os.path.abspath(f'{__file__}/..')))
from app.parser.parser import parser

class Test:
  def __init__(self, file):
    self.waf = os.getenv('NS3_WAF_PATH')
    self.file = file

  def parse(self):
    self.code = parser.parse(self.file)
    print('[+] Scenario successfully parsed.')
  
  def _check_ran(self):
    if self.code == None:
      print('[!] Scenario not parsed yet.')
      return False
    return True

  def print(self):
    if self._check_ran() == False:
      return
    for i, x in enumerate(self.code.split('\n')):
      print(f'{i}: {x}')

  def run(self):
    if self._check_ran() == False:
      return

    with open('__scenario.py', 'w') as f:
      f.write(self.code)
    
    process = Popen([self.waf+'/waf', '--pyrun', os.path.abspath('__scenario.py')], cwd=self.waf, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()

    os.remove('__scenario.py')
    print('=============================================================')
    print(out.decode(), err.decode())
    print('=============================================================')
  
  def all(self):
    print(' --- Running testfile: {self.file} ---')
    self.parse()
    self.print()
    self.run()