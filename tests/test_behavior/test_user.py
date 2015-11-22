#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests.base import BaseTestCase

class TestAccountBlueprint(BaseTestCase):
    def test_register_route(self):
        """Ensure about route behaves correctly."""
        response = self.client.get('/account/register', follow_redirects=True)
        self.assertIn(u'邮箱注册', response.data.decode('utf8'))

    def test_user_registration(self):
        """Ensure registration behaves correctlys."""
        with self.client:
            self.app.config['IN_FAKE_TEST'] = True
            response = self.client.post(
                '/account/register',
                data=dict(username="tester", email="test@tester.com", password="testing", repassword="testing"),
                follow_redirects=True
            )
            self.assertIn(u'账号激活邮件', response.data.decode('utf8'))