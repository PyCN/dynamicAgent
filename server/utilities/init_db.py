#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import SQLHelper

db = SQLHelper()
db.init()
db.insert(1, '127.0.0.1:8080')
