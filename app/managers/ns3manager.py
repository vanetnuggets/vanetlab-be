import os
from subprocess import Popen, PIPE
import glob

class Ns3manager:
  def __init__(self):
    self.filename = ''
    self.status = 'waiting'
    self.my_path = os.path.abspath('.')
    
    if os.getenv('NS3_WAF_PATH') is None:
      self.status = 'error'
      raise Exception('NS3_WAF_PATH environment variable not set.')
    else:
      self.waf_path = os.getenv('NS3_WAF_PATH')

  def _check_status(self, needed=None):
    if self.status == 'error':
      return None, 'waf path not set'
    if needed is not None and self.status != needed:
      return None, 'wrong state'

  def load(self, file):
    self._check_status()
    
    self.filename = file
    self.status = 'loaded'
  
  def run(self):
    self._check_status('loaded')

    process = Popen([self.waf_path+'/waf', '--pyrun', os.path.abspath(self.filename)], cwd=self.waf_path, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()


    if b'successfully' in out:
      # move logs
      for f in glob.glob(f'{self.waf_path}/*.pcap'):
        filename = f.split('/')[-1].strip()
        os.rename(f, f'{self.my_path}/scenarios/tmp/{filename}')

      return err, None
    else:
      return '', 'out'
  
  def get_pcap(self):
    self._check_status('done')
    pass
  
  def get_output(self):
    self._check_status('done')
    pass
  
  def status(self):
    return self.status

ns3manager = Ns3manager()