商品价格追踪系统（适用于淘宝商城，天猫商城，京东商城）

## 淘宝商品数据追踪系统.
### 安装开发库和依赖库
1. 安装轻量级浏览器--phantomjs  [链接: https://pan.baidu.com/s/12HCAumGqy5SVMZuLsi1wVg 密码: en4x]
```shell
$ tar -zxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && sudo rm phantomjs-2.1.1-linux-x86_64.tar.bz2
$ cd phantomjs-2.1.1-linux-x86_64/bin
$ sudo mv phantomjs /usr/local/bin
$ sudo chown root:root /usr/local/bin/phantomjs
```

2. 升级Ubuntu14.04自带的Python3.4至3.5版本
```shell
$ sudo add-apt-repository ppa:fkrull/deadsnakes
$ sudo apt-get update
$ sudo apt-get install python3.5
$ sudo rm /usr/bin/python3
$ sudo ln -s /usr/bin/python3.5m /usr/bin/python3
```

3. 安装python开发工具
```shell
$ sudo apt-get install build-essential
$ sudo apt-get install python3.5-dev
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade pip
```

4. 安装sip  [链接: https://pan.baidu.com/s/1txI1Y7fK_arnL0VAK_GlJA 密码: up5f]
```shell
$ tar -zxvf sip-4.19.8.tar.gz && sudo rm sip-4.19.8.tar.gz
$ cd sip-4.19.8
$ sudo python3 configure.py
$ sudo make
$ sudo make install
```

5. 安装PyQt5方案1  [链接: https://pan.baidu.com/s/1fRZHtphJME3y9X9vRDCqfA 密码: 27q3]
```shell
$ sudo apt-get install qt-sdk
$ tar -zxvf PyQt5_gpl-5.10.1.tar.gz  && sudo rm PyQt5_gpl-5.10.1.tar.gz
$ cd PyQt5_gpl-5.10.1
$ sudo python3 configure.py --sip-incdir=/usr/include/python3.5
$ sudo make -j4
$ sudo make install
```

6. 安装PyQt5方案2  [该种方法支持中文输入，建议选择方案2]
```shell
$ sudo apt install fcitx-frontend-qt5 fcitx-libs-qt fcitx-libs-qt5
$ sudo cp /usr/lib/x86_64-linux-gnu/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so /usr/local/lib/python3.5/dist-packages/PyQt5/Qt/plugins/platforminputcontexts/
$ sudo chmod +x /usr/local/lib/python3.5/dist-packages/PyQt5/Qt/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so
$ sudo pip3 install PyQt5
```

7. 安装相关依赖库
```shell
$ sudo apt-get install sqlite3 
$ sudo apt-get install libpng-dev
$ sudo pip3 install bs4
$ sudo pip3 install selenium 
$ sudo pip3 install xlwt 
$ sudo pip3 install pyyaml  
$ sudo pip3 install --upgrade pillow
```

8. 安装matplotlib  [链接: https://pan.baidu.com/s/1rZb2xqdECJ_uQevb2YQ3Wg 密码: u8nh]
```shell
$ tar -zxvf matplotlib-master.zip && sudo rm matplotlib-master.zip
$ cd matplotlib-master
$ sudo pip3 install --upgrade setuptools
$ sudo python3 setup.py build
$ sudo python3 setup.py install
```

9. 可选安装  [链接: https://pan.baidu.com/s/12daywXnyJHko5203X-lFXg 密码: mx32]
```shell
$ tar -zxvf freetype-2.9.tar.bz2 && sudo rm freetype-2.9.tar.bz2
$ cd freetype-2.9
$ ./configure
$ make
$ sudo make install
```
### 克隆源码
```shell
$ sudo apt-get install git
$ git clone https://github.com/summychou/TBTracker.git
$ cd TBTracker/TBTracker
````
### 初始化系统数据库
```shell
$ sudo python3 TBTracker_InitDataBase.py
```
### 运行系统
```shell
$ sudo python3 TBTracker_Main.py
```
### 运行定时采集程序
开启一个终端，执行以下命令
```shell
$ sudo apt-get install redis-server
$ sudo pip3 install celery 
$ sudo pip3 install redis
$ redis-server
```
另开一个终端，执行以下命令（注意在TBTracker_Tasks.py所在目录下执行）
```
$ celery -A TBTracker_Tasks worker --loglevel=info
```
再开一个终端，执行以下命令（注意在TBTracker_Tasks.py所在目录下执行）
```shell
$ celery -A TBTracker_Tasks beat
```
系统会在每天凌晨三点钟执行采集任务。
## JUST ENJOY IT!!!