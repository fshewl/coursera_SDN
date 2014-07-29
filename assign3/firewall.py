'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''

Policy = namedtuple('Policy', ['mac_0', 'mac_1'])
policies = []

with open(policyFile, "r") as pf:
    next(pf)
    for line in pf:
        line = line.rstrip()
        tokens = line.split(",")
        mac_0 = tokens[1]
        mac_1 = tokens[2]
        policies.append(Policy(mac_0, mac_1))

flowMods = []
dropAction = of.ofp_action_output(port = of.OFPP_NONE)

for mac_0, mac_1 in policies:
    fm = of.ofp_flow_mod()
    
    matchMac = of.ofp_match(dl_src = EthAddr(mac_0), dl_dst = EthAddr(mac_1))
    fm.match = matchMac
    fm.actions.append(dropAction)
    flowMods.append(fm)

    matchMac = of.ofp_match(dl_src = EthAddr(mac_1), dl_dst = EthAddr(mac_0))
    fm.match = matchMac
    flowMods.append(fm)
    

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        for fm in flowMods:
            event.connection.send(fm)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
