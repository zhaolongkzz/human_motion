#!/usr/bin/env python2.7

import rospy
import sys
import tf
import h5py
import numpy as np
from std_msgs.msg import Header
from human_motion.msg import Motion

sys.path.insert(0, 'Animation')
from motionAnimation import readFile, saveFile, animation
from playAnimation import _some_variables, fkl, revert_coordinate_space
from data_utils import expmap2rotmat


def RvizCallback(data):
    rospy.loginfo('%s: %s' % (data.header.seq, data.header.stamp))
    g = data.motion
    g_motion = g.strip().split(',')
    g_model = g_motion[0]
    g_action = g_motion[1]
    g_path = 'Pre-trained/{0}_{1}/'.format(g_model, g_action)
    
    print "receive the model: {0} ".format(g_model)
    print "receive the action: {0} ".format(g_action)

    g_gts, g_preds = readFile(g_path)
    # Broadcast tf
    parent, offset, rotInd, expmapInd = _some_variables()
    # numpy implementation
    with h5py.File( 'Motion/{0}_{1}.h5'.format(g_model, g_action), 'r' ) as h5f:
        # expmap_gt = h5f['expmap/gt/walking_0'][:]
        # expmap_pred = h5f['expmap/preds/walking_0'][:]
        expmap_gt = h5f['expmap/gts/{0}_0'.format(g_action)][:]
        expmap_pred = h5f['expmap/preds/{0}_0'.format(g_action)][:]
    nframes_gt, nframes_pred = expmap_gt.shape[0], expmap_pred.shape[0]  # 100x99

    # Put them together and revert the coordinate space
    expmap_all = revert_coordinate_space( np.vstack((expmap_gt, expmap_pred)), np.eye(3), np.zeros(3) )
    expmap_gt   = expmap_all[:nframes_gt,:]
    expmap_pred = expmap_all[nframes_gt:,:]

    # Compute 3d points for each frame
    xyz_gt, xyz_pred = np.zeros((nframes_gt, 96)), np.zeros((nframes_pred, 96))
    for i in range( nframes_gt ):
        xyz_gt[i,:] = fkl( expmap_gt[i,:], parent, offset, rotInd, expmapInd )
        angles = expmap_gt[i,:]
        assert len(angles) == 99
    for i in range( nframes_pred ):
        xyz_pred[i,:] = fkl( expmap_pred[i,:], parent, offset, rotInd, expmapInd )
        angles = expmap_pred[i,:]
        assert len(angles) == 99

    # Structure that indicates parents for each joint
    njoints   = 32

    stamp = data.header.stamp
    br = tf.TransformBroadcaster()
    while rospy.get_rostime() < stamp:
        rate.sleep()
    for i in range(njoints):
        tran = offset[i]
        rot = np.eye(3)
        if (i > 0):
            rm = np.eye(4)
            rot = expmap2rotmat(angles[expmapInd[i]])
            rm[0:3, 0:3] = np.linalg.inv(rot)
            quat = tf.transformations.quaternion_from_matrix(rm)
            br.sendTransform(tran / 1000, quat, stamp, '%s_%s' % (g_model, i), '%s_%s' % (g_model, parent[i]))
        else:
            quat = tf.transformations.quaternion_from_euler(np.pi/2, 0, 0)
            br.sendTransform(tran / 1000, quat, stamp, '%s_%s' % (g_model, i), 'motion')


def human_motion_Rviz():
    rospy.init_node('motion_Rviz', anonymous=True)
    rospy.Subscriber("motion_data", Motion, RvizCallback, queue_size=100)
    rospy.spin()


if __name__ == '__main__':
    try:
        human_motion_Rviz()
    except rospy.ROSInterruptException:
        pass