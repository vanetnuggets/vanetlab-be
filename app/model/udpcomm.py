from app.model.base import BaseModel

class UDPServer(BaseModel):
  def __init__(self, port=None, name=None, start=None, stop=None, network=None, node=None, attrs=[]):
    self.port = port
    self.name = name
    self.start = start
    self.stop = stop
    self.network = network
    self.node = node

    self.attrs = attrs
    self.essential = [
      'port', 'name', 'start', 'stop', 'network', 'node'
    ]

    self.apps = f'{self.name}_apps'
    
  def dumppy(self) -> str:
    if self.check_essential() == False:
      raise Exception("missing essential values:", ''.join(self.get_missing()))
    res = [
      f"{self.name} = UdpEchoServerHelper({self.port})"
    ]
    if self.attrs is not None:
      for x in self.attrs:
        attr, val = x
        res.append(
          f"{self.name}.SetAttribute('{attr}', {val})"
        )
    res.append(
      f'{self.apps} = {self.name}.Install({self.network}.Get({self.node}))'
    )
    res.append(
      f'{self.apps}.Start({self.start})'
    )
    res.append(
      f'{self.apps}.Stop({self.stop})'
    )

    return res

  def dumpcc(self) -> str:
    return ""

class UDPClient(BaseModel):
  def __init__(self, port=None, name=None, node=None, 
      start=None, stop=None, server_node=None, 
      server_network=None, network=None, attrs=[]):

    self.port = port
    self.name = name
    self.node = node
    
    self.start = start
    self.stop = stop
    
    self.server_node = server_node
    self.server_network = server_network
    self.network = network

    self.attrs = attrs
    self.apps = f'{self.name}_apps'

    self.essential = [
      'port', 'name', 'node', 'start', 'stop', 'server_node', 'server_network', 'network'
    ]

  def dumppy(self) -> str:
    if self.check_essential() == False:
      raise Exception("missing essential values:", ''.join(self.get_missing()))
    res = [
      f"{self.name} = UdpEchoClientHelper({self.server_network}.GetAddress({self.server_node}), {self.port})"
    ]
    if self.attrs is not None:
      for x in self.attrs:
        attr, val = x
        res.append(
          f"{self.name}.SetAttribute('{attr}', {val})"
        )
    res.append(
      f"{self.apps} = {self.name}.Install({self.network}.Get({self.node}))"
    )
    res.append(
      f"{self.apps}.Start({self.start})"
    )
    res.append(
      f"{self.apps}.Stop({self.stop})"
    )
    return res

  def dumpcc(self) -> str:
    return ""

