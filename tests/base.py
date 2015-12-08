#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests/base.py
from flask.ext.testing import TestCase
from project import create_app, db
from project.apps.account.models import User, Role, PermissionCode, CodeToRole
from contextlib import contextmanager


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
                              confirmed=True,
                              )
        self.test_user.save()

    # init test tables
    def init_test_role_table(self):
        Role.init_data()
        self.assertIsNotNone(Role.query.filter_by(name=u"Auth").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Moderator").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Admin").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Superuser").first())

    def init_test_code_table(self):
        PermissionCode.init_data()
        self.assertIsNotNone(PermissionCode.query.filter_by(code=u'100').first())
        self.assertIsNotNone(PermissionCode.query.filter_by(code=u'300').first())

    def init_test_code_to_role_table(self):
        CodeToRole.init_data()
        self.assertIsNotNone(CodeToRole.query.filter_by(permission_code=u'101').first())
        self.assertIsNotNone(CodeToRole.query.filter_by(permission_code=u'341').first())

    # context
    @contextmanager
    def init_all_user_tables_with_auth_user(self):
        try:
            self.init_test_role_table()
            self.init_test_code_table()
            self.init_test_code_to_role_table()

            test_auth_user = User(username=u'tester', email='tester@test.com', password='testing',
                        confirmed=True, role_id=Role.query.filter_by(name=u"Auth").first().id)
            test_auth_user.save()

            yield
        finally:
            pass

    @contextmanager
    def fake_test(self):
        try:
            self.app.config['IN_FAKE_TEST'] = True
            yield
        finally:
            self.app.config['IN_FAKE_TEST'] = False

