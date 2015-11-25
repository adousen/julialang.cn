#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests.base import BaseTestCase
from flask.ext.login import current_user

class TestAccountBlueprint(BaseTestCase):
    def test_register_route(self):
        """Ensure register route behaves correctly."""
        response = self.client.get('/account/register', follow_redirects=True)
        self.assertIn(u'邮箱注册', response.data.decode('utf8'))

    def test_user_registration_behaves_correctly(self):
        """Ensure registration behaves correctly."""
        with self.client:
            self.app.config['IN_FAKE_TEST'] = True
            response = self.client.post(
                '/account/register',
                data=dict(username="tester", email="tester@test.com", password="testing", repassword="testing"),
                follow_redirects=True
            )
            self.assertIn(u'账号激活邮件', response.data.decode('utf8'))

    def test_login_route(self):
        """Ensure register route behaves correctly."""
        response = self.client.get('/account/login', follow_redirects=True)
        self.assertIn(u'邮箱登录', response.data.decode('utf8'))

    def test_user_login_behaves_correctly(self):
        """Ensure user login behaves correctly."""
        with self.client:
            response = self.client.post(
                'account/login',
                data=dict(email="user@test.com", password="testing"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(u'登录成功', response.data.decode('utf8'))
            self.assertTrue(current_user.email == "user@test.com")
            self.assertTrue(current_user.username == "user")
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.is_authenticated())
            self.assertFalse(current_user.is_anonymous())
            self.assertEqual(int(current_user.get_id()), 1)

    def test_logout_route_requires_login(self):
        # Ensure logout route requires login.
        with self.client:
            response = self.client.get('account/logout', follow_redirects=True)
            self.assertIn(u'请先登录', response.data.decode('utf8'))

    def test_user_logout_behaves_correctly(self):
        # Ensure logout behaves correctly - regarding the session.
        with self.client:
            self.client.post(
                'account/login',
                data=dict(email="user@test.com", password="testing"),
                follow_redirects=True
            )
            response = self.client.get('account/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(u'登出成功', response.data.decode('utf8'))
            self.assertTrue(current_user.is_anonymous())
            self.assertFalse(current_user.is_active())
            self.assertFalse(current_user.is_authenticated())
