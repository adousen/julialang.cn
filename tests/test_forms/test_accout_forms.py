#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests.base import BaseTestCase
from project.apps.account.forms import RegisterForm
from contrib.utils.generic import random_str


class RegisterFormTests(BaseTestCase):
    # Ensure invalid or valid data format throws error.
    def test_validate_invalid_username(self):
        form = RegisterForm(username="1tester", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="Invalid_tester", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="Invalid-tester_", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="Invalid-tester-", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="Invalid--testers", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="I", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username="I-", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username=u"张", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        form = RegisterForm(username=u"张-", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())
        orm = RegisterForm(username="a-very-very-lang-name",email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())

    def test_validate_valid_username(self):
        form = RegisterForm(username="A-valid-tester", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())
        form = RegisterForm(username="This-valid-tester", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())
        form = RegisterForm(username="At", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())
        form = RegisterForm(username="A-t", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())
        form = RegisterForm(username=u"张三", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())
        form = RegisterForm(username=u"张-三", email="tester@test.com", password="testing", repassword="testing")
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        form = RegisterForm(username="tester", email="test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())

    def test_validate_invalid_password(self):
        password = random_str(5)
        form = RegisterForm(username="tester", email="tester@test.com", password=password, repassword=password)
        self.assertFalse(form.validate())

        password = random_str(41)
        form = RegisterForm(username="tester", email="tester@test.com", password=password, repassword=password)
        self.assertFalse(form.validate())

    # existed
    def test_validate_existed_username(self):
        form = RegisterForm(username="user", email="tester@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())

    def test_validate_existed_email(self):
        form = RegisterForm(username="tester", email="user@test.com", password="testing", repassword="testing")
        self.assertFalse(form.validate())