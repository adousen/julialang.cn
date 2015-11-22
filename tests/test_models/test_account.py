#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试account.model模块

    :copyright: (c) 2015 by adousen.
"""

import unittest
from flask.ext.testing import TestCase
from project import create_app, db
from project.apps.account.models import User


class UserModelTests(TestCase):
    def create_app(self):
        test_app = create_app('test')
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        db.create_all()
        self.test_user = User(username='user',
                              email='testuser@123.com',
                              password='password',
                              )
        self.test_user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_can_set_password_to_hash(self):
        self.assertTrue(self.test_user.password_hash is not None)

    def test_password_check(self):
        self.assertTrue(self.test_user.verify_password('password'))

    def test_user_save(self):
        if not User.query.filter_by(email=self.test_user.email).first():
            self.assertTrue(False)

    def test_user_save_fail(self):
        test_user = User(username='user', email='testuser@123.com', password='password')
        self.assertFalse(test_user.save())

    def test_can_save_data_join(self):
        if not User.query.filter_by(email=self.test_user.email).first().data_join == self.test_user.data_join:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()