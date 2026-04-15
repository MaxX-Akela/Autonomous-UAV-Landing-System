#!/usr/bin/env python3
import rospy
from clover import srv
from std_srvs.srv import Trigger
from aruco_pose.msg import MarkerArray
import math
from clover.srv import SetLEDEffect

rospy.init_node('landing_node')

ARUCO_ID = 102

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def markers_callback(msg):
    global detect
    for marker in msg.markers:

        if marker.id == ARUCO_ID:
            detect = True

rospy.Subscriber('aruco_detect/markers', MarkerArray, markers_callback)

while get_telemetry().armed:

    if detect:

        telemetry = get_telemetry(frame_id=f"aruco_{ARUCO_ID}")

        print(f"Вижу платформу, расстояние: X: {telemetry.x:3f}, Y: {telemetry.y:3f}")
        rospy.sleep(1)

rospy.spin()