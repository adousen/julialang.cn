#!/usr/bin/env python
# coding=utf-8
"""
    mixins.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.login import UserMixin
from project import db


class UserLoginMixin(UserMixin):
    pass


class ActiveRecordMixin(object):
    def __init__(self, *args, **kwargs):
        pass

    # ActiveRecord method
    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception, msg:
            print('Error: Cannot save %s object, because ' % self.__class__ + msg.message)
            db.session.rollback()
            return False
        return True