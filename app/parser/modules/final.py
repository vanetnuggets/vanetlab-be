class FinalParser:
  def __init__(self):
    pass
  
  def parse(self, data):
    out = []
    
    out.append(f'\n# finishing touches...')
    out.append(f'Ipv4GlobalRoutingHelper.PopulateRoutingTables()')
    out.append(f'Simulator.Run()')
    out.append(f'Simulator.Destroy()')

    return out

final_parser = FinalParser()
