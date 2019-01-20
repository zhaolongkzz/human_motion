#!/usr/bin/env python2.7

import rospy
import sys
import numpy as np
from six.moves import xrange
from std_msgs.msg import Header
from human_motion.msg import Motion

sys.path.insert(0, 'Animation')

g_model = ''
g_action = ''
g_path = ''

gtsData = []
predsData = []
num_forecast_examples = 24

def human_motion_publish(g_model_tem, g_action_tem):
    rospy.init_node('motion_publisher')
    publ = rospy.Publisher('motion_data', Motion, queue_size=50)
    rate = rospy.Rate(1/0.1)
    g_path = 'Pre-trained/{0}_{1}/'.format(g_model_tem, g_action_tem)
    
    header = Header()
    header.frame_id = 'main'
    motion = Motion()
    motion.header = header
    seq = 0
    
    while not rospy.is_shutdown():
        rospy.loginfo(seq)
        motion.header.seq = seq
        motion.header.stamp = rospy.get_rostime()
        g_motion = g_model_tem + ',' + g_action_tem
        motion.motion = g_motion
        rospy.loginfo(g_model_tem)
        rospy.loginfo(g_action_tem)
        publ.publish(motion)

        seq += 1
        rospy.loginfo("end reading the data")
        rate.sleep()


def usage():
    print "enter two arguments (x to quit):"
    return "%s [model: srnn] [path of predicted data: smoking]" % sys.argv[0]


def main():
    if len(sys.argv) > 2:
        g_model = sys.argv[1]
        g_action = sys.argv[2]
    else:
        print usage()
        sys.exit(1)
    print "Model is based on %s" % g_model
    print "The checkpoint's path is %s" % g_action
    human_motion_publish(g_model, g_action)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass