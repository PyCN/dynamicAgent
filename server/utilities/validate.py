#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from urlparse import urlparse
import requests
import logging
import time

logging.basicConfig(filename='validating.log',
                    level=logging.WARNING, format='%(levelname)s - %(asctime)s: %(message)s')

check_url = 'http://www.google.com/search?q=python'


def get_unstable_proxy():
    url = 'http://173.82.80.104:5000/?count=50&country=国外'
    r = requests.get(url)
    if r.status_code == 200:
        ipxs = r.json()
        proxies = []
        for ipx in ipxs:
            ip = ipx[0]
            port = ipx[1]
            proxy = {
                'http': 'http://%s:%s' % (ip, port),
                'https': 'http://%s:%s' % (ip, port)
            }
            proxies.append(proxy)
        return proxies
    else:
        return None


def delete_ipx(ipx):
    logging.warning(
        '[error] --> invalidate ip proxy: {} -> deleting...'.format(ipx))
    ip = urlparse(ipx.get('http')).netloc
    requests.get('http://173.82.80.104:5000/delete?ip=' + ip)
    logging.warning('[tips] - invalidate proxy deleted')


def check_proxy(ipx):
    try:
        r = requests.get(check_url, proxies=ipx, timeout=30, verify=False)
        if r.status_code == 200:
            logging.info('[success] --> available proxy: {}'.format(ipx))
            return ipx
        else:
            logging.warning(
                '[waring] --> invalidate http proxy - status code: {}'.format(r.status_code))
            delete_ipx(ipx)
    except requests.ConnectionError:
        logging.warning('[waring] --> connection error')
        delete_ipx(ipx)
    except requests.ReadTimeout:
        logging.warning('[waring] --> connect timeout')
        delete_ipx(ipx)


def validator(proxies):
    pool = ThreadPool(5)
    # results = pool.map(check_proxy, proxies)
    pool.map(check_proxy, proxies)
    pool.close()
    pool.join()
    print '[success] --> validate completed'
    # return results


if __name__ == '__main__':
    print '---------------------> start validate http proxy'
    while True:
        proxies = get_unstable_proxy()
        validator(proxies)
        print '---------------------> wait for validate again'
        time.sleep(30 * 60)
