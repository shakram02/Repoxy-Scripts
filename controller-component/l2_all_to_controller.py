# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A super simple OpenFlow switch that forwards all packets to controller 
-----------------------------------------
Rename this file to whatever you like, .e.g., mycomponent.py.  You can
then invoke it with "./pox.py mycomponent" if you leave it in the
ext/ directory.

Edit this docstring and your launch function's docstring.  These will
show up when used with the help component ("./pox.py help --mycomponent").
"""

# These next two imports are common POX convention
from pox.core import core
import pox.openflow.libopenflow_01 as of

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# This table maps (switch,MAC-addr) pairs to the port on 'switch' at
# which we last saw a packet *from* 'MAC-addr'.
# (In this case, we use a Connection object for the switch.)
table = {}

# To send out all ports, we can use either of the special ports
# OFPP_FLOOD or OFPP_ALL.  We'd like to just use OFPP_FLOOD,
# but it's not clear if all switches support this, so we make
# it selectable.
all_ports = of.OFPP_FLOOD

# Socket sending feedback to test manager
to_test_manager = None
sent_ready = False

from pox.lib.packet.ethernet import ethernet


# Handle messages the switch has sent us because it has no
# matching rule.
def _handle_PacketIn(event):
    global sent_ready
    packet = event.parsed

    # Learn the source
    table[(event.connection, packet.src)] = event.port

    # dst_port = table.get((event.connection, packet.dst))

    # send the packet out all ports (except the one it came in on!)
    # and hope the destination is out there somewhere. :)
    msg = of.ofp_packet_out(data=event.ofp)
    msg.actions.append(of.ofp_action_output(port=all_ports))
    event.connection.send(msg)

    if not sent_ready and packet.type != ethernet.ARP_TYPE:
        sent_ready = True
        core.quit()

    log.debug("Forwarding %s <-> %s" % (packet.src, packet.dst))


def connect_to_test_manager():
    global to_test_manager
    # Open TCP connection to vm 101
    # Send the ready message
    from socket import socket, AF_INET, SOCK_STREAM
    test_manager_ip = "192.168.1.241"
    test_manager_port = 6931

    to_test_manager = socket(AF_INET, SOCK_STREAM)

    try:
        to_test_manager.connect((test_manager_ip, test_manager_port))
        log.debug("Connected to : " + test_manager_ip)
        to_test_manager.close()
    except Exception as e:
        log.info("Couldn't connect to test manager" + str(e))
        return False

    return True


def send_ready():
    global sent_ready
    message = "UP"

    to_test_manager.send(message.encode())
    to_test_manager.close()
    sent_ready = True


def launch(disable_flood=False):
    global all_ports
    if disable_flood:
        all_ports = of.OFPP_ALL

    connected = connect_to_test_manager()
    # Even a simple usage of the logger is much nicer than print!
    # core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

    if connected:
        core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
        log.warn("Forwarding switch running.")
        log.info("Make sure that this component is running on the main controller FGS")
    else:
        log.warn("Failed to connect to test manager, Forwarding switch won't run")
        core.quit()
