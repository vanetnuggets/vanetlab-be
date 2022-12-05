from app.parser.helpers.format_helper import format_helper
from app.parser.modules.nodes import node_parser
from app.model.udpcomm import UDPClient, UDPServer
from app.parser.modules.base import BaseParser

class EchoUDPParser(BaseParser):
  def __init__(self):
    super().__init__()

  def _get_timeboudns(self, timedata, key=None):
    if 'value' not in timedata or 'format' not in timedata:
      # XXX possibly throw an exception instead ?
      return None, None
    else:
      return format_helper.parse_time(timedata['value'], timedata['format'])
  
  def parse_client(self, data, orig):
    out = []
    self.comment(out, 'UDP Echo client')

    sim = orig['simulation']['client'][data]

    attrs = []
    if 'max_packets' in sim:
      attrs.append(('MaxPackets', format_helper.parse_uint(sim['max_packets'])))
    if 'interval' in sim:
      attrs.append(('Interval', format_helper.time_value(sim['interval']['value'], sim['interval']['format'])))
    if 'packet_size' in sim:
      attrs.append(('PacketSize', format_helper.parse_uint(sim['packet_size'])))

    start = self._get_timeboudns(sim['start'], 'start')
    stop  = self._get_timeboudns(sim['stop'], 'stop')

    my_server = orig['simulation']['server'][sim['server']['name']]
    server_network = my_server['network']
    server_node    = self.daddy.node_parser.node(server_network, my_server['node'])
    my_node = self.daddy.node_parser.node(sim['network'], sim['node'])

    interfaces = sim['network'] + '_interfaces'

    client = UDPClient(
      port=sim['port'] if 'port' in sim else None,
      name=sim['name'] if 'name' in sim else None,
      node=my_node,
      start=start,
      stop=stop,
      server_node=server_node,
      server_network=interfaces,
      network=f"{sim['network']}_container" if 'network' in sim else None,
      attrs=attrs
    )

    return out + client.dumppy()

  def parse_server(self, data, orig):
    out = []
    self.comment(out, 'Parsing Echo Server')
    
    sim = orig['simulation']['server'][data]

    port = sim['port']
    name = sim['name']
    start = self._get_timeboudns(sim['start'], 'start')
    stop  = self._get_timeboudns(sim['stop'], 'stop')
    node = self.daddy.node_parser.node(sim['network'], sim['node'])
    network = f"{sim['network']}_container"

    server = UDPServer(
      port=port, 
      name=name, 
      start=start, 
      stop=stop, 
      network=network, 
      node=node, 
      attrs=[]
    )
    return out + server.dumppy()
    

  def p(self, data):
    out = []
    if 'simulation' not in data:
      return []
    
    if 'server' in data['simulation']:
      for x in data['simulation']['client']:
        out += self.parse_client(x, data)
              
      for x in data['simulation']['server']:
        out += self.parse_server(x, data)
        
    
    return out

  def parse(self, data):
    out = []
    out.append('\n# Client/Server communication')
    
    # TODO - asi ich moze byt z rovnakeho typu viac, tak tam treba pridat cisielka

    for simtype in data['simulation']:
      if simtype == 'server_apps':
        out.append(f'\n# Server communication...')
        cont = data['simulation'][simtype]
        port = cont['port']
        nodes = cont['nodes']
        network = cont['network']
        out.append(f'echo_server = UdpEchoServerHelper({port})')

        if len(nodes) > 1:
          # TODO musis spravit nodecontainer dalsi ktory to nainstaluje 
          pass
        else:
          # len get a install jejda
          out.append(f'server_apps = echo_server.Install({network}_container.Get({nodes[0]}))')
        
        start = format_helper.parse_time(cont['start']['value'], cont['start']['format'])
        stop  = format_helper.parse_time(cont['stop']['value'], cont['stop']['format'])

        out.append(f'server_apps.Start({start})')
        out.append(f'server_apps.Stop({stop})')

      # TODO Tu URCITE treba pridat cisielka, lebo klientov bude vela
      elif simtype == 'client_apps':
        out.append(f'\n# Client communication...')
        cont = data['simulation'][simtype]
        port = cont['port']
        nodes = cont['nodes']
        packets = cont['max_packets']
        size = cont['packet_size']
        network = cont['network']
        server = cont['server']
        start = format_helper.parse_time(cont['start']['value'], cont['start']['format'])
        stop  = format_helper.parse_time(cont['stop']['value'], cont['stop']['format'])
        interval = format_helper.time_value(cont['interval']['value'], cont['interval']['format'])
        
        for n in nodes:
          i = node_parser.node(network, n)
          client_name = f'echo_client_{network}_{n}'
          app_name = f'echo_client_apps_{network}_{n}'

          out.append(f'{client_name} = UdpEchoClientHelper({server["network"]}_interfaces.GetAddress({server["node"]}), {port})')
          out.append(f'{client_name}.SetAttribute("MaxPackets", UintegerValue({packets}))')
          out.append(f'{client_name}.SetAttribute("Interval", {interval})')
          out.append(f'{client_name}.SetAttribute("PacketSize", UintegerValue({size}))')

          out.append(f'{app_name} = {client_name}.Install({network}_container.Get({i}))')
          out.append(f'{app_name}.Start({start})')
          out.append(f'{app_name}.Stop({stop})')
    return out


echo_udp_parser = EchoUDPParser()