from app.parser.helpers.format_helper import format_helper

class P2PParser:
  def __init__(self):
    pass

  def parse(self, data):
    out = []

    containers = data['topology']['node_containers']

    for c in containers:
      if data['topology']['container_settings'][c]['type'] == 'point_to_point':
        out.append(f'# Point-To-Point')
        break
    
    for c in containers:
      settings = data['topology']['container_settings'][c]
      if settings['type'] != 'point_to_point':
        continue
      
      cont_name = f'{c}_p2p_helper'
      out.append(f'{cont_name} = PointToPointHelper()')

      if "data_rate" in settings:
        val = settings['data_rate']['value']
        fmt = settings['data_rate']['format']
        together = format_helper.parse_time(val, fmt)
        out.append(f'{cont_name}.SetDeviceAttribute("DataRate", "{together}")')

      if "delay" in settings:
        val = settings['delay']['value']
        fmt = settings['delay']['format']
        together = format_helper.parse_time(val, fmt)
        out.append(f'{cont_name}.SetChannelAttribute("Delay", "{together}")')

      out.append(f'{c}_devices = {cont_name}.Install({c}_container)')
    return out

p2p_parser = P2PParser()