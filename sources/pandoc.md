---
title: ubuntu pandoc 环境变量配置
date: 2020-03-01
---

### 问题描述

* 使用whereis命令在ubuntu上发现有三处pandoc所在的PATH目录，第一个是直接安装pandoc时形成的，第二个是rstudio目录里的，第三个是安装Anacoda时形成的，版本不一样，Anaconda更新后发现pandoc未更新的最新，rstudio中的版本应该是用在Rmarkdown导出文件的功能中的，也比较旧。
* 在Terminal中使用pandoc命令时，使用`pando -v`显示的版本（**2.3**)，与cd到pandoc安装目录`/path/to/pandoc -v`显示的版本(**2.6**)不一样，前者版本较低，使用`sudo apt install pandoc`命令时显示为系统已安装了最新版本。
* 将原版pandoc的bin目录加入`/etc/profile`中，不管放在Anaconda的path前面还是后面，在任意命令行中执行pandoc依然是Anaconda的版本。
* 想到除了`/etc/profile`之外，还有其他几个环境变量配置文件，可能是这几个文件之间存在先后和覆盖的关系。

### 问题搜索

* 在CSDN上看到一个[相关的文章](https://blog.csdn.net/smile_from_2015/article/details/80058351)，发现确实是不同的配置文件的不同功能和用途，导致了PATH变量被覆盖的情况，为了能在命令行中直接使用单独的pandoc，而不是Anaconda目录下的版本，需要重新在不同文件中修改环境变量，以便能够在不影响现有的PATH目录列表的情况下，使用最新版本的工具。
* 仅以我使用的ubuntu为例，四个配置文件分别为`/etc/profile`、`~/.profile`、`~/.bashrc`、`/etc/bash.bashrc`，它们的特点如下：

   1. `/etc/profile`针对系统中的所有用户，登录时加载，修改需要重启，可以用`source`命令立即生效。
   2. `~/.profile`针对系统当前用户，当前用户登录系统时加载，修改需要重启，可以用`source`命令立即生效。
   3. `/etc/bash.bashrc`为每一个（理解为所有）使用bash shell的用户执行，修改无需重启,重新打开新的bash即可生效。
   4. `~/.bashrc`为系统当前用户的bash shell执行，当用户登录以及打开shell时文件被读取，修改无需重启，重新打开新的bash即可生效。
   
### 问题解决
* 从上述说明来看，系统启动和用户登录时应该会首先执行前两个文件，打开Terminal时，会执行后两个文件，所以从PATH变量的角度来看，在Terminal中最先寻找的应该是`/etc/bash.bashrc`、`~/.bashrc`，如果没有会继续在前两个文件的PATH中寻找。
* 于是将Anaconda的PATH信息依然放在原先`/etc/profile`文件中，将单独的pandoc的bin目录放在`/etc/bashrc.bash`文件中，任意打开新的Terminal，输入`pandoc -v`，显示为**2.6**， 而输入`conda --version`也正常显示。