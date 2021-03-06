# -*- coding:utf-8 -*-
# !/usr/bin/python2.7

import sys
import numpy as np
import argparse
import theano
import os
from theano import tensor as T
from neuralmodels.utils import permute
from neuralmodels.loadcheckpoint import *
from neuralmodels.costs import softmax_loss, euclidean_loss
from neuralmodels.models import *
from neuralmodels.predictions import OutputMaxProb, OutputSampleFromDiscrete
from neuralmodels.layers import *
from neuralmodels.updates import Adagrad,RMSprop,Momentum,Adadelta
import cPickle
import pdb
import socket as soc
import copy
import readCRFgraph as graph
import time
from unNormalizeData import unNormalizeData
from convertToSingleVec import convertToSingleVec

global rng
rng = np.random.RandomState(1234567890)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--action',type=str,default='action')
parser.add_argument('--checkpoint',type=str,default='checkpoint')
parser.add_argument('--forecast',type=str,default='malik')
parser.add_argument('--iteration',type=str,default='pik')
parser.add_argument('--motion_prefix',type=int,default=50)
parser.add_argument('--motion_suffix',type=int,default=100)
parser.add_argument('--temporal_features',type=int,default=0)
parser.add_argument('--full_skeleton',type=int,default=1)
parser.add_argument('--dataset_prefix',type=str,default='')
parser.add_argument('--train_for',type=str,default='final')
parser.add_argument('--drop_features',type=int,default=0)
parser.add_argument('--drop_id',type=int,default=9)
args = parser.parse_args()


'''Loads H3.6m dataset'''
print 'Loading H3.6m'
sys.path.insert(0,'Prediction/DataProcess')
import processdata as poseDataset
poseDataset.T = 150
poseDataset.delta_shift = 100
poseDataset.num_forecast_examples = 24
poseDataset.motion_prefix = args.motion_prefix
poseDataset.motion_suffix = args.motion_suffix
poseDataset.temporal_features = args.temporal_features
poseDataset.full_skeleton = args.full_skeleton
poseDataset.dataset_prefix = args.dataset_prefix
poseDataset.crf_file = './Prediction/DataProcess/crf'
poseDataset.train_for = args.train_for
poseDataset.drop_features = args.drop_features
poseDataset.drop_id = [args.drop_id]
poseDataset.runall()
print '**** H3.6m Loaded ****'

def unnormalize_data(data_tnd, data_mean, data_std, ignore_dim):
    [T1, N1, D1] = data_tnd.shape
    data_tnd_orig = np.zeros((T1, N1, data_mean.shape[0]))
    for i in range(N1):
        data_tnd_orig[:, i, :] = np.float32(unNormalizeData(data_tnd[:, i, :], data_mean, data_std, ignore_dim))
    return data_tnd_orig


iteration = args.iteration
new_idx = poseDataset.new_idx
featureRange = poseDataset.nodeFeaturesRanges
path = args.checkpoint
if not os.path.exists(path):
    print 'Checkpoint path does not exist. Exiting!!'
    sys.exit()

crf_file = './Prediction/DataProcess/crf'


