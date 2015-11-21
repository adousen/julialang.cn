#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_account
    ~~~~~~~~~~~~~~~~~~

    测试account模块的model

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
        self.test_user = User(password='cat', email='123123123@123.com')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_setter(self):
        print(self.test_user.password_hash)
        self.assertTrue(self.test_user.password_hash is not None)

    def test_password_verification(self):
        self.assertTrue(self.test_user.verify_password('cat'))

    def test_user_save(self):
        save_flag = False

        self.test_user.save()
        if User.query.filter_by(email=self.test_user.email).first():
            save_flag = True

        self.assertTrue(save_flag)

if __name__ == '__main__':
    unittest.main()