#!/usr/bin/env python2.7

import rospy
import sys
import numpy as np
from std_msgs.msg import String
from human_motion.msg import Motion

sys.path.insert(0, 'Prediction')
from generateMotionForecast import predicts

g_model = ''
g_action = ''
g_checkpoint = ''
g_procedure = ''
g_motion_prefix = 50
g_motion_suffix = 100


def human_motion_preds(model, action):
    g_checkpoint = 'Pre-trained/{0}_{1}'.format(g_model, g_action)
    rospy.init_node('prediction', anonymous=True)
    pub = rospy.Publisher('motionPreds', String, queue_size=50)
    rate = rospy.Rate(10)
    
    begin_str = "Begining to predict the motion %s" % rospy.get_time()
    rospy.loginfo(begin_str)
    pub.publish(begin_str)
    predicts(model, action)
    rospy.sleep()


def usage():
    print "enter two arguments (x to quit):"
    return "%s [model] [path of checkpoint]" % sys.argv[0]


def main():
    if len(sys.argv) > 2:
        g_model = sys.argv[1]
        g_action = sys.argv[2]
    else:
        print usage()
        sys.exit(1)
    
    print "Model is based on %s" % g_model
    print "The action is %s" % g_action
    rospy.loginfo("procedure only for 'preds' or 'publ'......")
    human_motion_preds(g_model, g_action)
    rospy.loginfo('Input wrong arument of procedure!')


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass