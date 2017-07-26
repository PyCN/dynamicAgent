#!/usr/bin/env bash

squid_path="/etc/squid3/"
squid_cfg="./source/squid.conf"
echo "-> start building proxy service"

echo "-> update ubuntu, please wait for minutes ..."
apt-get update && apt-get upgrade -y 2>&1 > /dev/null
if [ $? -eq 0 ]
then
    echo "-> install dependency packages, please wait for minutes ..."
    apt-get install python-dev python-pip squid -y --force-yes 2>&1 > /dev/null
    if [ $? -ne 0 ]
    then
        echo "!-> install failed"
        exit 6
    fi
else
    echo "!-> update failed"
    exit 6
fi

echo "-> install python requests ..."
pip install requests 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    exit 6
fi

if [ -e $squid_cfg ]
then
    echo "-> copy squid config to /etc path"
    cp $squid_cfg $squid_path
else
    echo "squid config not found in source/"
    exit 66
fi

echo "reconfigure squid ..."
squid3 -k reconfigure 2>&1 > /dev/null
if [ $? -eq 0 ]
then
    cd client/
    nohup python run.py &
    if [ $? -ne 0 ]
    then
        echo "start proxy client task failed"
        exit 66
    fi
else
    echo "reconfigure squid3 failed"
    exit 66
fi