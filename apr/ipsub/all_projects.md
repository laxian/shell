# IP白名单实际修改细节

## IP排查

[云端服务环境说明 & IP白名单](https://wiki.segwayrobotics.com/pages/viewpage.action?pageId=50279616)
[机器人端IP白名单需要修改的项目统计](https://doc.weixin.qq.com/txdoc/word?docid=w2_AAEA-gaQAMQgy5J2x8MRiSUOeNCfu&scode=AHwAVAcbAAgBb7PY15AAEA-gaQAMQ&type=0)

## 所有修改的项目

> 勾选代表代码已提交，前期优先修改S2机型相关项目，等测试通过后再修改其他机型

- [x] GXMonitor
- [x] SegwayProvision
- [x] GX_Service

  - [x] interactwatchdog

- [x] GxSystemDevKit
  
  - [x] message-client-sdk
  
    - [x] messageservice（使用了message-client-sdk）
  
  - [x] submit-sdk
  
    - [x] debuglog（使用该submit-sdk用于创建JIRA任务）
  
  - [x] toolbox

    - remotecontrol
    - messageservice
    - debuglog
    - watchdog

  - [x] robotconfig
  - [x] watchdog

- [x] nav_app
- [x] app-apr-food-deliver
- [ ] apprestaurant
- [ ] r1_app
- [ ] scooter_app
- [ ] lite_app

### mqtt only

- GX_Service

### http only

- SegwayProvision
- GXMonitor

## 需要提供的App

- SegwayProvision
- messageservice
- interactwatchdog
- nav_app
- watchdog
- robotconfig
- GXMonitor
- S2App
- debuglog
- r1_app
- scooter_app
- lite_app
- apprestaurant
- remotecontrol（只有toolbox埋点地址变更，如其他App埋点正常，可跳过）

### S2车型对应的App

#### 业务板

- SegwayProvision
- messageservice
- debuglog
- interactwatchdog
- S2App

#### 导航板

- SegwayProvision
- messageservice
- debuglog
- watchdog
- robotconfig
- GXMonitor
- nav_app

### D2车型对应的App

- SegwayProvision
- messageservice
- debuglog
- S2App
- watchdog
- robotconfig
- GXMonitor
- nav_app

### R1车型对应的App

- SegwayProvision
- messageservice
- debuglog
- watchdog
- robotconfig
- GXMonitor
- r1_app
- apprestaurant

## 测试注意事项

### 环境切换验证

- 业务有多个环境，对应不同的http地址
- 消息服务也有多个环境
- 不同的环境都要切换测试到

### 时间周期验证

- 如SegwayProvision，是激活应用，需要激活才能测试到修改是否生效
  
### 特定后台验证

- 导航埋点数据在logwatch，人工查看测试车辆埋点是否正常

### 流量监控

- 需要安装一个流量监控app
- 首次运行，需要安装并信任证书，安装证书又必须要求设置锁屏密码
- 保持流量监控app运行，且同意权限
- 网络请求信息包括访问的URL，以及建立的TCP、UDP连接，保存在特定日志中

### 三方网络地址

三方工具中也有网络访问，目前保持现状，加入白名单。目前已知的有：

- bugsnag（App异常上报监控后台）

```c
sessions.bugsnag.com # 35.190.88.7
notify.bugsnag.com # 35.186.205.6
```

- dokit（测试工具，不影响使用）

### 日志分析

目前方案，旧地址和新地址都是可用的，测试需要确保两点：

1. mqtt和http在各个环境都正常使用
2. mqtt和http都是访问的IP白名单中的地址，而不是旧地址

第一点通过人工测试验证

第二点通过日志分析确认

日志分析可能的两种异常：

1. 日志中出现旧地址
2. 日志中出现未知地址

对于旧地址，说明是替换漏掉的地址，补上即可
对于未知地址，说明是未排查到的地址，后端@李泽鑫，添加对应新地址到wiki，然后本地再修改

### 修改期间引入的新地址

有一定概率，在上述项目的IP修改期间，有新的提交引入了新的IP，目前暂不考虑，如有发现再修改

## Issue

- [x] netbare流量监控，打包，日志工具集成

[netbare-sample-apk下载](http://10.10.80.25:8080/files/netbare-sample-debug.apk)

- [ ] 所有项目打包
- [ ] bugsnag上报地址处理
