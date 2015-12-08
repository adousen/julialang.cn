#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.permission
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试permission模块

    :copyright: (c) 2015 by adousen.
"""
from tests.base import BaseTestCase

from project.apps.account.models import User, Role, PermissionCode, CodeToRole
from flask.ext.login import (login_user, current_user, login_required, user_logged_in,
    user_logged_out, user_unauthorized)
from flask.signals import Namespace
from werkzeug.exceptions import HTTPException
from flask.ext.principal import identity_changed, Identity, PermissionDenied

from project.permissions import RolePerms, CodePerms


class PermissionTests(BaseTestCase):
    def setUp(self):
        super(PermissionTests, self).setUp()
        self.init_test_role_table()
        self.init_test_code_table()
        self.init_test_code_to_role_table()

        self.unauthorized_handled = False  # 是否对未获许可权限操作进行了后续处理
        self.no_permission_handled = False
        user_no_permission_signal = Namespace().signal('no-permission')

        @user_logged_in.connect_via(self.app)
        def logged_in(app, user):
            print('You were logged in')
            return

        @user_logged_out.connect_via(self.app)
        def logged_out(app, user):
            print('You were logged out')
            return

        @user_unauthorized.connect_via(self.app)
        def unauthorized(app, user=None):
            self.unauthorized_handled = True

        @user_no_permission_signal.connect_via(self.app)
        def no_permission_signal(app, user=None):
            self.no_permission_handled = True  # not used

    @login_required
    def do_something_need_unauthorized(self):
        self.assertTrue(current_user.is_authenticated(), "Should not go here without login!")
        return True

    @CodePerms.User.EDIT.require(User, 403)
    def edit_user_profile_route(self, id):
        return True

    def test_when_not_logged_in(self):
        self.test_user.save()
        self.do_something_need_unauthorized()
        self.assertTrue(self.unauthorized_handled)

    def test_when_logged_in(self):
        """If user is logged in, do_something_need_unauthorized()"""
        login_user(self.test_user)
        self.assertTrue(self.do_something_need_unauthorized())

        #

    def test_normal_user_no_permission_to_edit_profile_throws_HTTPException(self):
        # a superuser
        one_user = User(username=u'normal_user', email='normal_user@test.com', password='testing',
                          role_id=Role.query.filter_by(name=u"auth").first().id, confirmed=True)

        test_normal_user = User(username=u'test_normal_user', email='test_normal_user@test.com',
                                password='testing',
                                role_id=Role.query.filter_by(name=u"auth").first().id,
                                confirmed=True)
        one_user.save()
        test_normal_user.save()
        login_user(test_normal_user)
        identity_changed.send(self.app, identity=Identity(test_normal_user.id))
        self.assertRaises(HTTPException, self.edit_user_profile_route, id=one_user.id)

    def test_permission_of_someone_to_edit_self_profile(self):
        # a superuser
        test_normal_user = User(username=u'normal_user', email='normal_user@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"auth").first().id, confirmed=True)
        test_normal_user.save()
        login_user(test_normal_user)
        identity_changed.send(self.app, identity=Identity(test_normal_user.id))
        self.assertTrue(self.edit_user_profile_route(id=test_normal_user.id))

    def test_permission_of_superuser_to_edit_profile(self):
        """Confirm superuser can edit anyone's profile"""
        one_user = User(username=u'normal_user', email='normal_user@test.com', password='testing',
                          role_id=Role.query.filter_by(name=u"auth").first().id, confirmed=True)
        test_superuser = User(username=u'superuser', email='superuser@test.com', password='testing',
                         role_id=Role.query.filter_by(name=u"Superuser").first().id, confirmed=True)
        one_user.save()
        test_superuser.save()
        login_user(test_superuser)
        identity_changed.send(self.app, identity=Identity(test_superuser.id))
        try:
            self.assertTrue(self.edit_user_profile_route(id=one_user.id))
        except HTTPException, e:
            self.assertFalse(True, "Catch an Error, superuser has no Permission!")
