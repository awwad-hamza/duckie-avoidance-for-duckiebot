#!/usr/bin/env python3

'''
WheelControlNode: Autonomous obstacle-avoiding wheel control for Duckietown robots.

This ROS node subscribes to the front-center Time-of-Flight (ToF) distance sensor and 
publishes wheel velocity commands to control the robot's movement. Its main function 
is to move forward when the path is clear and avoid collisions by stopping and spinning 
in place when an obstacle is detected.

Key Features:
- Reads distance data from the ToF sensor.
- Stops if an object is within the defined safety distance.
- Spins to change direction when encountering obstacles.
- Publishes velocity commands to the wheels driver node.

Safety Parameters:
- SAFETY_DISTANCE: Minimum safe distance to maintain from an obstacle (in meters).
- MIN_VALID_OBSTACLE & MAX_VALID_OBSTACLE: Valid sensor reading bounds to filter out noise.

ROS Topics:
- Subscriber:  /<VEHICLE_NAME>/front_center_tof_driver_node/range  (sensor_msgs/Range)
- Publisher:   /<VEHICLE_NAME>/wheels_driver_node/wheels_cmd        (duckietown_msgs/WheelsCmdStamped)
'''


import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelsCmdStamped
from sensor_msgs.msg import Range

# Safety settings
SAFETY_DISTANCE = 0.2
MIN_VALID_OBSTACLE = 0.00
MAX_VALID_OBSTACLE = 1.19

class WheelControlNode(DTROS):
    def __init__(self, node_name):
        super(WheelControlNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)

        vehicle_name = os.environ['VEHICLE_NAME']
        wheels_topic = f"/{vehicle_name}/wheels_driver_node/wheels_cmd"
        tof_topic = f"/{vehicle_name}/front_center_tof_driver_node/range"

        self._publisher = rospy.Publisher(wheels_topic, WheelsCmdStamped, queue_size=1)

        rospy.Subscriber(tof_topic, Range, self.tof_callback, queue_size=1)

    def tof_callback(self, msg):
        # Ignore invalid readings
        if msg.range < msg.min_range or msg.range > msg.max_range:
            return

        distance = msg.range
        rospy.loginfo_throttle(0.1, f"Distance: {distance:.3f} m")

        if self.safe_to_move(distance):
            # Move forward
            self.send_wheel_cmd(0.3, 0.3)
        else:
            self.send_wheel_cmd(0.0, 0.0)
            rospy.sleep(0.8)


            rospy.logwarn(f"Obstacle at {distance:.3f} m! Spinning.")
            # Spin in place 
            self.send_wheel_cmd(0.4, -0.2)
            rospy.sleep(0.35)
            # Resume forward
            self.send_wheel_cmd(0.3, 0.3)

    def safe_to_move(self, distance):
        if distance < MIN_VALID_OBSTACLE or distance > MAX_VALID_OBSTACLE:
            return True
        return distance > SAFETY_DISTANCE

    def send_wheel_cmd(self, vel_left, vel_right):
        msg = WheelsCmdStamped(vel_left=vel_left, vel_right=vel_right)
        self._publisher.publish(msg)

    def on_shutdown(self):
        self.send_wheel_cmd(0.0, 0.0)

if __name__ == '__main__':
    node = WheelControlNode(node_name='wheel_control_node')
    rospy.spin()
