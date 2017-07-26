#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests.exceptions import ConnectionError
from config import *
import subprocess
import requests
import time


def local_ipaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    addr = s.getsockname()[0]
    s.close()
    return addr


def adsl():
    while True:
        print('ADSL Start, Please wait')
        try:
            subprocess.check_output(ADSL_BASH, shell=True)
            status = 0
        except subprocess.CalledProcessError:
            status = 2
        if status == 0:
            print('ADSL Successfully')
            ip = local_ipaddress()
            if ip:
                print('New IP', ip)
                try:
                    requests.post(SERVER_URL, data={
                                  'token': TOKEN, 'proxy': ip + ':' + PROXY_PORT, 'name': CLIENT_NAME})
                    print('Successfully Sent to Server ', SERVER_URL)
                except ConnectionError:
                    print('Failed to Connect Server ', SERVER_URL)
                time.sleep(ADSL_CYCLE)
            else:
                print('Get IP Failed')
        else:
            print('ADSL Failed, Please Check')
        time.sleep(ADSL_CYCLE)


if __name__ == '__main__':
    adsl()
