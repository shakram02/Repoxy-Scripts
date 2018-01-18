#!/usr/bin/env bash
ip=$(hostname -I)   # Get the IP of the machine, configured to be static
port=$1 # Get the port supplied when launching the sciprt, 6834 / 6835
sudo ~/pox/pox.py openflow.of_01 --address=${ip} --port=${port} l2_all_to_controller info.packet_dump samples.pretty_log log.level --DEBUG