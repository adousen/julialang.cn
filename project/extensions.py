#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    extensions
    ~~~~~~~~~~~~~~~~~~

    导入外部扩展

    :copyright: (c) 2015 by adousen.
"""
from flask.ext.flatpages import FlatPages
from flask.ext.flatpages import Page
import operator
from itertools import takewhile
from werkzeug.utils import import_string


class MyFlatPages(FlatPages):
    def _parse(self, content, path):
        """Parse a flatpage file, i.e. read and parse its meta data and body.

        :return: initialized :class:`Page` instance.
        """
        lines = iter(content.split('\n'))

        # Read lines until an empty line is encountered.
        meta = '\n'.join(takewhile(operator.methodcaller('strip'), lines)).strip('---\n')
        # The rest is the content. `lines` is an iterator so it continues
        # where `itertools.takewhile` left it.
        content = '\n'.join(lines)

        # Now we ready to get HTML renderer function
        html_renderer = self.config('html_renderer')

        # If function is not callable yet, import it
        if not callable(html_renderer):
            html_renderer = import_string(html_renderer)

        # Make able to pass custom arguments to renderer function
        html_renderer = self._smart_html_renderer(html_renderer)

        # Initialize and return Page instance
        return Page(path, meta, content, html_renderer)

pages = MyFlatPages()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap()

from flask.ext.moment import Moment
moment = Moment()

from flask.ext.mail import Mail
mail = Mail()

from contrib.mail import SendMail
sendmail = SendMail()

from flask.ext.frozen import Freezer
freezer = Freezer()