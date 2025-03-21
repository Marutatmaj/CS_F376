from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI


topo = load_topo('topology.json')
controllers = {}

for switch, data in topo.get_p4rtswitches().items():
    print(switch)
    print
    controllers[switch] = SimpleSwitchP4RuntimeAPI(data['device_id'], data['grpc_port'],
                                                   p4rt_path=data['p4rt_path'],
                                                   json_path=data['json_path'])


s1_controller = controllers['s1']    
s1_controller.table_add('ipv4_lpm', 'drop')
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.1.2/32'], ['00:00:0a:01:01:02', '1'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.2.2/32'], ['00:00:0a:01:02:02', '2'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.3.2/32'], ['00:00:0a:01:03:02', '3'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:01:07:00', '4'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:01:07:00', '4'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:01:07:00', '4'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:01:07:00', '4'])
s1_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:01:07:00', '4'])

s2_controller = controllers['s2']    
s2_controller.table_add('ipv4_lpm', 'drop')
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.4.2/32'], ['00:00:0a:02:04:02', '1'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.5.2/32'], ['00:00:0a:02:05:02', '2'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.6.2/32'], ['00:00:0a:02:06:02', '3'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:02:07:00', '4'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:02:07:00', '4'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:02:07:00', '4'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:02:07:00', '4'])
s2_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:02:07:00', '4'])

s3_controller = controllers['s3']    
s3_controller.table_add('ipv4_lpm', 'drop')
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.7.2/32'], ['00:00:0a:03:07:02', '1'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.8.2/32'], ['00:00:0a:03:08:02', '2'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.9.2/32'], ['00:00:0a:03:09:02', '3'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:03:07:00', '4'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:03:07:00', '4'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:03:07:00', '4'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:03:07:00', '4'])
s3_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:03:07:00', '4'])

s4_controller = controllers['s4']
s4_controller.table_add('ipv4_lpm', 'drop')    
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.10.2/32'], ['00:00:0a:04:0a:02', '1'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.11.2/32'], ['00:00:0a:04:0b:02', '2'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.12.2/32'], ['00:00:0a:04:0c:02', '3'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:04:08:00', '4'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:04:08:00', '4'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:04:08:00', '4'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:04:08:00', '4'])
s4_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:04:08:00', '4'])

s5_controller = controllers['s5']  
s5_controller.table_add('ipv4_lpm', 'drop')  
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.13.2/32'], ['00:00:0a:05:0d:02', '1'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.14.2/32'], ['00:00:0a:05:0e:02', '2'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.15.2/32'], ['00:00:0a:05:0f:02', '3'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:05:08:00', '4'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:05:08:00', '4'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:05:08:00', '4'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:05:08:00', '4'])
s5_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:05:08:00', '4'])

s6_controller = controllers['s6']    
s6_controller.table_add('ipv4_lpm', 'drop')
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.16.2/32'], ['00:00:0a:06:10:02', '1'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.17.2/32'], ['00:00:0a:06:11:02', '2'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.18.2/32'], ['00:00:0a:06:12:02', '3'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:06:08:00', '4'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:06:08:00', '4'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:06:08:00', '4'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:06:08:00', '4'])
s6_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:06:08:00', '4'])

s7_controller = controllers['s7']   
s7_controller.table_add('ipv4_lpm', 'drop') 
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:07:01:00', '1'])
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:07:02:00', '2'])
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:07:03:00', '3'])
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:07:08:00', '4'])
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:07:08:00', '4'])
s7_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:07:08:00', '4'])

s8_controller = controllers['s8']   
s8_controller.table_add('ipv4_lpm', 'drop') 
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.1.0.0/16'], ['00:00:00:08:07:00', '4'])
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.2.0.0/16'], ['00:00:00:08:07:00', '4'])
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.3.0.0/16'], ['00:00:00:08:07:00', '4'])
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.4.0.0/16'], ['00:00:00:08:04:00', '1'])
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.5.0.0/16'], ['00:00:00:08:05:00', '2'])
s8_controller.table_add('ipv4_lpm', 'ipv4_forward', ['10.6.0.0/16'], ['00:00:00:08:06:00', '3'])