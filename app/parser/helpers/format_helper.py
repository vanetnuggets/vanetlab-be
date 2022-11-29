class FormatHelper:
  def __init__(self):
    pass
  
  def string_value(self, val, format):
    return f'StringValue("{val}{format}")'
  
  def parse_time(self, val, format):
    if format == 's':
      return f'Seconds({val}.0)'
    elif format == 'ns':
      return f'NanoSeconds({val})'
    return f'MiliSeconds({val})'

  def time_value(self, val, format):
    r = self.parse_time(val, format)
    return f'TimeValue({r})'

  def parse_uint(self, val):
    return f'UintegerValue({val})'

  def ssid_value(self, val):
    return f'SsidValue(Ssid("{val}"))'
format_helper = FormatHelper()