def model():
    if args.forecast == 'srnn':
        path_to_checkpoint = '{0}checkpoint.{1}'.format(path, args.iteration)
        print "Using checkpoint at: ",path_to_checkpoint
        if os.path.exists(path_to_checkpoint):
            [nodeNames,
            nodeList,
            nodeFeatureLength,
            nodeConnections,
            edgeList,
            edgeListComplete,
            edgeFeatures,
            nodeToEdgeConnections,
            trX,trY,
            trX_validation,
            trY_validation,
            trX_forecasting,
            trY_forecasting,
            trX_forecast_nodeFeatures] = graph.readCRFgraph(poseDataset)

            print trX_forecast_nodeFeatures.keys()
            print 'Loading the model (this takes long, can take upto 25 minutes)'
            model = loadDRA(path_to_checkpoint)
            print model
            print 'Loaded S-RNN from ', path_to_checkpoint
            t0 = time.time()
            save_full = True

            trY_forecasting = model.convertToSingleVec(trY_forecasting,new_idx,featureRange)  # 8x100x54
            print trY_forecasting.shape
            trX_forecast_nodeFeatures_ = model.convertToSingleVec(trX_forecast_nodeFeatures, new_idx, featureRange)
            # normalize_data_for_srnn()

            trY_forecasting_tem = trY_forecasting
            trX_forecasting_tem = trX_forecast_nodeFeatures_

            filterList = [10, 11,
                        16, 17, 18, 19, 20,
                        25, 26,
                        31, 32, 33, 34, 35,
                        48, 49, 50,
                        58, 59,
                        63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                        82, 83, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98]

            for i in filterList:
                trY_forecasting_tem = np.insert(trY_forecasting_tem, i, 0, axis=2)
                trX_forecasting_tem = np.insert(trX_forecasting_tem, i, 0, axis=2)
            trY_forecasting_full = trY_forecasting_tem
            trX_forecasting_full = trX_forecasting_tem
            print(trY_forecasting_full.shape)
            print(trX_forecasting_full.shape)

            fname = 'ground_truth_forecast'
            if(save_full):
                # unnormalize_data()
                trY_forecasting_full_orig = unnormalize_data(trY_forecasting_full, poseDataset.data_mean, poseDataset.data_std, [])
                model.saveForecastedMotion(trY_forecasting_full_orig, path, fname)
            else:
                model.saveForecastedMotion(trY_forecasting, path, fname)

            fname = 'motionprefix'
            if(save_full):
                trX_forecast_nodeFeatures_full_orig = unnormalize_data(trX_forecasting_full, poseDataset.data_mean, poseDataset.data_std, [])
                model.saveForecastedMotion(trX_forecast_nodeFeatures_full_orig, path, fname)
            else:
                model.saveForecastedMotion(trX_forecasting, path, fname)

            forecasted_motion = model.predict_sequence(trX_forecasting, trX_forecast_nodeFeatures,sequence_length=trY_forecasting.shape[0],poseDataset=poseDataset,graph=graph)
            forecasted_motion = model.convertToSingleVec(forecasted_motion, new_idx, featureRange)
            fname = 'forecast'
            if(save_full):
                filter_list = []
                for x in range(trY_forecasting_full.shape[2]):
                    if x in  filterList:
                        continue
                    filter_list.append(x)
                forecasted_motion_full = trY_forecasting_full
                forecasted_motion_full[:, :, filter_list] = forecasted_motion
                # unnormalize_data()
                forecasted_motion_full_orig = unnormalize_data(forecasted_motion_full, poseDataset.data_mean, poseDataset.data_std, [])
                model.saveForecastedMotion(forecasted_motion_full_orig, path, fname)
            else:
                model.saveForecastedMotion(forecasted_motion, path, fname)

            skel_err = np.mean(np.sqrt(np.sum(np.square((forecasted_motion - trY_forecasting)),axis=2)),axis=1)
            err_per_dof = skel_err / trY_forecasting.shape[2]
            fname = 'forecast_error'
            model.saveForecastError(skel_err,err_per_dof,path,fname)
            t1 = time.time()
            print t1-t0
            del model
        else:
            print "the path is not found!!!"


    elif args.forecast == 'lstm3lr' or args.forecast == 'erd':
        path_to_checkpoint = '{0}checkpoint.{1}'.format(path, args.iteration)
        if os.path.exists(path_to_checkpoint):
            print "Loading the model {0} (this may take sometime)".format(args.forecast)
            model = load(path_to_checkpoint)
            print 'Loaded the model from ',path_to_checkpoint

            save_full = True
            # more colum than srnn1 8x100x99
            trX_forecasting_full, trY_forecasting_full = poseDataset.getMalikTrajectoryForecastingFull()

            # same mat as srnn1 8x100x54
            trX_forecasting, trY_forecasting = poseDataset.getMalikTrajectoryForecasting()

            fname = 'ground_truth_forecast'
            if(save_full):
                # unnormalize_data()
                # print(poseDataset.dimensions_to_ignore)
                trY_forecasting_full_orig = unnormalize_data(trY_forecasting_full, poseDataset.data_mean,
                                                            poseDataset.data_std, [])
                model.saveForecastedMotion(trY_forecasting_full_orig, path, fname)
            else:
                model.saveForecastedMotion(trY_forecasting, path, fname)

            fname = 'motionprefix'
            if(save_full):
                # unnormalize_data()
                trX_forecasting_full_orig = unnormalize_data(trX_forecasting_full, poseDataset.data_mean,
                                                            poseDataset.data_std, [])
                model.saveForecastedMotion(trX_forecasting_full_orig, path, fname)
            else:
                model.saveForecastedMotion(trX_forecasting, path, fname)

            forecasted_motion = model.predict_sequence(trX_forecasting,sequence_length=trY_forecasting.shape[0])
            fname = 'forecast'
            if(save_full):
                filter_list = []
                for x in range(trY_forecasting_full.shape[2]):
                    if x in poseDataset.dimensions_to_ignore:
                        continue
                    filter_list.append(x)
                forecasted_motion_full = trY_forecasting_full
                forecasted_motion_full[:, :, filter_list] = forecasted_motion
                # unnormalize_data()
                forecasted_motion_full_orig = unnormalize_data(forecasted_motion_full, poseDataset.data_mean,
                                                            poseDataset.data_std, [])
                model.saveForecastedMotion(forecasted_motion_full_orig, path, fname)
            else:
                model.saveForecastedMotion(forecasted_motion,path,fname)

            skel_err = np.mean(np.sqrt(np.sum(np.square((forecasted_motion - trY_forecasting)),axis=2)),axis=1)
            err_per_dof = skel_err / trY_forecasting.shape[2]
            fname = 'forecast_error'
            model.saveForecastError(skel_err,err_per_dof,path,fname)

            # print(trX_forecasting_full.shape)
            # print(trX_forecasting.shape)

            del model
        else:
            print "the path is not found!!!"


    elif args.forecast == 'dracell':
        path_to_checkpoint = '{0}checkpoint.{1}'.format(path, args.iteration)
        if os.path.exists(path_to_checkpoint):
            [nodeNames,nodeList,nodeFeatureLength,nodeConnections,edgeList,edgeListComplete,edgeFeatures,nodeToEdgeConnections,trX,trY,trX_validation,trY_validation,trX_forecasting,trY_forecasting,trX_forecast_nodeFeatures] = graph.readCRFgraph(poseDataset,noise=0.7,forecast_on_noisy_features=True)
            print trX_forecast_nodeFeatures.keys()
            print 'Loading the model'
            model = loadDRA(path_to_checkpoint)
            print 'Loaded DRA: ',path_to_checkpoint
            t0 = time.time()
            trY_forecasting = model.convertToSingleVec(trY_forecasting,new_idx,featureRange)

            trX_forecast_nodeFeatures_ = model.convertToSingleVec(trX_forecast_nodeFeatures,new_idx,featureRange)
            fname = 'motionprefixlong'
            model.saveForecastedMotion(trX_forecast_nodeFeatures_,path,fname)

            cellstate = model.predict_cell(trX_forecasting,trX_forecast_nodeFeatures,sequence_length=trY_forecasting.shape[0],poseDataset=poseDataset,graph=graph)
            fname = 'forecast_celllong_{0}'.format(args.iteration)
            model.saveCellState(cellstate,path,fname)
            t1 = time.time()
            del model

    print 'ending program'


if __name__ == "__main__":
    model()
    
