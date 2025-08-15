#!/bin/bash

source /environment.sh

dt-launchfile-init
rosrun avoid_duck wheel_control_node.py
dt-launchfile-join