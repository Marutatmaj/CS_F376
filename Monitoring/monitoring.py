import sys
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


class ReadCounters(object):

    def __init__(self, sw_name):
        self.topo = load_topo('topology.json')
        self.sw_name = sw_name
        self.thrift_port = self.topo.get_thrift_port(sw_name)
        self.controller = SimpleSwitchThriftAPI(self.thrift_port)

    def read(self):
        entries = self.controller.table_num_entries('count_table')
        for i in range(0,4):
            self.controller.counter_read('direct_port_counter', i)


if __name__ == '__main__':
    ReadCounters('s1').read()