from app.parser.modules.base import BaseParser

class NodeParser(BaseParser):
  def __init__(self):
    # Maps ID of node to its position
    self.nodemap = {}

    self.nodes = {}

  # Get INDEX of NODE with ID <id> in CONTAINER <cont>
  def node(self, cont, id):
    return self.nodemap[cont][id]

  def _to_index(self ,id):
    return self.nodes[id]

  def parse(self, data):
    self.nodemap = {}


    out = []
    node_count = data['topology']['node_count']
    node_count = 100 # TODO FIX POVEDZ VOJTOVI NEH TO POROBI
    containers = data['topology']['node_containers']

    # Create initial node mappings

    i = 0
    for x in containers:
      nodes = data['topology']['container_settings'][x]['nodes']
      for y in nodes:
        if y not in self.nodes:
          self.nodes[y] = i
          i += 1
    
    all_nodes = [
      f'_all_nodes = NodeContainer()',
      f'_all_nodes.Create({node_count})'
    ]
    out += all_nodes

    print(self.nodes);
    
    for c in containers:
      cont_nodes = []
      cont_name = f'{c}_container'
      out.append(f'{cont_name} = NodeContainer()')
      
      self.nodemap[c] = {}


      for i, node in enumerate(data['topology']['container_settings'][c]['nodes']):
        self.nodemap[c][node] = i

        cont_nodes.append(f'{cont_name}.Add(_all_nodes.Get({self._to_index(node)}))')
        
      out += cont_nodes

    return out

      

node_parser = NodeParser()
