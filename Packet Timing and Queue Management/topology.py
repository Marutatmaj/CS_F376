from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

net.setLogLevel('info')
net.setCompiler(p4rt=True)
net.execScript('python3 controller.py', reboot=True)

net.addP4RuntimeSwitch('s1')
net.addP4RuntimeSwitch('s2')
net.setP4SourceAll('p4src/src.p4')

net.addHost('h1')
net.addHost('h2')
net.addHost('h3')
net.addHost('h4')

net.addLink('h1','s1')
net.addLink('h2','s1')
net.addLink('h3','s2')
net.addLink('h4','s2')
net.addLink('s1','s2')

net.l3()
net.enablePcapDumpAll()
net.enableLogAll()
net.enableCli()
net.startNetwork()