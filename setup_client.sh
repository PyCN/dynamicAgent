#!/usr/bin/env bash

squid_path="/etc/squid3/"
squid_cfg="./source/squid.conf"
echo "start building proxy service ..."
apt-get update && apt-get upgrade -y
if [$? -eq 0]
then
    apt-get install python-dev python-pip zip unzip squid -y
    if [$? -ne 0]
    then
        exit 6
    fi
else
    exit 6
fi

pip install requests
if [$? -ne 0]
then
    exit 6
fi
echo "update ubuntu and install dependency packages successful"

if [-e $squid_cfg]
then
    echo "copy squid config from source/ to /etc"
    cp $squid_cfg $squid_path
else
    echo "squid config not found in source/"
    exit 66

echo "reconfigure squid..."
squid3 -k reconfigure 2>&1 > /dev/null
if [$? -eq 0]
then
    nohup python run.py & 2>&1 > /dev/null
    if [$? -ne 0]
    then
        echo "start proxy client task failed"
        exit 66
    fi
else
    echo "reconfigure squid3 failed"
    exit 66