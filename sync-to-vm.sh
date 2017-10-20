#!/usr/bin/env bash

if [ "$#" -ne 1 ];then
 echo "Invalid number of arguments, Usage: sync-to-vm machine_number"
 exit 1
fi

pass="mininet"
# Align the command parameters with python script parameters, just supply machine number (1,4,5)
ip="192.168.1.24$1"

# Sync controller component
#rsync -ravI ssh ./controller-component/l2_all_to_controller.py "mn0@$ip:/home/mn0/pox/ext/"

rsync -ravI ssh --exclude=".*" . "mn0@$ip:/home/mn0/px/$(basename "$PWD")/"