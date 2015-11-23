#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from flask.ext.testing import TestCase
from project import create_app
from flask import request


class SiteUrlTests(TestCase):
    def create_app(self):
        test_app = create_app('test')
        return test_app

    def test_url_resolve_to_homepage(self):
        with self.client as client:
            client.get("/")
            self.assertEqual(request.endpoint, 'website.home')

    def test_url_resolve_to_account_register(self):
        with self.client as client:
            client.get('/account/register')
            self.assertEqual(request.endpoint, 'account.register')
