'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.linkopts = [linkopts1, linkopts2, linkopts3]
        self.fanout = fanout

        # layer list contains three lists
        # layer[0] = [c1]
        # layer[1] = [a1, a2]
        # layer[2] = [e1, e2, e3, e4]
        layer = [[], [], []]
        for i in range(0, 4):
            if i == 0:
                switch = self.addSwitch('c1')
                layer[0].append(switch)
            elif i <= 2:
                name = ""
                if i == 1:
                    name = "a"
                else:
                    name = "e"
                count = 1
                for node in layer[i-1]:
                    for j in range(1, fanout+1):
                        switch = self.addSwitch('%s%s' % (name, count))
                        self.addLink(switch, node, **self.linkopts[i-1])
                        layer[i].append(switch)
                        count += 1
            else:
                count = 1
                for node in layer[2]:
                    for j in range(1, fanout+1):
                        host = self.addHost('h%s' % count)
                        self.addLink(host, node, **self.linkopts[2])
                        count += 1
                    
topos = { 'custom': ( lambda: CustomTopo() ) }
