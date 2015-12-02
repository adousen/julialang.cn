#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试account.model模块

    :copyright: (c) 2015 by adousen.
"""
from tests.base import BaseTestCase

from project.apps.account.models import User, Role, PermissionCode


class UserModelTests(BaseTestCase):
    def test_can_set_password_to_hash(self):
        self.assertTrue(self.test_user.password_hash is not None)

    def test_password_check(self):
        self.assertTrue(self.test_user.verify_password('testing'))

    def test_user_save(self):
        if not User.query.filter_by(email=self.test_user.email).first():
            self.assertTrue(False)

    def test_save_existed_username_fail(self):
        test_user = User(username=u'user', email='tester@test.com', password='testing')
        self.assertFalse(test_user.save())

    def test_save_existed_email_fail(self):
        test_user = User(username=u'tester', email='user@test.com', password='testing')
        self.assertFalse(test_user.save())

    def test_can_save_data_join(self):
        if not User.query.filter_by(email=self.test_user.email).first().data_join == self.test_user.data_join:
            self.assertTrue(False)


class RoleModelTests(BaseTestCase):
    def test_add_role(self):
        test_role = Role(name=u"系统测试员", group="-1", level="4")
        self.assertTrue(test_role.save())
        self.assertIsNotNone(Role.query.filter_by(name=u"系统测试员").first())

    def test_init_roles(self):
        Role.init_roles()
        self.assertIsNotNone(Role.query.filter_by(name=u"Auth").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Moderator").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Admin").first())
        self.assertIsNotNone(Role.query.filter_by(name=u"Superuser").first())


class PermissionCodeModelTests(BaseTestCase):
    def test_add_role(self):
        test_code = PermissionCode(name=u"测试操作", code=100)
        self.assertTrue(test_code.save())
        self.assertIsNotNone(PermissionCode.query.filter_by(code=100).first())

    def test_init_codes(self):
        PermissionCode.init_codes()
        self.assertIsNotNone(PermissionCode.query.filter_by(code=200).first())
        self.assertIsNotNone(PermissionCode.query.filter_by(code=300).first())