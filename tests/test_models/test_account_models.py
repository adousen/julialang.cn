#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试account.model模块

    :copyright: (c) 2015 by adousen.
"""
from tests.base import BaseTestCase

from project.apps.account.models import User


class UserModelTests(BaseTestCase):
    def test_can_set_password_to_hash(self):
        self.assertTrue(self.test_user.password_hash is not None)

    def test_password_check(self):
        self.assertTrue(self.test_user.verify_password('testing'))

    def test_user_save(self):
        if not User.query.filter_by(email=self.test_user.email).first():
            self.assertTrue(False)

    def test_existed_user_save_fail(self):
        test_user = User(username='user', email='tester@test.com', password='testing')
        self.assertFalse(test_user.save())

        test_user = User(username='tester', email='user@test.com', password='testing')
        self.assertFalse(test_user.save())

    def test_can_save_data_join(self):
        if not User.query.filter_by(email=self.test_user.email).first().data_join == self.test_user.data_join:
            self.assertTrue(False)

