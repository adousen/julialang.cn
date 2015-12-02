#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests/base.py
from flask.ext.testing import TestCase
from project import create_app, db
from project.apps.account.models import User, Role, PermissionCode


class BaseTestCase(TestCase):
    def create_app(self):
        test_app = create_app('test')
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        db.create_all()
        self.init_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def init_test_user(self):
        self.test_user = User(username=u'user',
                              email='user@test.com',
                              password='testing',
                              )
        self.test_user.save()

    def init_test_role_table(self):
        Role.init_data()
        self.assertIsNotNone(Role.query.filter_by(name=u"Auth").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Moderator").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Admin").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Superuser").first())

    def init_test_code_table(self):
        PermissionCode.init_data()
        self.assertIsNotNone(PermissionCode.query.filter_by(code=200).first())
        self.assertIsNotNone(PermissionCode.query.filter_by(code=300).first())
