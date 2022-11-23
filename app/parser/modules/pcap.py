from app.parser.modules.base import BaseParser

class PcapParser(BaseParser):
  def __init__(self):
    pass
  
  def parse(self, data):
    out = []
    containers = data['topology']['node_containers']

    for c in containers:
      ## get type
      type = data['topology']['container_settings'][c]['type']
      helper_name = None
      if type == 'point_to_point':
        helper_name = f'{c}_p2p_helper'
      elif type == 'csma':
        helper_name = f'{c}_csma_helper'
      
      # TODO nejaky handler tu raz bude zejo
      if helper_name is None:
        PADNI()

      node = data['topology']['container_settings'][c]
      
      if node['log_pcap'] == True:
        out.append(f'{helper_name}.EnablePcapAll({c})')
    
    return out

pcap_parser = PcapParser()
