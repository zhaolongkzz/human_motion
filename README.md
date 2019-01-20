EN | [中文](https://github.com/zhaolongkzz/human_motion/blob/master/README_CN.md)

# Overview of human motion
Structural-RNN for human-motion prediction!

## Summary
Here I provide the code for [CVPR2015 Structural-RNN](https://arxiv.org/pdf/1511.05298.pdf), the original code of author is [here](http://asheshjain.org/srnn/).

The work I have done is reproduce the paper, and make a animation from the result. And making a ROS topic to publish motion data,then a predicter to subscribe the data and predict the next motion from dataset. The code also get a TF animation in Rviz.

Qualitatively, ERD models human motion better than LSTM-3LR. However, in the short-term, it does not mimic the ground-truth as well as LSTM-3LR.

it well handles both short and long term forecasting. And the SRNN exhibit well both in short and long term prediction, the most important is that SRNN can also get well in aperiodic activity all algorithms.

### Main files Location:
- ./scripts/Prediction/generateMotionForecast.py
- ./scripts/Animation/motionAnimation.py

## Prerequisites
- ubuntu16.04
- anaconda3
- ROS-Kinetic

you can create an environment to run them.
```conda create -n srnn python=2.7```
the package you need to install:
- python=2.7
- numpy>=1.8.1
- theano=0.8.2
- matplotlib=2.2.3
- h5py=2.9.0

if you want to train it with GPU here, you should install cuda
- cuda=8.0
- libcudnn6_6.0.21

with the theano, using the package [NeuralModels](https://github.com/asheshjain399/NeuralModels) same as the paper.
use the Model of theano, and install it with:
```python setup.py develop```

## Dataset
**Note:** you can download the mocap dataset from [here](http://www.cs.stanford.edu/people/ashesh/h3.6m.zip), and if you want more raw dataset, you can visit [H3.6m](http://vision.imar.ro/human3.6m/description.php).

And the Pre-trained dataset is in [here](https://drive.google.com/drive/folders/0B7lfjqylzqmMZlI3TUNUUEFQMXc).
(**Provided by the paper's author.**)

## Quickstart

first, here you can git the code from github:
```bash
git clone https://github.com/zhaolongkzz/human_motion.git
unzip human_motion
cd human_motion/scripts
wget http://www.cs.stanford.edu/people/ashesh/h3.6m.zip
unzip h3.6m.zip
rm h3.6m.zip
# download the Pre-trained dataset from Drive to scripts floder
```

**Note:**download the Pre-tarined dataset from google drive, and place them into the scripts floder.(the h3.6m and Pre-train floders is both in scripts floder.)


### With python
```bash
cd scripts
# train your model, it will cost you about 20 min
python Prediction/generateMotionForecast.py srnn smoking
# make a animation, and then it will play it automaticcally
python Animation/motionAnimation.py --model srnn --action smoking
# the result data will save with a h5df file in /Motion floder!
```

### With ROS

Play the animation of the motion!
```bash
cd human_motion/scripts
roscore
# predict the motion, remember to open another terminal
rosrun human_motion motion_predicts.py srnn smoking
# read the file and publish the msg
rosrun human_motion motion_publisher.py srnn smoking
# get the data, and play the animation
rosrun human_motion motion_animation.py
```

## Structure
The floder here is human\_motion.you'd better place the dataset as below.

<p align="center">
  <img src="https://github.com/zhaolongkzz/human_motion/blob/master/images/Tree.png"><br><br>
</p>

S-RNN architecture from the factor graph representation of the st-graph. The factors in the st-graph operate in a temporal manner, where at each time step the factors observe (node & edge) features and perform some computation on those features. In S-RNN, we represent each factor with an RNN. We refer the RNNs obtained from the node factors as nodeRNNs and the RNNs obtained from the edge factors as edgeRNNs. The interactions represented by the st-graph are captured through connections between the nodeRNNs and the edgeRNNs.
**Parameter sharing and structured feature space**

Structural-RNN make a connection between nodes and edges, and every one is trained by RNNs, so from the temporal graph, it will relate before state and the skeleto, then get a trade-off action to predict in the future.

## Video
### srnn_smoking
<p align="center">
  <img src="https://github.com/zhaolongkzz/human_motion/blob/master/images/srnn_smoking.gif"><br><br>
</p>

### srnn_eating
<p align="center">
  <img src="https://github.com/zhaolongkzz/human_motion/blob/master/images/srnn_eating.gif"><br><br>
</p>

## FAQ
**Q1**.the path is miss, and it will not run well?

**A1**:All the code is set by the premise of the scripts floder. So here you must change your dictionary to /scripts with your terminal, then it will get normal operation.

