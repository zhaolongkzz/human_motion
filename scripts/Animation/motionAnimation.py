# -*- coding:utf-8 -*-
# !/usr/bin/python2.7

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import math
import os
import random
import sys
import time
import h5py

import subprocess as sbp
import numpy as np
from six.moves import xrange # pylint: disable=redefined-builtin
import tensorflow as tf
# import data_utils
# import ipdb

def readFile(path):
    gtsData = []
    predsData = []
    errorData = []

    # get the data of gts
    for i in xrange(8):
        fileName_gts = "ground_truth_forecast_N_{0}".format(i)
        fr_gts = open(r'{0}/{1}'.format(path, fileName_gts), 'rb')
        for line in fr_gts.readlines():
            lineArr0 = line.strip().split(',')
            # print(lineArr0)
            for j in xrange(99):
                add = float(lineArr0[j])
                gtsData.append(add)
    gts = np.array([gtsData])
    gts = gts.reshape(8, 100, 99)
    fr_gts.close()
    # print(gts)

    # get the data of preds
    for i in xrange(8):
        fileName_preds = "forecast_N_{0}".format(i)
        fr_preds = open(r'{0}/{1}'.format(path, fileName_preds), 'rb')
        for line in fr_preds.readlines():
            lineArr1 = line.strip().split(',')
            # print(lineArr1)
            for j in xrange(99):
                add = float(lineArr1[j])
                predsData.append(add)
    preds = np.array([predsData])
    preds = preds.reshape(8, 100, 99)
    fr_preds.close()
    print(type(preds))
    # print(preds[2][2][3]) is the same as print(preds[2, 2, 3])

    mean_errors = 0
    try:
        with open(r'{0}/mean_error'.format(path), 'rb') as f:
            for i in f.readlines():
                ii = i.strip().split(',')
                errorData.append(ii[0])

        mean_errors = np.array([errorData])
        mean_errors = mean_errors.reshape(1, 100, 1)
        f.close()
        # print(mean_errors[:, :])
    except:
        pass
    return gts, preds


def saveFile(model, action, gts_expmap, preds_expmap):
    # Clean and create a new h5 file of samples
    SAMPLES_FNAME = 'Motion/{0}_{1}.h5'.format(model, action)
    try:
        os.remove(SAMPLES_FNAME)
    except OSError:
        pass

    # Save the samples
    with h5py.File(SAMPLES_FNAME, 'a') as hf:
        for i in np.arange(8):
            # Save conditioning ground truth
            node_name = 'expmap/gts/{1}_{0}'.format(i, action)
            hf.create_dataset(node_name, data=gts_expmap[i, :, :])
            # Save prediction
            node_name = 'expmap/preds/{1}_{0}'.format(i, action)
            hf.create_dataset(node_name, data=preds_expmap[i, :, :])

    # with h5py.File(SAMPLES_FNAME, 'a') as hf:
    #     node_name = 'mean_{0}_error'.format(action)
    #     hf.create_dataset(node_name, data=mean_mean_errors)

    # # Compute and save the errors here
    # mean_errors = np.zeros((len(preds_expmap), preds_expmap[0].shape[0]))
    #
    # for i in np.arange(24):
    #
    #     eulerchannels_pred = preds_expmap[i]
    #
    #     for j in np.arange(eulerchannels_pred.shape[0]):
    #         for k in np.arange(3, 97, 3):
    #             eulerchannels_pred[j, k:k + 3] = data_utils.rotmat2euler(
    #                 data_utils.expmap2rotmat(eulerchannels_pred[j, k:k + 3]))
    #
    #     eulerchannels_pred[:, 0:6] = 0
    #
    #     # Pick only the dimensions with sufficient standard deviation. Others are ignored.
    #     idx_to_use = np.where(np.std(eulerchannels_pred, 0) > 1e-4)[0]
    #
    #     euc_error = np.power(gts_euler[action][i][:, idx_to_use] - eulerchannels_pred[:, idx_to_use], 2)
    #     euc_error = np.sum(euc_error, 1)
    #     euc_error = np.sqrt(euc_error)
    #     mean_errors[i, :] = euc_error
    #
    # mean_mean_errors = np.mean(mean_errors, 0)
    # print(action)
    # print(','.join(map(str, mean_mean_errors.tolist())))
    #
    # with h5py.File(SAMPLES_FNAME, 'a') as hf:
    #     node_name = 'mean_{0}_error'.format(action)
    #     hf.create_dataset(node_name, data=mean_mean_errors)
    #
    print("finish saving the H5DF file")

def animation(model, action):
    # play the motion on video
    print("Begining to play the animation!")
    print("*******************************")
    params = {}
    params['model'] = model
    params['action'] = action
    args = ['python', 'Animation/playAnimation.py']
    for k in params.keys():
        args.append('--{0}'.format(k))
        if not isinstance(params[k], list):
            args.append(str(params[k]))
        else:
            for x in params[k]:
                args.append(str(x))
    p = sbp.Popen(args)
    p.wait()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--model', type=str, choices=['erd', 'lstm3lr', 'srnn'])
    parser.add_argument('--action', type=str, choices=['walking', 'smoking', 'eating', 'discussion'])
    args = parser.parse_args()

    path = "Pre-trained/{0}_{1}".format(args.model, args.action)

    # readFile1(path)
    # gts, preds, mean_errors = readFile(path)
    gts, preds = readFile(path)
    # saveFile(args.model, args.action, gts, preds, mean_errors)
    saveFile(args.model, args.action, gts, preds)

    animation(args.model, args.action)


if __name__ == "__main__":
    main()
