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
from project import create_app


class UserModelTests(unittest.TestCase):
    def create_app(self):
        test_app = create_app('test')
        return test_app

    def setUp(self):
        from project.apps.account.models import User
        self.test_user = User(password='cat', email='123123123@123.com')

    def test_password_setter(self):
        u = self.test_user
        print(self.test_user.password_hash)
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = self.test_user
        self.assertTrue(u.verify_password('cat'))

if __name__ == '__main__':
    unittest.main()