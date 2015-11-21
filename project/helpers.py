#!/usr/bin/env python
# coding=utf-8
"""
    helpers.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import re
import markdown
import urlparse
import functools
import hashlib
import socket, struct

from datetime import datetime

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from flask.ext.babel import gettext, ngettext, format_date, format_datetime

def request_wants_json(request):
    """ 
    we only accept json if the quality of json is greater than the
    quality of text/html because text/html is preferred to support
    browsers that accept on */*
    """
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
       request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def timesince(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    
    if default is None:
        default = gettext("just now")

    now = datetime.now()
    diff = now - dt

    years = diff.days / 365
    months = diff.days / 30
    weeks = diff.days / 7
    days = diff.days
    hours = diff.seconds / 3600
    minutes = diff.seconds / 60
    seconds = diff.seconds 

    periods = (
        (years, u"%s年" % years),
        (months, u"%s月" % months),
        (weeks, u"%s周" % weeks),
        (days, u"%s天" % days),
        (hours, u"%s小时" % hours),
        (minutes, u"%s分钟" % minutes),
        (seconds, u"%s秒" % seconds),
    )

    for period, trans in periods:
        if period:
            return u"%s前" % trans

    return default


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
_pre_re = re.compile(r'<pre (?=l=[\'"]?\w+[\'"]?).*?>(?P<code>[\w\W]+?)</pre>')
_lang_re = re.compile(r'l=[\'"]?(?P<lang>\w+)[\'"]?')


def code_highlight(value):
    f_list = _pre_re.findall(value)

    if f_list:
        s_list = _pre_re.split(value)

        for code_block in _pre_re.finditer(value):

            lang = _lang_re.search(code_block.group()).group('lang')
            code = code_block.group('code')

            index = s_list.index(code)
            s_list[index] = code2html(code, lang)

        return u''.join(s_list)

    return value


def code2html(code, lang):
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
