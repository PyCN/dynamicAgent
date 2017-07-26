# dynamicAgent
动态拨号 vps HTTP 代理服务器搭建


## Server(固定 IP 机器) 配置

登录一台拥有固定公网 ip 的主机 
```bash
$ pip install bottle gunicorn
$ cd aynamicAgent/server
$ gunicorn -w 2 -b 0.0.0.0:8000 app:run -D
# 0.0.0.0:8000 是对外暴露的 api 接口，host:port 格式
```
ipdatbles 防火墙配置，增加 api 中的端口对外开放
```bash
$ iptables -F  # 懒癌患者
# 注：请务必加强网络安全意识，查阅运维手册正确配置您的防火墙
```
测试 api 接口是否可用，随便另一台机器，你的本机即可
```bash
# 修改 oneproxy.py 中的 api 接口
$ vi oneproxy.py
api = 'http://192.168.31.130:8008/api/get' # 你知道怎么改的
$ ./oneproxy.py
{u'status': 0, u'msg': u'ok', u'proxy': u'192.168.31.203:6578'}
# 返回响应，ok
```


## Client（拨号 VPS 机器）配置
> 云立方的动态拨号主机
### vps control panel![vps-control-panel](https://github.com/Zhiwei1996/dynamicAgent/raw/master/source/img/vps-control-panel.png)

ssh 连接到 vps，初始状态只有 root 用户，root 的 home 目录下有拨号脚本
```bash
root@cloud:~# ls
ppp.sh
# 执行脚本进行初始化拨号
root@cloud:~# ./ppp.sh
请输入ADSL帐号: xxxxxxx
请输入ADSL密码: xxxxxx
del ifcfg-eth0 Gateway  ...... Success
del ifcfg-eth0 DNS     ...... Success
MOdify chap-secrets    ...... Success
Modify pap-secrets     ......Success
Modify /etc/ppp/pppoe.conf      ......Success
/etc/resolvconf/update.d/libc: Warning: /etc/resolv.conf is not a symbolic link to /run/resolvconf/resolv.conf
# 执行成功后将创建如下 pppoe 相关执行文件(linux 命令)
root@cloud:~# pppoe-s
pppoe-server  pppoe-setup   pppoe-sniff   pppoe-start   pppoe-status  pppoe-stop
# 看命令名称可以知道其作用，pppoe-start 开始拨号上网，pppoe-stop断开拨号连接
root@cloud:~# pppoe-start
. Connected!
# 现在拨号已经完全设置好了，可以上网
```

```bash
# 更新 ubuntu 系统
root@cloud:~# apt-get update && apt-get upgrade -y
# 安装 python 相关组件
root@cloud:~# apt-get install python-dev python-pip -y
```

打开  `aynamicAgent/client/config.py` 进行配置
```python
# 拨号间隔
ADSL_CYCLE = 60  # 秒
# ADSL命令
ADSL_BASH = 'pppoe-stop;pppoe-start'

# 代理端口
PROXY_PORT = '6578'

# 服务器 API
SERVER_URL = 'http://host:port/api/store'  # host:port 要和 server 端配置的一样

# 通信秘钥
TOKEN = '73EA1Ada10a6F4C3e1eC7FaBACDEFB47c825CFB7eD49C3C9689AA8a35F7dBBd9264fa8fca5f4cBf2b0314aD4377C6b0999a1e5fAe5c8c31aD42657C1ce605B072ff3B42aEb8C9aad994cf9E3DAaaCC178791677288AdB48e319076e495Ec54dbcdc27bAF3Fc96c45b13Fa6A9c350D80f8Dcd4C559EFc0716bAec0Dbefb62AF5b'

# 客户端唯一标识
CLIENT_NAME = 'adsl1'

# 拨号网卡
ADSL_IFNAME = 'ppp0'
```


安装程序依赖的 python 包（依赖 requests ）
```bash
root@cloud:~# pip install requests
```
安装代理服务器软件  squid
```bash
root@cloud:~# apt-get install squid -y
```
配置 squid.conf
```bash
root@cloud:~# vim /etc/squid3/squid.conf

# Squid normally listens to port 3128
http_port 3128  # 改成 config.py 里设置的 6578

# Deny requests to certain unsafe ports
http_access deny !Safe_ports  # deny改成allow

# Deny CONNECT to other than secure SSL ports
http_access deny CONNECT !SSL_ports  # deny改成allow

# And finally deny all other access to this proxy
http_access deny all  # deny改成allow
```

重载 squid 配置文件，使新的配置文件生效

```bash
root@cloud:~#  squid3 -k reconfigure
```

验证代理是否起作用

```bash
# squid 的访问日志文件在 /var/log/squid3/access.log
tail -f /var/log/squid3/access.log
# 在一台linux机器上执行
curl -x host:port "http://www.baidu.com"
# 如果代理配置正确，回输出响应内容，同时代理服务器上的access.log会记录这次请求
```
设置 squid 高匿代理（可选项）
```json
# 修改配置文件squid.conf，在最后加上
request_header_access X-Forwarded-For deny all  
request_header_access From deny all  
request_header_access Via deny all
```

启动 client 端脚本，自动重新拨号发送更换后的ip到 server 端 api 接口
```bash
root@cloud:~/dynamicAgent/client# python run.py
ADSL Start, Please wait
ADSL Successfully
('New IP', '172.247.109.130')
('Successfully Sent to Server ', 'http://173.82.80.40:8000/api/store')
# 测试 ok， 先 ctr+c 终止， 然后开启后台运行
root@cloud:~/dynamicAgent/client# nohup python run.py &
```

---------------
有 bug 请不要联系我 noparking188@hmail.com
