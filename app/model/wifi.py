# "wifi": {
#   // Definition params
#   "name": "whatever"
#   "type": "wifi"
#   // Wifi specific params
#   // lets assume that all wifi networks will have one access point and any number of station nodes
#   "ssid": "string"
#   "AP": 0,
#   "nodes": [
#     1, 2, 3, 4 ... // must NOT contain AP node ID
#   ]
#   // Other attributes hardcoded for now as we have no idea tf they even mean
#   // Inherited params:
#   "network_address": "10.0.0.0",
#   "network_mask": "255.255.255.0",
#   "log_pcap": true,
#   "log_ascii": true,
# }

from app.model.base import BaseModel
from app.parser.helpers.concat_helper import add
from app.parser.helpers.format_helper import format_helper

imports = [
  "from ns.applications import *"
  "from ns.core import *"
  "from ns.mobility import *"
  "from ns.network import *"
  "from ns.wifi import *"
]

class WifiModel(BaseModel):
  """
  @brief Adds a wifi network into the scenario

  self explanatory.

  @param ap - index of ap node in global _all_nodes container
  @param nodes - any number of nodes as indexes in global _all_nodes container 
  """
  def __init__(self, name, ssid, ap, nodes, log_pcap=False, log_ascii=False):
    self.name = name
    self.ssid = ssid
    self.ap = ap
    self.nodes = nodes
    self.log_pcap = log_pcap
    self.log_ascii = log_ascii
  
  """
  @brief generates python ns3 simulation script for wifi network creation
  """
  def dumppy(self):
    res = []

    # Initialize container specific values
    sta = f'{self.name}_sta_nodes'
    ap = f'{self.name}_ap_nodes'
    wifi_mac = f'{self.name}_mac'
    wifi_phy = f'{self.name}_phy'
    wifi_chn = f'{self.name}_chn'
    ssid = format_helper.ssid_value(self.ssid)

    # Creates node containers
    add(res, "{sta} = NodeContainer()")
    add(res, "{ap}  = NodeContainer()")

    add(res, "{sta}.Create({len(self.nodes)})")
    add(res, "{ap}.Create(1)")

    # Add needed imports which are not yet imported
    for imp in imports:
      if self.daddy.check_import(imp) == False:
        res.append(imp)

    # Setup generic wifi shit
    # No config here, idk what even to configure, its just gibberish
    add(res, f'{self.name} = WifiHelper()')
    add(res, f'{wifi_phy} = YansWifiPhyHelper.Default()')
    add(res, f'{wifi_chn} = YansWifiChannelHelper.Default()')
    add(res, f'{wifi_phy}.SetChannel({wifi_chn}.Create())')
    add(res, f'{self.name}.SetRemoteStationManager("ns3::ArfWifiManager")')
    
    # Create MAC layer for AP node and install AP node config
    add(res, f'{wifi_mac} = WifiMacHelper')
    add(res, f'{wifi_mac}.SetType("ns3::StaWifiMac", "Ssid", "{ssid}"))')
    
    # TODO XXX verify if _devices is ok ? maybe needs to be _interfaces idk
    add(res, f'{ap}_devices = {self.name}.Install({wifi_phy}, {wifi_chn}, {ap})')
    
    # Create MAC layer for STA nodes and install STA node config
    add(res, f'{wifi_mac}.SetType("ns3::ApWifiMac", "Ssid", "{ssid}"))')
    add(res, f'{sta}_devices = {self.name}.Install({wifi_phy}, {wifi_chn}, {sta})')

    return res
