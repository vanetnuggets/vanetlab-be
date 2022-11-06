import os
from subprocess import Popen, PIPE

class Ns3manager:
  def __init__(self):
    self.filename = ''
    self.status = 'waiting'
    
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
  
  def run(self, file):
    self._check_status('loaded')

    process = Popen([self.waf_path, '--pyrun', self.filename], stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()

    print(out, err)
    return None
  
  def get_pcap(self):
    self._check_status('done')
    pass
  
  def get_output(self):
    self._check_status('done')
    pass
  
  def status(self):
    return self.status