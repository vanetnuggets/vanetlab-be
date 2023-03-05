import re
import pprint

PATH = 'C:/Users/PC/Downloads/Export kodov z GitHub/TP_FIIT-main/Sumo_to_NS3_using_NS2/ns2mobility.tcl'
MOBILITY = 'mobility'
AT = 'at'
MAX_AT = 'max_at'
NODES = 'nodes'
X = 'x'
Y = 'y'
Z = 'z'

class TclParser():
    def __init__(self) -> None:
        # TODO toto sa este naplni ked sa finishne endpoint
        pass

    def tcl_to_conf(self, mobility_path) -> dict:
        conf = {NODES: {}, MAX_AT: 0}
        with open(mobility_path) as f:
            reg_ns = r"\$ns_"
            reg_node = r"\$node_\((\d+)\)"
            max_at = 0
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
                        conf[NODES][node_num] = {}
                        conf[NODES][node_num][MOBILITY] = {}
                    conf[NODES][node_num][MOBILITY][at] = {X: x, Y: y, Z: z}
            conf[MAX_AT] = max_at
            # pprint.pprint(conf)
        return conf

    def conf_to_tcl(self, conf):
        # TODO replace prints with file writeline
        node_nums = list(conf[NODES].keys())
        # dict used to determine if node x, y, z is needed to print
        used_nodes = {num: True for num in node_nums}
        for at in range(int(conf[MAX_AT]) + 1):
            for node_num in node_nums:
                data = conf[NODES][node_num][MOBILITY]
                at = float(at)
                if at in data:
                    if used_nodes[node_num]:
                        print(f'$node_({node_num}) set X_ {data[at][X]}')
                        print(f'$node_({node_num}) set Y_ {data[at][Y]}')
                        print(f'$node_({node_num}) set Z_ {data[at][Z]}')
                        used_nodes[node_num] = False
                    print(f'$ns_ at {at} "$node_({node_num}) setdest {data[at][X]} {data[at][Y]} {data[at][Z]}"')

tcl_parser = TclParser()