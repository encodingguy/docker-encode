# Docker-VapourSynth-Linux

## Software Versions

- python3: 3.8.5
- dgdemux: v1.0.0.50
- mediainfo: v21.03
- rclone: v1.55.0
- x264: x264-r3048-b86ae3c

## Vapoursynth Plugins
* [vapoursynth-fillborders](https://github.com/dubhater/vapoursynth-fillborders)
* [Adaptivegrain-rs v0.3.1](https://git.kageru.moe/kageru/adaptivegrain)
* [RemapFrames v1.1](https://github.com/Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames)

## Vapoursynth Python Module
* [awsmfunc](https://git.concertos.live/AHD/awsmfunc)
* [vardefunc](https://github.com/Ichunjo/vardefunc/)
## How to build the environment

```
docker-compose up -d
```

## How to enter the container

```
docker exec -it vapoursynth-linux /bin/bash
```

## How to encode a movie

Please refer to [WhaleHu/Encode-guide-frds](https://github.com/WhaleHu/Encode-guide-frds)


# Tutorial from Krita

### 一.环境准备

#### 1.Docker部署

##### ①.拉取文件：

```
git clone https://github.com/gzycode39/docker-vapoursynth-yuuno.git
```

##### ②.进入项目目录

```
cd docker-vapoursynth-yuuno
```

##### ③.启动容器：

```
docker-compose up -d
```

##### ④.进入容器：

```
docker exec -it vapoursynth-linux /bin/bash
```

##### ⑤.删除容器

```
docker-compose ps

docker-compose down
```

##### ⑥.更新镜像

```
docker pull yyfyyf/vapoursynth-yuuno:v0.X
X为最新版本号
```

#### 2.拉取原盘，压片前的装备

##### ①.拉取原盘文件至容器外对应/encode的目录下

##### ②.查看原盘目录结构

```
eac3to 目录
```

##### ③.找到对应的（最大的）mpls，并提取其全部文件到当前目录

```
eac3to-demux 目录
```

##### ④.进入jupyter notebook

```
ip:映射端口
```

### 二.压制样片

#### 1.使用现成脚本或新建python3脚本

```
先输一行%load_ext yuuno
然后下面输入%%vspreview再接脚本代码
run
```

#### 2.查看并记录原片及样片帧数，进行切黑边，修脏边等操作



#### 3.压制样片

把ipynb的脚本内容复制一份到vpy，修改sh脚本中的帧数为样片帧数，修改vpy为对应vpy

运行sh脚本，压制样片

观察码率



### 三.样片与原片进行对比

#### 1.在ipynb加入抽取对比



#### 2.对比样片图片及原片图片



#### 3.根据情况对crf值进行0.5步进微调



#### 4.可以则开始正片压制，不可则重新压制样片，重新进行对比



### 四.压制成片

#### 1.修改sh脚本中帧数为原片帧数，执行sh脚本进行压制

#### 2.等待压制完成



#### 五.进行成片与原片对比

