from app.parser.modules.base import BaseParser

class NodeParser(BaseParser):
  """
  @brief Parses topology into node containers. 

  Also maps node IDs from front-end to indices in _all_nodes container.
  Use <node(cont, id)> function to get the index
  """
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
      this_cont = data['topology']['container_settings'][c]
      self.nodemap[c] = {}

      # Handle wifi container 
      #  - nodes need to be split between AP and STA containers
      if this_cont['type'] == 'wifi':
        out.append(f'{cont_name} = NodeContainer()')
        out.append(f'{cont_name}_ap = NodeContainer()')
        out.append(f'{cont_name}_sta = NodeContainer()')
        
        # Get AP node - must not be added in STA container
        ap_node = this_cont['AP']

        for i, node in enumerate(this_cont['nodes']):
          # Add every node into node map
          self.nodemap[c][node] = i
          
          # Add STA nodes into STA container
          if node != ap_node:
            cont_nodes.append(f'{cont_name}_sta.Add(_all_nodes.Get({self._to_index(node)}))')
          cont_nodes.append(f'{cont_name}.Add(_all_nodes.Get({self._to_index(node)}))')
      
        # Add AP node into AP container
        cont_nodes.append(f'{cont_name}_ap.Add(_all_nodes.Get({self._to_index(ap_node)}))')

      # Handle all other contaienrs 
      else:
        out.append(f'{cont_name} = NodeContainer()')
        print(this_cont)
        for i, node in enumerate(this_cont['nodes']):
          self.nodemap[c][node] = i
          cont_nodes.append(f'{cont_name}.Add(_all_nodes.Get({self._to_index(node)}))')
        
      out += cont_nodes

    return out

      

node_parser = NodeParser()
