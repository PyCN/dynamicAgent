#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

TOKEN = '73EA1Ada10a6F4C3e1eC7FaBACDEFB47c825CFB7eD49C3C9689AA8a35F7dBBd9264fa8fca5f4cBf2b0314aD4377C6b0999a1e5fAe5c8c31aD42657C1ce605B072ff3B42aEb8C9aad994cf9E3DAaaCC178791677288AdB48e319076e495Ec54dbcdc27bAF3Fc96c45b13Fa6A9c350D80f8Dcd4C559EFc0716bAec0Dbefb62AF5b'

DATA_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'cache/data.json'))

DB_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'cache/data.db'))


class SQLHelper(object):
    """docstring for SQLite"""

    def __init__(self):
        super(SQLHelper, self).__init__()
        # self.database = database
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()

    def insert(self, ID, ip, table='proxies'):
        '''
        >>> TABLES
        1 raw_ipxs
        2 verified_ipxs
        '''
        sql = "INSERT INTO {} (id, proxy) VALUES ({}, \'{}\')".format(
            table, ID, ip)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def update(self, ID, ip, table='proxies'):
        sql = "UPDATE {} set proxy=\'{}\' WHERE id={}".format(table, ip, ID)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def fetch(self, ID, table='proxies'):
        ''' retrieve ip proxies from db, default table is verified_ipxs and default number is one
        if ip proxies is less than the number, it will return all proxies in db
        -------------------------------------------------------
        >>> TABLES
        1 raw_ipxs
        2 verified_ipxs
        >>> db = SQLHelper()
        >>> db.fetchIP(2)
        [u'10.10.10.10:80', u'10.12.13.14:80']
        '''
        sql = 'SELECT proxy FROM {}  WHERE id={}'.format(table, ID)
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            return [x[0] for x in rows]
        except sqlite3.OperationalError as e:
            raise e

    def delete(self, ID, table='proxies'):
        '''
        >>> TABLES
        1 raw_ipxs
        2 verified_ipxs
        '''
        sql = 'DELETE FROM {} WHERE id=ID'.format(table, ID)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def drop(self):
        drop_table_1 = '''DROP TABLE proxies'''
        self.cur.execute(drop_table_1)
        print 'Drop data tables success'
        self.cur.close()

    def init(self):
        create_table_1 = '''
            CREATE TABLE  proxies(
                id INTERGER PRIMARY KEY NOT NULL,
                proxy TEXT NOT NULL
            )
        '''
        self.cur.execute(create_table_1)
        print 'Init database success'
        self.cur.close()

    def close(self):
        self.conn.close()
