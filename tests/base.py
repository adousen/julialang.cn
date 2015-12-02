#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests/base.py
from flask.ext.testing import TestCase
from project import create_app, db
from project.apps.account.models import User


class BaseTestCase(TestCase):
    def create_app(self):
        test_app = create_app('test')
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        db.create_all()
        self.test_user = User(username=u'user',
                              email='user@test.com',
                              password='testing',
                              )
        self.test_user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

