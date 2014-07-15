#!/usr/bin/env python

import roslib
#roslib.load_manifest('')
import rospy

from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
import transformations as tf

import sys, select, termios, tty
from math import atan2, pi, acos
from time import sleep

class TurtlebotDiscreteRotation:
    def __init__(self):
        rospy.init_node('turtlebot_discrete_rotation')
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.saveModelStates)

        self.desired_orientation = 0.0

        self.success = 0

        self.P = 0.4

        self.yaw = 0.0

    def run (self):
        rospy.spin ()

    def publishDrive (self, twist):
        self.pub.publish(twist)

    def rotate90Left (self):
        if self.desired_orientation == -pi: self.desired_orientation = -pi/2
        elif self.desired_orientation == -pi/2: self.desired_orientation = 0.0
        elif self.desired_orientation == 0.0: self.desired_orientation = pi/2
        elif self.desired_orientation == pi/2: self.desired_orientation = -pi

    def rotate90Right (self):
        if self.desired_orientation == -pi: self.desired_orientation = pi/2
        elif self.desired_orientation == pi/2: self.desired_orientation = 0.0
        elif self.desired_orientation == 0.0: self.desired_orientation = -pi/2
        elif self.desired_orientation == -pi/2: self.desired_orientation = -pi

    def checkRotation (self):
        print "Desired Orientation: ",
        print self.desired_orientation
        error = self.desired_orientation - self.yaw 
        print "Error: ",
        print abs (error)

        twist = Twist ()

        print "Success: ",
        print self.success
        if abs (error) > 0.2:
            print "Correcting!"
            twist.angular.z = self.P * error
            self.publishDrive (twist)
            self.success = 0
        else:
            self.success = 1

    def printModelStates (self):
        #print "Position:"
        #print self.turtlebot_position.x
        #print self.turtlebot_position.y
        #print self.turtlebot_position.z
        #print "Orientation:"
        #print self.turtlebot_orientation.x
        #print self.turtlebot_orientation.y
        #print self.turtlebot_orientation.z
        #print self.turtlebot_orientation.w
        print "Yaw: ",
        print self.yaw
        print "Compass: ",
        print self.compass
        print "--------------------"

    def saveModelStates (self, model_states):
        m = model_states.name.index ("mobile_base")

        self.turtlebot_position = model_states.pose[m].position
        self.turtlebot_orientation = model_states.pose[m].orientation

        self.euler_angles = tf.euler_from_quaternion([self.turtlebot_orientation.w, self.turtlebot_orientation.x, self.turtlebot_orientation.y, self.turtlebot_orientation.z])

        self.yaw = pi - (self.euler_angles[0] + pi)
        self.compass = (self.yaw - pi/4) // (pi / 2)
 
        if self.compass == -1.0:
            self.compass = 3.0

        self.checkRotation ()
        self.printModelStates ()

    def getDirection (self):
        return self.compass

'''
turtlebot = TurtlebotDiscreteRotation ()

while True:
    try:
        turtlebot.rotate90Right ()
        sleep (10)
        turtlebot.rotate90Right ()
        sleep (10)
        turtlebot.rotate90Left ()
        sleep (10)
    except KeyboardInterrupt:
        sys.exit ()
'''