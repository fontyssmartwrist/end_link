#!/usr/bin/env python

import rospy
from dynamixel_workbench_msgs.srv import DynamixelCommand

def call_dymanixel_service(setpoint):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:
        dyna_srv = rospy.ServiceProxy('dynamixel_workbench/dynamixel_command', DynamixelCommand)
        resp = dyna_srv('', 1, 'Goal_Position', setpoint)
        print resp
        return resp.comm_result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == '__main__':
    try:
        call_dymanixel_service(0)
        rospy.sleep(1)
        call_dymanixel_service(4095)
    except rospy.ROSInterruptException:
        pass
