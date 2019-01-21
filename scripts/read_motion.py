#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import Header
from human_motion.msg import Skeleto

sys.path.insert(0, 'Animation')
import data_utils

g_motion_dataset_path = ''

def motion_publisher():
    global g_motion_dataset_path
    rospy.init_node('motion_publisher')
    pub = rospy.Publisher('motion_skeleto', Skeleto, queue_size=rospy.get_param('prefix_sequence_length', 50))
    rate = rospy.Rate(1 / rospy.get_param('frames_interval', 0.05))
    g_motion_dataset_path = rospy.get_param('motion_dataset_path', g_motion_dataset_path)

    if len(g_motion_dataset_path) == 0:
        rospy.loginfo('invalid motion_dataset_path!')
        return

    motion_sequece = data_utils.readCSVasFloat(g_motion_dataset_path)
    motion_sequece = motion_sequece[20::2, :]
    header = Header()
    header.frame_id = 'main'
    skeleto = Skeleto()
    skeleto.header = header
    seq = 0
    while not rospy.is_shutdown() and seq < motion_sequece.shape[0]:
        rospy.loginfo(seq)
        skeleto.header.seq = seq
        skeleto.header.stamp = rospy.get_rostime()
        skeleto.skeleto = motion_sequece[seq]
        pub.publish(skeleto)

        seq += 1
        rate.sleep()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        g_motion_dataset_path = sys.argv[1]
    try:
        motion_publisher()
    except rospy.ROSInterruptException:
        pass
