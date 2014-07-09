#!/usr/bin/env python
import roslib
#roslib.load_manifest('')
import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates

from std_msgs.msg import String

import sys, select, termios, tty
from math import atan2, pi
from time import sleep

import grid

class SearchAndRescue ():
    def __init__(self):
        self.x = 0

	self.turtlebot_position = None
	self.last_turtlebot_position = None
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
        rospy.init_node('irll_search_rescue')
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.saveModelStates)
        rospy.Subscriber('/mission/status', String, self.status)	
	self.status = 1

        rospy.spin ()

    def status(self, status):
	if status == "GO":
	   self.status = 1
	else:
	   self.status = 0	

    def publishDrive (self, twist):
        self.pub.publish(twist)

        self.x += 0.1
        if self.x > 1.5: self.x = 0.0
    
    def printModelStates (self):
        try:
            print "Cylinder:"
            print "Position:"
            print self.cylinder_position.x
            print self.cylinder_position.y
            print self.cylinder_position.z
            print "Orientation:"
            print self.cylinder_orientation.x
            print self.cylinder_orientation.y
            print self.cylinder_orientation.z
            print self.cylinder_orientation.w
            print "Base:"
            print "Position:"
            print self.turtlebot_position.x
            print self.turtlebot_position.y
            print self.turtlebot_position.z
            print "Orientation:"
            print self.turtlebot_orientation.x
            print self.turtlebot_orientation.y
            print self.turtlebot_orientation.z
            print self.turtlebot_orientation.w
            print "--------------------"
        except:
            pass

    def saveModelStates (self, model_states):
        m = model_states.name.index ("mobile_base")
        c = model_states.name.index ("unit_cylinder_2")
	
	if self.turtlebot_position != None:
	    self.last_turtlebot_position = self.turtlebot_position
        self.cylinder_position = model_states.pose[c].position
        self.turtlebot_position = model_states.pose[m].position
        self.cylinder_orientation = model_states.pose[c].orientation
        self.turtlebot_orientation = model_states.pose[m].orientation

        ## Adjustments
        #self.turtlebot_orientation.x = -(self.turtlebot_orientation.x * 3.14)
        #self.turtlebot_orientation.y = -(self.turtlebot_orientation.y * 3.14)
        #self.turtlebot_orientation.z = -(self.turtlebot_orientation.z * 3.14)

        #self.cylinder_orientation.x = (self.cylinder_orientation.x * 3.14)
        #self.cylinder_orientation.y = (self.cylinder_orientation.y * 3.14)
        #self.cylinder_orientation.z = (self.cylinder_orientation.z * 3.14)

        #self.printModelStates ()
        #self.determineOrientation ()
	if self.status:
            self.test ()
        #self.touchCylinder ()

    def test (self):
        twist = Twist ()
        print self.turtlebot_orientation
        print
	
	if abs(self.turtlebot_position.x - self.cylinder_position.x) >= .5 or abs(self.turtlebot_position.y - self.cylinder_position.y) >= .5:
	  if abs(self.turtlebot_position.x - self.cylinder_position.x) >= abs(self.last_turtlebot_position.x - self.cylinder_position.x) or abs(self.turtlebot_position.y - self.cylinder_position.y) >= abs(self.last_turtlebot_position.y - self.cylinder_position.y):
 	      twist.linear.x = .2
              twist.angular.z = .7	
	  else:
	      twist.angular.z = 0
	      twist.linear.x = .2

          self.publishDrive (twist)

	elif abs(self.turtlebot_position.x - 0) >= .5 or abs(self.turtlebot_position.y - 0) >= .5:
	  if abs(self.turtlebot_position.x - 0) >= abs(self.last_turtlebot_position.x - 0) or abs(self.turtlebot_position.y - 0) >= abs(self.last_turtlebot_position.y - 0):
 	      twist.linear.x = .2
              twist.angular.z = .7	
	  else:
	      twist.angular.z = 0
	      twist.linear.x = .2

          self.publishDrive (twist)


    def touchCylinder (self):
        twist = Twist ()

        c_o = atan2 (self.cylinder_position.y, self.cylinder_position.x)

        print self.turtlebot_orientation.z - c_o
        print
        if (self.turtlebot_orientation.z - c_o) > 0.2: twist.angular.z = 0.2
        elif (self.turtlebot_orientation.z - c_o) < -0.2: twist.angular.z = -0.2
        else: twist.linear.x = 1.0

        self.publishDrive (twist)

    def determineOrientation (self):
        twist = Twist ()

        c_o = atan2 (self.cylinder_position.y, self.cylinder_position.x)
        t_o = atan2 (self.turtlebot_position.y, self.turtlebot_position.x)

        print "c_o:",
        print c_o
        print "t_o:",
        print t_o
        #print "twist.angular.z",
        #print twist.angular.z
        print

        self.publishDrive (twist)

class Discrete_Movement ():
    def __init__(self):
        rospy.init_node('discrete_movement')
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.saveModelStates)
	self.max_speed = 3.0
	self.cell_spacing = 3.0

    def saveModelStates (self, model_states):
        m = model_states.name.index ("mobile_base")
        c = model_states.name.index ("unit_cylinder_2")
	
        self.cylinder_position = model_states.pose[c].position
        self.turtlebot_position = model_states.pose[m].position
        self.cylinder_orientation = model_states.pose[c].orientation
        self.turtlebot_orientation = model_states.pose[m].orientation

    def move_forward(self, spaces):
	#Move in a quadratic motion
	#As distance increases speed increases
	#until you reach half way
	distance = self.cell_spacing * spaces
	destination1 = self.pos_x + distance
	destination2 = self.pos_y + distance
	while not self.pos_x != destination1 or not self.pos_y != destination:
	    speed = -(self.pos_x - .5(distance))**2
	


if __name__=="__main__":
#    sar = SearchAndRescue ()
     print "hi"