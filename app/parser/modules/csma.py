from app.parser.helpers.format_helper import format_helper

class CSMAParser:
  def __init__(self):
    pass



  def parse(self, data):
    out = []

    containers = data['topology']['node_containers']

    for c in containers:
      settings = data['topology']['container_settings'][c]
      if settings['type'] != 'point_to_point':
        continue
      
      cont_name = f'{c}_csma_helper'
      out.append(f'{cont_name} = CsmaHelper()')

      # csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
      # csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))
      
      if "data_rate" in settings:
        val = settings['data_rate']['value']
        fmt = settings['data_rate']['format']
        together = format_helper.parse_time(val, fmt)
        out.append(f'{cont_name}.SetChannelAttribute("DataRate", "{together}")')

      if "delay" in settings:
        val = settings['delay']['value']
        fmt = settings['delay']['format']
        together = format_helper.parse_time(val, fmt)
        out.append(f'{cont_name}.SetChannelAttribute("Delay", "{together}")')
      return out

      





csma_parser = CSMAParser()