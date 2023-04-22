import re
from app.managers.filemanager import filemanager
from pprint import pprint

MOBILITY = 'mobility'
AT = 'at'
MAX_AT = 'max_at'
NODES = 'nodes'
X = 'x'
Y = 'y'
Z = 'z'

class TclParser():
    def __init__(self):
        pass
    
    def _init_node(self, config, node_num):
        config[NODES][node_num] = {}
        config[NODES][node_num]['id'] = node_num
        config[NODES][node_num]['type'] = 'basic'
        config[NODES][node_num]['l2id'] = -1
        config[NODES][node_num]['l2'] = None
        config[NODES][node_num]['l2conf'] = {}
        config[NODES][node_num]['l3'] = None
        config[NODES][node_num]['l3conf'] = {}
        config[NODES][node_num]['mobility'] = {}
        config[NODES][node_num]['x'] = None
        config[NODES][node_num]['y'] = None

    def tcl_to_conf(self, mobility_path) -> dict:
        conf = {NODES: {}, MAX_AT: 0}
        with open(mobility_path) as f:
            reg_ns = r"\$ns_"
            reg_node = r"\$node_\((\d+)\)"
            max_at = 0
            min_at = {}
            min_nums = {}
            for line in f.readlines():
                if re.search(reg_ns, line):
                    sp = line.split()
                    at = float(sp[2])
                    if max_at < at : max_at = at
                    
                    node_num = int(re.search(reg_node, sp[3]).group(1))
                    x = float(sp[5])
                    y = float(sp[6])
                    z = float(sp[7].replace('"', ''))

                    if node_num not in conf[NODES].keys():
                        self._init_node(conf, node_num)
                    
                    conf[NODES][node_num][MOBILITY][at] = {X: x, Y: y, Z: z}
                    
                    if node_num not in min_at or min_at[node_num] > at:
                        min_at[node_num] = at 
                        conf[NODES][node_num][X] = x
                        conf[NODES][node_num][Y] = y
            conf[MAX_AT] = max_at
            conf['networks'] = {}
        return conf

    def conf_to_tcl(self, name, conf, save_to=None):
        lines = []
        node_nums = list(conf[NODES].keys())
        # dict used to determine if node x, y, z is needed to print
        used_nodes = {num: True for num in node_nums}
        for at in range(int(conf[MAX_AT]+1)):
            for node_num in node_nums:
                data = conf[NODES][node_num][MOBILITY]
                at = str(float(at))
                if at in data:
                    if used_nodes[node_num]:
                        lines.append(f'$node_({node_num}) set X_ {data[at][X]}')
                        lines.append(f'$node_({node_num}) set Y_ {data[at][Y]}')
                        lines.append(f'$node_({node_num}) set Z_ {data[at][Z]}')
                        used_nodes[node_num] = False
                    lines.append(f'$ns_ at {at} "$node_({node_num}) setdest {data[at][X]} {data[at][Y]} {data[at][Z]}"')
        filemanager.save_tcl(name, lines, save_to)

tcl_parser = TclParser()
