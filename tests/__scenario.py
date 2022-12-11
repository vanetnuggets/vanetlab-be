from ns.core import *
from ns.network import *
from ns.csma import *
from ns.internet import *
from ns.point_to_point import *
from ns.applications import *
import sys
LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO)
LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO)
_all_nodes = NodeContainer()
_all_nodes.Create(100)
csma_nodes_container = NodeContainer()
csma_nodes_container.Add(_all_nodes.Get(0))
csma_nodes_container.Add(_all_nodes.Get(1))
csma_nodes_container.Add(_all_nodes.Get(2))
csma_nodes_container.Add(_all_nodes.Get(3))
p2p_nodes_container = NodeContainer()
p2p_nodes_container.Add(_all_nodes.Get(3))
p2p_nodes_container.Add(_all_nodes.Get(4))

# Wifi L2 configuration
# Point-To-Point
p2p_nodes_p2p_helper = PointToPointHelper()
p2p_nodes_p2p_helper.SetDeviceAttribute("DataRate", StringValue("100Mbps"))
p2p_nodes_p2p_helper.SetChannelAttribute("Delay", StringValue("1ns"))
p2p_nodes_devices = p2p_nodes_p2p_helper.Install(p2p_nodes_container)
p2p_nodes_p2p_helper.EnablePcapAll("p2p_nodes")
# CSMA 
csma_nodes_csma_helper = CsmaHelper()
csma_nodes_csma_helper.SetChannelAttribute("DataRate", StringValue("100Mbps"))
csma_nodes_csma_helper.SetChannelAttribute("Delay", TimeValue(NanoSeconds(1)))
csma_nodes_devices = csma_nodes_csma_helper.Install(csma_nodes_container)
csma_nodes_csma_helper.EnablePcapAll("csma_nodes")

# Internet Stack
stack = InternetStackHelper()
stack.Install(_all_nodes)

# Assign Address
address = Ipv4AddressHelper()
address.SetBase(Ipv4Address("10.1.1.0"), Ipv4Mask("255.255.255.0"))
csma_nodes_interfaces = address.Assign(csma_nodes_devices)
address.SetBase(Ipv4Address("10.2.2.0"), Ipv4Mask("255.255.255.0"))
p2p_nodes_interfaces = address.Assign(p2p_nodes_devices)

# UDP Echo client
echo_client = UdpEchoClientHelper(csma_nodes_interfaces.GetAddress(3), 9)
echo_client.SetAttribute('MaxPackets', UintegerValue(10))
echo_client.SetAttribute('Interval', TimeValue(Seconds(1.0)))
echo_client.SetAttribute('PacketSize', UintegerValue(128))
echo_client_apps = echo_client.Install(csma_nodes_container.Get(0))
echo_client_apps.Start(Seconds(1.0))
echo_client_apps.Stop(Seconds(10.0))

# Parsing Echo Server
echo_server = UdpEchoServerHelper(9)
echo_server_apps = echo_server.Install(csma_nodes_container.Get(3))
echo_server_apps.Start(Seconds(1.0))
echo_server_apps.Stop(Seconds(10.0))

# Trace pcap
csma_nodes_csma_helper.EnablePcapAll("csma_nodes")
p2p_nodes_p2p_helper.EnablePcapAll("p2p_nodes")

# finishing touches...
Ipv4GlobalRoutingHelper.PopulateRoutingTables()
Simulator.Stop(Seconds(10.0))
Simulator.Run()
Simulator.Destroy()