from app.parser.modules.base import BaseParser
from app.model.wifi import WifiModel
from app.parser.helpers.concat_helper import add

class WifiParser(BaseParser):
  def __init__(self):
    super().__init__()
  
  def parse(self, data):
    out = []
    curr = 0
    self.comment(out, 'Wifi L2 configuration')

    for cont in data['topology']['node_containers']:
      settings = data['topology']['container_settings'][cont]
      
      if settings['type'] == 'wifi':
        self.comment(out, f'Wifi network pair n.{curr}')
        name = settings['name']
        ssid = settings['ssid']
        network = f'{cont}_container'

        log_pcap = settings['log_pcap']
        log_ascii = settings['log_ascii']

        mobility = settings['mobility']

        wifi = WifiModel(
          parser=self,
          name=name,
          ssid=ssid,
          network=network,
          mobility=mobility,
          log_pcap=log_pcap,
          log_ascii=log_ascii
        )

        curr += 1
        out += wifi.dumppy()
        
    return out