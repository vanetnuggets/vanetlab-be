from app.parser.modules.base import BaseParser
from app.model.helper import BulkSendHelper, PacketSinkHelper

class HelperParser(BaseParser):
    def __init__(self):
        super().__init__()
    
    def _get_common_vars(self, rec):
        node_id = rec['node_id']
        network = rec['network']
        name = rec['name']
        port = rec['port']
        start_val = rec['start']['value']
        start_format = rec['start']['format']
        stop_val = rec['stop']['value']
        stop_format = rec['stop']['format']
        return node_id, network, name, port, start_val, start_format, stop_val, stop_format

    def parse_bulk(self, data):
        out = []
        out.append(f'\n# BulkSendHelper')

        for cont in data['topology']['node_containers']:
            settings = data['topology']['container_settings'][cont]
            
            if settings['type'] == 'csma':
                rec = data['simulation']['bulk_send_helper']
                node_id, network, name, port, start_val, start_format, stop_val, stop_format = self._get_common_vars(rec=rec)
                max_byte = rec['max_byte']
                
                helper = BulkSendHelper(
                    node_id=node_id,
                    network=network,
                    name=name,
                    port=port,
                    max_byte=max_byte,
                    start_val=start_val,
                    start_format=start_format,
                    stop_val=stop_val,
                    stop_format=stop_format
                )
                out += helper.dumppy()
        
        return out
    
    def parse_sink(self, data):
        out = []
        out.append(f'\n# PacketSinkHelper')

        for cont in data['topology']['node_containers']:
            settings = data['topology']['container_settings'][cont]
            
            if settings['type'] == 'csma':
                rec = data['simulation']['packer_sink_helper']
                node_id, network, name, port, start_val, start_format, stop_val, stop_format = self._get_common_vars(rec=rec)
                
                helper = PacketSinkHelper(
                    node_id=node_id,
                    network=network,
                    name=name,
                    port=port,
                    start_val=start_val,
                    start_format=start_format,
                    stop_val=stop_val,
                    stop_format=stop_format
                )
                out += helper.dumppy()
        
        return out