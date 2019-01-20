[EN](https://github.com/zhaolongkzz/human_motion/blob/master/README.md) | 中文

# 人体姿态预测
通过使用结构化RNN(Structural-RNN)来进行人体预测!

## 概要
Here I provide the code for [CVPR2015 Structural-RNN](https://arxiv.org/pdf/1511.05298.pdf), the original code of author is [here](http://asheshjain.org/srnn/).

The work I have done is making a ROS topic to publish motion data,then a predicter to subscribe the data and predict the next motion from dataset.
### Files Location:
- ./scripts/Prediction/generateMotionForecast.py
- ./scripts/Animation/motionAnimation.py
### Subscriptions:

### Publications:


## Prerequisites
- ubuntu16.04
- anaconda3
- ROS-Kinetic

you can create an environment to run them.

```conda install -n srnn python=2.7```
- python=2.7
- numpy>=1.8.1
- theano=0.8.2
- matplotlib=2.2.3
- h5py=2.9.0
if you want to train it with GPU here, you should install cuda
- cuda=8.0
- libcudnn6_6.0.21

with the theano, using the package [NeuralModels](https://github.com/asheshjain399/NeuralModels) same as the paper.
```python setup.py develop```

you can download the mocap dataset from [here](http://www.cs.stanford.edu/people/ashesh/h3.6m.zip), if you want more raw dataset, you can visit [H3.6m](http://vision.imar.ro/human3.6m/description.php).

## Quickstart

```bash
git clone https://github.com/zhaolongkzz/human_motion.git
unzip human_motion
cd human_motion
wget http://www.cs.stanford.edu/people/ashesh/h3.6m.zip
unzip h3.6m.zip
rm h3.6m.zip

```

**With python**
```python
cd scripts
# train your model
python Prediction/generateMotionForecast.py srnn smoking
# make a animation, and then it will play it automaticcally
python Animation/motionAnimation.py --model srnn --action smoking
# the result data will save with a h5df file in /Motion floder!
```

**With ROS**

Play the animation of the motion!
```bash
cd human_motion/scripts
roscore
# predict the motion, remember to open another terminal
rosrun human_motion motion_predicts.py erd Pre-trained/srnn_smoking/
# read the file and publish the msg
rosrun human_motion motion_publisher.py srnn smoking
# get the data, and play the animation
rosrun human_motion motion_animation.py
```

## Structure



## Video
Uploading...It will coming soon! 

## FAQ








