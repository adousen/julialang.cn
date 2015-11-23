#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    contrib.utils.generic
    ~~~~~~~~~~~~~~~~~~

    生成验证函数

    :copyright: (c) 2015 by adousen.
"""
from datetime import datetime
from random import Random
import random


def random_str(length=6):
    string = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars_length = len(chars) - 1
    random = Random()
    for i in range(length):
        string += chars[random.randint(0, chars_length)]
    return string


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))