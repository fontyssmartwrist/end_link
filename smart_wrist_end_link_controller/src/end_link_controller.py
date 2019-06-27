#!/usr/bin/env python

import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from dynamixel_workbench_msgs.srv import DynamixelCommand
from std_msgs.msg import Float64
import math

class EndLinkController():
    def __init__(self):
        self.goal_sub = rospy.Subscriber("~goal", Float64, self.goal_callback)
        rospy.loginfo("Waiting for dynamixel Service")
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
	rospy.loginfo("Found service")
        self.dynamixel_srv = rospy.ServiceProxy(
            '/dynamixel_workbench/dynamixel_command', DynamixelCommand)

    def goal_callback(self, goal_angle_rad):

        if goal_angle_rad.data >= -math.pi and goal_angle_rad.data <= math.pi:
            rospy.loginfo(
                "Setting end_link to goal position {}".format(goal_angle_rad.data))
            self.dynamixel_srv('', 1, 'Goal_Position',
                               self.angle_to_position(goal_angle_rad.data))
        else:
            rospy.logerr("Goal out of range: -pi to +pi")

    def angle_to_position(self, angle_rad):
        setpoint = (angle_rad + math.pi) * (4095 / (2*math.pi))
	rospy.loginfo("setpoint {}".format(setpoint))

        return setpoint


if __name__ == '__main__':
    try:
        rospy.init_node('end_link_controller')
        controller = EndLinkController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
