# -*- coding:utf-8 -*-
# !/usr/bin/python2.7

import subprocess as sbp
import os
import copy
import socket as soc
from datetime import datetime
import sys


def predicts(model, action):
    supported_model = ['srnn','lstm3lr','erd']
    if model not in supported_model:
        print 'Incorrect model, Supported models: ',supported_model
        return 0

    my_env = os.environ
    # Adding CUDA to path
    my_env['PATH'] += ':/usr/local/cuda/bin'
    my_env['THEANO_FLAGS']='mode=FAST_RUN, device=gpu0, floatX=float32'

    params = {}
    params['forecast'] = model
    params['action'] = action
    params['checkpoint'] = './Pre-trained/{0}_{1}/'.format(model, action)
    params['train_for'] = action

    params['motion_prefix'] = 50
    params['motion_suffix'] = 100
    args = ['python','Prediction/forecastTrajectories.py']
    for k in params.keys():
        args.append('--{0}'.format(k))
        if not isinstance(params[k],list):
            args.append(str(params[k]))
        else:
            for x in params[k]:
                args.append(str(x))
    p=sbp.Popen(args)
    p.wait()


def readPikFile():
    import cPickle
    data = cPickle.load(open(r'../Pre-trained/srnn_smoking/checkpoint.pik'))
    print data  


if __name__ == "__main__":
    # Inputs
    model = sys.argv[1]
    action = sys.argv[2]
    predicts(model, action)
