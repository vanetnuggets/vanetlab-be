from app.parser.helpers.format_helper import format_helper
from app.parser.modules.nodes import node_parser

class EchoUDPParser:
  def __init__(self):
    pass

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