# SSH 内网穿透

## 服务端配置

- 修改ssh配置，打开端口转发

```Bash
# /etc/ssh/sshd_config
AllowTcpForwarding yes
GatewayPorts yes
```

然后重启ssh服务：sudo systemctl restart sshd

- 添加车端公钥到服务器

> 非必需，配置后可以免密连接，便于自动化执行

## 车端配置

- 和服务器公钥对应的私钥文件
  设置好权限：如600，权限太宽松，可能会被拒绝

- ssh启动
  
```Bash
# 使用autossh，命令更简单（autossh需要提前安装）
# -p远程ssh端口
# -M monitor，保活端口
# -N远程不执行，只透传
# -R远程转发，-L本地转发，-D动态转发
# -i证书，默认~/.ssh/id_rsa可省略
# 3334为远程端口，22为本地端口，建立映射
autossh -p 2222 -M 3333 -NR *:3334:localhost:22 -i <path-to-private-key> <user>@<IP>
```

## 添加自启

> 车端不能自启的话，服务挂掉就失联了，可以使用systemd实现开机自启动和退出重新启动

```Bash
# autossh.service
[Unit]
Description=AUTO SSH Tunnel
Documentation=https://segwayrobotics.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
User=nvidia
Type=simple
ExecStart=run-ssh-auto.sh
ExecReload=/bin/kill -s HUP ${MAINPID}
ExecStop=/bin/kill -s TERM ${MAINPID}

LimitNOFILE=100
LimitNPROC=3000
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=always
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target

添加autossh.service到系统，然后打开开机自启动
systemctl enable autossh.service
```
