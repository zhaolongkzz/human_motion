#!/usr/bin/env python2.7

import rospy
import sys
import numpy as np
from std_msgs.msg import Header
from human_motion.msg import Motion

sys.path.insert(0, 'Animation')
from motionAnimation import readFile, saveFile, animation

g_model = ''
g_checkpoint = ''


def AnimaCallback(data):
    rospy.loginfo('%s: %s' % (data.header.seq, data.header.stamp))
    g = data.motion
    g_motion = g.strip().split(',')
    g_model = g_motion[0]
    g_action = g_motion[1]
    g_path = 'Pre-trained/{0}_{1}/'.format(g_model, g_action)
    
    print "receive the model: {0} ".format(g_model)
    print "receive the action: {0} ".format(g_action)

    g_gts, g_preds = readFile(g_path)
    saveFile(g_model, g_action, g_gts, g_preds)
    animation(g_model, g_action)
    rate = rospy.Rate(100)
    while rospy.get_rostime() < data.header.stamp:
        rate.sleep()
    

def human_motion_animation():
    rospy.init_node('motion_animation', anonymous=True)
    rospy.Subscriber("motion_data", Motion, AnimaCallback, queue_size=100)

    rospy.spin()


if __name__ == '__main__':
    try:
        human_motion_animation()
    except rospy.ROSInterruptException:
        pass