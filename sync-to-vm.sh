#!/usr/bin/env bash

if [ "$#" -ne 1 ];then
 echo "Invalid number of arguments"
 exit 1
fi

pass="mininet"
ip="192.168.1.2$1"

# Sync controller component
#rsync -ravI ssh --exclude=".*"\
#./controller-component/l2_all_to_controller.py \
#"mn0@$ip:/home/mn0/pox/ext/"

rsync -ravI ssh  --exclude=".*" . "mn0@$ip:/home/mn0/px/$(basename "$PWD")/"