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
git clone https://github.com/zhaolongkzz/human_motion
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
# 训练数据集,可能需要花费大概20min
python Prediction/generateMotionForecast.py srnn smoking
# 制作一个动画, 然后播放动画
python Animation/motionAnimation.py --model srnn --action smoking
# 动画的数据结果会以h5df格式保存到/Motion文件夹下
```

### 使用ROS

播放运动的结果!
```bash
cd human_motion/scripts
roscore
# 预测结果, 记得打开另外一个terminal
rosrun human_motion motion_predicts.py srnn smoking
# 读取文件以及发布msg信息
rosrun human_motion motion_publisher.py srnn smoking
# 获得数据,并且播放动画
rosrun human_motion motion_animation.py
```

可以通过RViz来运行真实值和预测值
```bash
rosrun human_motion read_motion.py h3.6m/dataset/S5/smoking_1.txt
rosrun human_motion rviz_motion.py motion:=/motion_skeleto
```

## 结构
human\_motion文件夹下.你需要把数据集放到该文件夹下.

<p align="center">
  <img src="https://github.com/zhaolongkzz/human_motion/blob/master/images/Tree.png"><br><br>
</p>

S-RNN架构来自st图的因子图表示。 st图中的因子以时间方式操作，其中在每个时间步骤中因子观察（节点和边缘）特征并对这些特征执行一些计算。 在S-RNN中，我们用RNN表示每个因子。 我们将从节点因子获得的RNN称为nodeRNN，将从边缘因子获得的RNN称为edgeRNN。 通过nodeRNN和edgeRNN之间的连接捕获由st图表示的交互。
**参数共享和结构化特征空间**

结构-RNN在节点和边缘之间建立连接，并且每个都由RNN训练，因此从时间图中，它将在状态和角度之前相关，然后得到权衡行为以在将来进行预测。


## 视频
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










