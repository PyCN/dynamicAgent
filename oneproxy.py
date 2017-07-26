#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

TOKEN = '73EA1Ada10a6F4C3e1eC7FaBACDEFB47c825CFB7eD49C3C9689AA8a35F7dBBd9264fa8fca5f4cBf2b0314aD4377C6b0999a1e5fAe5c8c31aD42657C1ce605B072ff3B42aEb8C9aad994cf9E3DAaaCC178791677288AdB48e319076e495Ec54dbcdc27bAF3Fc96c45b13Fa6A9c350D80f8Dcd4C559EFc0716bAec0Dbefb62AF5b'

data = {
    'token': TOKEN
}

# 修改 api 接口
api = 'http://192.168.31.130:8008/api/get'
r = requests.post(api, data=data)
print r.json()
