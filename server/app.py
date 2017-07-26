#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, request, default_app
from config import TOKEN, DATA_FILE
# from config import SQLHelper
import json


# ---------------------------------------
# store proxy data in JSON
# ---------------------------------------
@route('/api/store', method='POST')
def storeipx():
    token = request.forms.get('token')
    if token == TOKEN:
        ipx = request.params.get('proxy')
        data = {'proxy': ipx}
        with open(DATA_FILE, 'wb') as fp:
            json.dump(data, fp)
        return {'status': 0, 'msg': 'ok'}
    else:
        return {'status': 2, 'msg': 'error - invalid authorization'}


@route('/api/get', method='POST')
def ipxapi():
    token = request.params.get('token')
    print token
    if token == TOKEN:
        with open(DATA_FILE, 'rb') as fp:
            try:
                data = json.load(fp)
            except ValueError:
                return {'status': 0, 'msg': 'error - no http proxy found'}
            try:
                ipx = data['proxy']
            except KeyError:
                ipx = None
            return {'status': 0, 'msg': 'ok', 'proxy': ipx}
    else:
        return {'status': 2, 'msg': 'error - invalid authorization'}


# ---------------------------------------
# store proxy data in sqlitedb
# ---------------------------------------
# @route('/api/store', method='POST')
# def storeipx():
#     token = request.forms.get('token')
#     if token == TOKEN:
#         db = SQLHelper()
#         ipx = request.params.get('proxy')
#         # data = {'proxy': ipx}
#         db.update(ID=1, ip=ipx)
#         return {'status': 0, 'msg': 'ok'}
#     else:
#         return {'status': 2, 'msg': 'error - invalid authorization'}


# @route('/api/get', method='POST')
# def ipxapi():
#     token = request.params.get('token')
#     if token == TOKEN:
#         db = SQLHelper()
#         data = db.fetch(ID=1)
#         try:
#             ipx = data[0]
#             return {'status': 0, 'msg': 'ok', 'proxy': ipx}
#         except IndexError:
#             return {'status': 0, 'msg': 'error - no proxy obtained'}
#     else:
#         return {'status': 2, 'msg': 'error - invalid authorization'}


if __name__ == '__main__':
    run(host='0.0.0.0', port='8000')

app = default_app()
