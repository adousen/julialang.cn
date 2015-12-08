#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试account.model模块

    :copyright: (c) 2015 by adousen.
"""
from tests.base import BaseTestCase

from project.apps.account.models import User, Role, PermissionCode, CodeToRole


class UserModelTests(BaseTestCase):
    def test_can_set_password_to_hash(self):
        self.assertTrue(self.test_user.password_hash is not None)

    def test_password_check(self):
        self.assertTrue(self.test_user.verify_password('testing'))

    def test_user_save(self):
        if not User.query.filter_by(email=self.test_user.email).first():
            self.assertTrue(False)

    def test_user_save_with_data_join(self):
        if not User.query.filter_by(email=self.test_user.email).first().data_join == self.test_user.data_join:
            self.assertTrue(False)

    def test_save_existed_username_fail(self):
        test_user = User(username=u'user', email='tester@test.com', password='testing')
        self.assertFalse(test_user.save())

    def test_save_existed_email_fail(self):
        test_user = User(username=u'tester', email='user@test.com', password='testing')
        self.assertFalse(test_user.save())

    def test_one_to_many_relationship(self):
        self.init_test_role_table()
        test_user1 = User(username=u'tester1', email='tester1@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user1.save()

        test_user2 = User(username=u'tester2', email='tester2@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user2.save()

        users = Role.query.filter_by(name=u"Superuser").first().users
        username_list = list()
        for user in users:
            username_list.append(user.username)
        self.assertIn(u'tester2', username_list)

    def test_many_to_one_relationship(self):
        self.init_test_role_table()
        test_user1 = User(username=u'tester1', email='tester1@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user1.save()

        self.assertEqual(1, test_user1.role.level)

    def test_check_user_is_superuser(self):
        self.init_test_role_table()
        test_user = User(username=u'tester', email='tester@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user.save()
        self.assertTrue(test_user.is_superuser)

    def test_check_user_is_admin(self):
        self.init_test_role_table()
        test_user = User(username=u'tester', email='tester@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Admin").first().id)
        test_user.save()
        self.assertTrue(test_user.is_admin)

    def test_check_user_is_moderator(self):
        self.init_test_role_table()
        test_user = User(username=u'tester', email='tester@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Moderator").first().id)
        test_user.save()
        self.assertTrue(test_user.is_moderator)



class RoleModelTests(BaseTestCase):
    def test_add_role(self):
        test_role = Role(name=u"System Tester", level=1)
        self.assertTrue(test_role.save())
        self.assertIsNotNone(Role.query.filter_by(name=u"System Tester").first())

    def test_find_all_users_of_a_role(self):
        self.init_test_role_table()
        test_user1 = User(username=u'tester1', email='tester1@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user1.save()

        test_user2 = User(username=u'tester2', email='tester2@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id)
        test_user2.save()

        self.assertEqual(Role.query.filter_by(name=u"Superuser").first().users[0].username, u'tester1')


class PermissionCodeModelTests(BaseTestCase):
    def test_add_code(self):
        test_code = PermissionCode(name=u"测试操作", code=50)
        self.assertTrue(test_code.save())
        self.assertIsNotNone(PermissionCode.query.filter_by(code=u'50').first())

    def test_init_codes(self):
        self.init_test_code_table()


class CodeToRoleModelTests(BaseTestCase):
    def setUp(self):
        super(CodeToRoleModelTests, self).setUp()
        self.init_test_role_table()
        self.init_test_code_table()
        
    def test_add_new(self):
        self.assertTrue(CodeToRole(role_level=1, permission_code=300).save())
        self.assertIsNotNone(CodeToRole.query.filter_by(permission_code=u'300').first())


class CodeToUser(BaseTestCase):
    def setUp(self):
        super(CodeToUser, self).setUp()
        self.init_test_role_table()
        self.init_test_code_table()

    def test_add_new(self):
        pass

