class LogParser:
  def __init__(self):
    pass
  
  def parse(self, data):
    out = []
    containers = data['topology']['node_containers']

    for c in containers:
      helper_name = c + '_helper'
      node = data['topology']['container_settings'][c]
      
      if node['log_pcap'] == True:
        out.append(f'{helper_name}.enablePcapAll({c})')
    
    return out

log_parser = LogParser()
