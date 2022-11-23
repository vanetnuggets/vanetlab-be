from app.parser.modules.nodes import node_parser, NodeParser
from app.parser.modules.csma import csma_parser, CSMAParser
from app.parser.modules.echoudp import echo_udp_parser, EchoUDPParser
from app.parser.modules.ipv4 import ipv4parser, IPv4Parser
from app.parser.modules.p2p import p2p_parser, P2PParser
from app.parser.modules.log import log_parser, LogParser
from app.parser.modules.final import final_parser, FinalParser
from app.parser.modules.pcap import pcap_parser, PcapParser

import json

class Parser:
  def __init__(self):
    self.buf = []
    self.node_parser = NodeParser()
    self.node_parser.init(self)
    self.csma_parser = CSMAParser()
    self.csma_parser.init(self)
    self.echo_udp_parser = EchoUDPParser()
    self.echo_udp_parser.init(self)
    self.ipv4parser = IPv4Parser()
    self.ipv4parser.init(self)
    self.p2p_parser = P2PParser()
    self.p2p_parser.init(self)
    self.log_parser = LogParser()
    self.log_parser.init(self)
    self.final_parser = FinalParser()
    self.final_parser.init(self)
    self.pcap_parser = PcapParser()
    self.pcap_parser.init(self)

  def add(self, item):
    self.buf += item
  
  def _to_json(self, filename):
    with open(filename, 'r') as f:
      return json.loads(f.read())

  def _add_imports(self):
    self.add([
      "from ns.core import *",
      "from ns.network import *",
      "from ns.csma import *",
      "from ns.internet import *",
      "from ns.point_to_point import *",
      "from ns.applications import *",
      "import sys"
    ])

  def p(self, filename, iam_json=False):
    if iam_json is False:
      data = self._to_json(filename)
    else:
      data = json.loads(filename)

    print('------')
    print(data)
    self._add_imports()

    logs = log_parser.parse(data)
    self.add(logs)
    nodes = self.node_parser.parse(data)
    self.add(nodes)
    p2p = p2p_parser.parse(data)
    self.add(p2p)
    csma = csma_parser.parse(data)
    self.add(csma)
    ipv4 = ipv4parser.parse(data)
    self.add(ipv4)
    sim = self.echo_udp_parser.p(data)
    self.add(sim)
    
    final = final_parser.parse(data)
    self.add(final)

    
    return '\n'.join(self.buf)


  def parse(self, filename, iam_json=False):
    if iam_json is False:
      data = self._to_json(filename)
    else:
      data = json.loads(filename)

    print('------')
    print(data)
    self._add_imports()

    logs = log_parser.parse(data)
    self.add(logs)
    nodes = node_parser.parse(data)
    self.add(nodes)
    p2p = p2p_parser.parse(data)
    self.add(p2p)
    csma = csma_parser.parse(data)
    self.add(csma)
    ipv4 = ipv4parser.parse(data)
    self.add(ipv4)
    sim = echo_udp_parser.parse(data)
    self.add(sim)
    
    final = final_parser.parse(data)
    self.add(final)

    
    return '\n'.join(self.buf)

parser = Parser()
