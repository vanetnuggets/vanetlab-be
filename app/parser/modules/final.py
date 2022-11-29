from app.parser.modules.base import BaseParser

class FinalParser(BaseParser):
  def __init__(self):
    pass
  
  def parse(self, data):
    out = []
    
    out.append(f'\n# finishing touches...')
    out.append(f'Ipv4GlobalRoutingHelper.PopulateRoutingTables()')
    out.append(f'Simulator.Stop(Seconds(10.0))')
    out.append(f'Simulator.Run()')
    out.append(f'Simulator.Destroy()')

    return out

final_parser = FinalParser()
