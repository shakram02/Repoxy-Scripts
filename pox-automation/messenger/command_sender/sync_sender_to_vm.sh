#!/usr/bin/env bash

ip="192.168.1.241"
rsync -ravI ssh . "mn0@$ip:/home/mn0/px/pox-automation/command_sender/"