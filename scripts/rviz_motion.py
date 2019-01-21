#!/usr/bin/env python

import rospy
from std_msgs.msg import Header
from human_motion.msg import Skeleto
import tf
import sys

import copy
import numpy as np

sys.path.insert(0, 'Animation')
import data_utils
import playAnimation
import viz

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


parent = np.array([0, 1, 2, 3, 4, 5, 1, 7, 8, 9,10, 1,12,13,14,15,13,
                17,18,19,20,21,20,23,13,25,26,27,28,29,28,31])-1

offset = np.array(
    [0.000000,0.000000,0.000000,
    -132.948591,0.000000,0.000000,
    0.000000,-442.894612,0.000000,
    0.000000,-454.206447,0.000000,
    0.000000,0.000000,162.767078,
    0.000000,0.000000,74.999437,
    132.948826,0.000000,0.000000,
    0.000000,-442.894413,0.000000,
    0.000000,-454.206590,0.000000,
    0.000000,0.000000,162.767426,
    0.000000,0.000000,74.999948,
    0.000000,0.100000,0.000000,
    0.000000,233.383263,0.000000,
    0.000000,257.077681,0.000000,
    0.000000,121.134938,0.000000,
    0.000000,115.002227,0.000000,
    0.000000,257.077681,0.000000,
    0.000000,151.034226,0.000000,
    0.000000,278.882773,0.000000,
    0.000000,251.733451,0.000000,
    0.000000,0.000000,0.000000,
    0.000000,0.000000,99.999627,
    0.000000,100.000188,0.000000,
    0.000000,0.000000,0.000000,
    0.000000,257.077681,0.000000,
    0.000000,151.031437,0.000000,
    0.000000,278.892924,0.000000,
    0.000000,251.728680,0.000000,
    0.000000,0.000000,0.000000,
    0.000000,0.000000,99.999888,
    0.000000,137.499922,0.000000,
    0.000000,0.000000,0.000000])
offset = offset.reshape(-1,3)

expmapInd = np.split(np.arange(4,100)-1,32)

g_tf_prefix = ''

def motion_visualize_callback(data):

    rospy.loginfo('%s: %s' % (data.header.seq, data.header.stamp))

    skeleto = data.skeleto
    angles = np.array(skeleto)

    assert len(angles) == 99

    # Structure that indicates parents for each joint
    njoints = 32

    stamp = data.header.stamp
    rate = rospy.Rate(1000)
    br = tf.TransformBroadcaster()
    while rospy.get_rostime() < stamp:
        rate.sleep()
    for i in range(njoints):
        tran = offset[i]
        rot = np.eye(3)
        if (i > 0):
            rm = np.eye(4)
            rot = data_utils.expmap2rotmat(angles[expmapInd[i]])
            rm[0:3, 0:3] = np.linalg.inv(rot)
            quat = tf.transformations.quaternion_from_matrix(rm)
            br.sendTransform(tran / 1000, quat, stamp, '%sj%s' % (g_tf_prefix, i), '%sj%s' % (g_tf_prefix, parent[i]))
        else:
            quat = tf.transformations.quaternion_from_euler(np.pi/2, 0, 0)
            br.sendTransform(tran / 1000, quat, stamp, '%sj%s' % (g_tf_prefix, i), 'skeleto')

def main():
    global g_tf_prefix
    rospy.init_node('motion_tf_broadcaster', anonymous=True)
    g_tf_prefix = rospy.get_param('tf_prefix', g_tf_prefix)
    print('tf_prefix: ', g_tf_prefix)
    rospy.Subscriber('motion', Skeleto, motion_visualize_callback, queue_size=100)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass