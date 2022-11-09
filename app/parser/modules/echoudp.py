from app.parser.helpers.format_helper import format_helper

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

        out.append(f'echo_server = UdpEchoServerHelper({port})')

        if len(nodes) > 1:
          # TODO musis spravit nodecontainer dalsi ktory to nainstaluje 
          pass
        else:
          # len get a install jejda
          out.append(f'server_apps = echo_server.Install(_all_nodes.Get({nodes[0]}))')
        
        start = format_helper.parse_time(cont['start']['value'], cont['start']['format'])
        stop  = format_helper.parse_time(cont['stop']['value'], cont['stop']['format'])

        out.append(f'server_apps.Start({start})')
        out.append(f'server_apps.Stop({start})')

      # TODO Tu URCITE treba pridat cisielka, lebo klientov bude vela
      elif simtype == 'client_apps':
        out.append(f'\n# Client communication...')
        cont = data['simulation'][simtype]
        port = cont['port']
        nodes = cont['nodes']
        out.append(f'echo_client = UdpEchoClientHelper()')
    return out


echo_udp_parser = EchoUDPParser()