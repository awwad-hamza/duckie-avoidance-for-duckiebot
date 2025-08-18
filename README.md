
# Duckiebot Object Avoidance

This project implements a simple **object avoidance system** for [Duckietown's](https://duckietown.com/) Duckiebot DB21M using the **front-center Time-of-Flight (ToF) sensor** and wheel commands.  
The bot drives forward, monitors the ToF sensor, and when an obstacle is detected within a safety threshold, it executes an avoidance maneuver.

---

## Features
- Moves forward at a constant speed.
- Continuously monitors the front-center ToF sensor (`/VEHICLE_NAME/front_center_tof_driver_node/range`).
- Stops if an obstacle is closer than the safety distance.
- Turns right after detection.
- Terminates the node automatically after avoidance.

---

## Repository Layout
```bash
duckie-avoidance-for-duckiebot/
├── assets/                  # Place assets if needed
├── configurations.yaml      # Configurations for container
├── dependencies-apt.txt     # APT dependencies
├── dependencies-py3.dt.txt  # Python dependencies (Duckietown format)
├── dependencies-py3.txt     # Python dependencies (pip)
├── Dockerfile               # Container build file
├── docs/                    # Documentation files
├── html/                    # Generated HTML docs
├── launchers/
│   ├── default.sh
│   └── wheel-control.sh     # Script to launch wheel control node
├── packages/
│   └── avoid_duck/
│       ├── CMakeLists.txt   # ROS CMake configuration
│       ├── package.xml      # ROS package manifest
│       └── src/
│           └── wheel_control_node.py # Main ROS node
└── README.md
```

---

##  Usage

### 1. Make the Node and Launch FileExecutable
Before running, give execution permission to the node script:
```bash
chmod +x ./packages/avoid_duck/src/wheel_control_node.py
chmod +x ./launchers/wheel-control.sh
```
### 2. Run Options

You have two ways to build and run the node:

🔹 Option A: Run from your PC (Fast Testing)

This allows you to test quickly over the ROS network, but note there can be some delay with the ToF sensor.
```bash
dts devel build -f
dts devel run -R ROBOT_NAME -L wheel-control
```
🔹 Option B: Run Directly on the Duckiebot (Recommended)

This builds and runs the node on the robot itself for more reliable sensor performance.

Build:
```bash
dts devel build -H ROBOT_NAME -f
```
If the build fails, try pulling the latest base image:
```bash
dts devel build -H ROBOT_NAME -f --pull
```
Run
```
dts devel run -H ROBOT_NAME -L wheel-control
```
