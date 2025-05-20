from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
import re
from datetime import datetime, timedelta




topo = load_topo('topology.json')
controllers = {}

for switch, data in topo.get_p4rtswitches().items():
    controllers[switch] = SimpleSwitchP4RuntimeAPI(data['device_id'], data['grpc_port'],
                                                   p4rt_path=data['p4rt_path'],
                                                   json_path=data['json_path'])

s1_controller = controllers['s1']    
s1_controller.table_add('ipv4_lpm', 'drop')                    
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.1.2/32'], ['00:00:0a:01:01:02', '1'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.2.2/32'], ['00:00:0a:01:02:02', '2'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.3.2/32'], ['3e:ad:09:92:a2:dd', '3'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.4.2/32'], ['3e:ad:09:92:a2:dd', '3'])

s2_controller = controllers['s2']            
s2_controller.table_add('ipv4_lpm', 'drop')             
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.1.2/32'], ['7a:93:a0:aa:90:6d', '3'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.2.2/32'], ['7a:93:a0:aa:90:6d', '3'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.3.2/32'], ['00:00:0a:02:03:02', '1'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.4.2/32'], ['00:00:0a:02:04:02', '2'])