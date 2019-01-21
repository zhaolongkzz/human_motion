[EN](https://github.com/zhaolongkzz/human_motion/blob/master/README.md) | 中文

# 人体姿态预测
通过使用结构化RNN(Structural-RNN)来进行人体预测!

## 概要
这里提供[CVPR2015 Structural-RNN](https://arxiv.org/pdf/1511.05298.pdf)的论文,作者的源代码链接[点击](http://asheshjain.org/srnn/).

我所做的工作是复现该论文的效果，并从所得到的结果中制作动画。 以及制作ROS的topic以发布运动数据，然后使用预测部分来订阅数据并预测数据集中的下一个运动。 提供运行在Rviz中获得了TF动画的代码。

定性地，ERD比LSTM-3LR更好地模拟人体运动。 然而，从短期来看，它并不像LSTM-3LR那样模仿地面实况。

它可以很好地处理短期和长期预测。 并且SRNN在短期和长期预测中都表现良好，最重要的是SRNN在所有算法的非周期性活动中也能很好地完成。


### 主要的文件位置:
- ./scripts/Prediction/generateMotionForecast.py
- ./scripts/Animation/motionAnimation.py

## 前提需要
- ubuntu16.04
- anaconda3
  &ensp;&ensp;(安装anaconda, 可以点击[这里](http://docs.anaconda.com/anaconda/install/linux/).)
- ROS-Kinetic
  &ensp;&ensp;(可以去ROS的官网安装,点击[这里](http://wiki.ros.org/kinetic/Installation/Ubuntu).)
- python=2.7
  &ensp;&ensp;(通过下面所述的anaconda来创建虚拟环境)

创建一个虚拟环境来运行本代码.

```bash
conda create -n srnn python=2.7
```

你需要安装的python包:
- numpy>=1.8.1
- theano=0.8.2
- matplotlib=2.2.3
- h5py=2.9.0

如果你想要使用加速训练,那么你可以安装cuda来使用你的GPU:
- cuda=8.0
- libcudnn6_6.0.21

通过theano, 使用与原论文中相同的神经网络框架[NeuralModels](https://github.com/asheshjain399/NeuralModels).
运用theano的模型, 以下方式进行安装:
```python setup.py develop```

## 数据集
**注意:** 你可以从[这里](http://www.cs.stanford.edu/people/ashesh/h3.6m.zip)下载运动捕捉的数据集, 如果你想要更多的原始数据集信息, 你可以访问[H3.6m](http://vision.imar.ro/human3.6m/description.php)官方的数据集网站.

论文中含有预处理的数据集, 可以在[谷歌云盘](https://drive.google.com/drive/folders/0B7lfjqylzqmMZlI3TUNUUEFQMXc)中下载.
(**原论文作者提供**)

## 快速开始

首先,从github上git下载本带代码:
```bash
git clone https://github.com/zhaolongkzz/human_motion.git
unzip human_motion
cd human_motion/scripts
wget http://www.cs.stanford.edu/people/ashesh/h3.6m.zip
unzip h3.6m.zip
rm h3.6m.zip
# 从谷歌云下载预处理的数据集```
```

**注意:**从谷歌云中下载的数据集, 需要放入scripts中新建命名为Pre-trained的文件夹.(h3.6m和Pre-train文件夹都放置于scripts文件夹下.)


### 使用python
```bash
cd scripts
# train your model, it will cost you about 20 min
python Prediction/generateMotionForecast.py srnn smoking
# make a animation, and then it will play it automaticcally
python Animation/motionAnimation.py --model srnn --action smoking
# the result data will save with a h5df file in /Motion floder!
```

### ROS

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

Here you can run the ground_truth or forcast file with RViz
```bash
rosrun human_motion read_motion.py h3.6m/dataset/S5/smoking_1.txt
rosrun human_motion rviz_motion.py motion:=/motion_skeleto
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

### srnn_smoking in RViz
<p align="center">
  <img src="https://github.com/zhaolongkzz/human_motion/blob/master/images/rviz.gif"><br><br>
</p>

## FAQ
**Q1**.the path is miss, and it will not run well?

**A1**:All the code is set by the premise of the scripts floder. So here you must change your dictionary to /scripts with your terminal, then it will get normal operation.










