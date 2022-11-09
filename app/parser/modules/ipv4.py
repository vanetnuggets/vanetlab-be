class IPv4Parser:
  def __init__(self):
    pass

  def parse(self, data):
    out = []

    out.append(f'\n# Internet Stack')
    out.append(f'stack = InternetStackHelper()')
    out.append(f'stack.Install(_all_nodes)')


    out.append(f'\n# Assign Address')
    out.append(f'address = IPv4AddressHelper()')

    containers = data['topology']['node_containers']
    for c in containers:
      cont = data['topology']['container_settings'][c]
      
      addr = cont['network_address']
      mask = cont['network_mask']

      out.append(f'address.SetBase(IPv4Address(\"{addr}\"), IPv4Mask(\"{mask}\"))')
      out.append(f'{c}_interfaces = address.Assign({c}_devices)')




    return out

ipv4parser =  IPv4Parser()