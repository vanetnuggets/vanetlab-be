class NodeParser:
  def __init__(self):
    pass



  def parse(self, data):
    out = []

    node_count = data['topology']['node_count']
    all_nodes = [
      f'_all_nodes = NodeContainer()',
      f'_all_nodes.Create({node_count})'
    ]
    out += all_nodes

    containers = data['topology']['node_containers']
    for c in containers:
      cont_nodes = []
      cont_name = f'{c}_container'
      for node in data['topology']['container_settings'][c]['nodes']:
        cont_nodes.append(f'{cont_name}.Add(_all_nodes.Get({node}))')

      out.append(cont_name)
      out += cont_nodes

    return out

      


node_parser = NodeParser()