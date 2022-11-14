class NodeParser:
  def __init__(self):
    nodemap = {}

  def node(self, cont, i):
    return self.nodemap[cont][i]

  def parse(self, data):
    self.nodemap = {}
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
      out.append(f'{cont_name} = NodeContainer()')
      
      self.nodemap[c] = []
      
      for i, node in enumerate(data['topology']['container_settings'][c]['nodes']):
        cont_nodes.append(f'{cont_name}.Add(_all_nodes.Get({node}))')
        self.nodemap[c].append(i)
        
      out.append(cont_name)
      out += cont_nodes
    print(self.nodemap)
    return out

      


node_parser = NodeParser()