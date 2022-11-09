from app.parser.modules.nodes import node_parser
from app.parser.modules.csma import csma_parser
from app.parser.modules.echoudp import echo_udp_parser
from app.parser.modules.ipv4 import ipv4parser
from app.parser.modules.p2p import p2p_parser
from app.parser.modules.log import log_parser
from app.parser.modules.final import final_parser

import json

class Parser:
  def __init__(self):
    self.buf = []

  def add(self, item):
    self.buf += item
  
  def _to_json(self, filename):
    with open(filename, 'r') as f:
      return json.loads(f.read())

  def parse(self, filename):
    json = self._to_json(filename)

    nodes = node_parser.parse(json)
    self.add(nodes)
    p2p = p2p_parser.parse(json)
    self.add(p2p)
    csma = csma_parser.parse(json)
    self.add(csma)
    ipv4 = ipv4parser.parse(json)
    self.add(ipv4)
    sim = echo_udp_parser.parse(json)
    self.add(sim)
    logs = log_parser.parse(json)
    self.add(logs)
    final = final_parser.parse(json)
    self.add(final)

    
    return '\n'.join(self.buf)

parser = Parser()
