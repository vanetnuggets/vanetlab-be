from app.model.base import BaseModel
from app.parser.helpers.concat_helper import add

class HelperModel(BaseModel):
    def __init__(self, node_id, network, name, port, start_val, start_format, stop_val, stop_format):
        self.node_id = node_id
        self.network = network
        self.name = name
        self.port = port
        self.start_val = start_val
        self.start_format = start_format
        self.stop_val = stop_val
        self.stop_format = stop_format


class BulkSendHelper(HelperModel):
    def __init__(self, node_id, network, name, port, max_byte, start_val, start_format, stop_val, stop_format):
        super().__init__(node_id, network, name, port, start_val, start_format, stop_val, stop_format)
        self.max_byte = max_byte
    
    def dumppy(self) -> str:
        res = []
        add(res, f'{self.name} = BulkSendHelper("ns3::TcpSocketFactory", InetSocketAddress (i.GetAddress (1), {self.port}))')
        add(res, f'{self.name}.SetAttribute ("MaxBytes", UintegerValue ({self.max_byte}))')
        add(res, f'sourceApps = source.Install (nodes.Get (0))')
        add(res, f'sourceApps.Start (Seconds ({self.start_val}))')
        add(res, f'sourceApps.Stop (Seconds ({self.stop_val}))')
        return res

class PacketSinkHelper(HelperModel):
    def __init__(self, node_id, network, name, port, start_val, start_format, stop_val, stop_format):
        super().__init__(node_id, network, name, port, start_val, start_format, stop_val, stop_format)

    def dumppy(self) -> str:
        res = []
        add(res, f'{self.name} = PacketSinkHelper("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), {self.port}))')
        add(res, f'sinkApps = {self.name}.Install (nodes.Get (1))')
        add(res, f'sinkApps.Start (Seconds ({self.start_val}))')
        add(res, f'sinkApps.Stop (Seconds ({self.stop_val}))')
        return res