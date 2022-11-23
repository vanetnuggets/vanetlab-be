from app.parser.modules.base import BaseParser

class LogParser(BaseParser):
  def __init__(self):
    pass
  
  def parse(self, data):
    out = []
    out += [
      f'LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO)',
	    f'LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO)'
    ]
    return out



log_parser = LogParser()