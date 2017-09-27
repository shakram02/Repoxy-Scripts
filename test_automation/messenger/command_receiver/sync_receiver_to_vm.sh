#!/usr/bin/env bash

if [ "$#" -ne 1 ];then
 echo "Invalid number of arguments"
 exit 1
fi

ip="192.168.1.2$1"
rsync -ravI ssh . --exclude=".*" "mn0@$ip:/home/mn0/px/pox-automation/command_receiver/"