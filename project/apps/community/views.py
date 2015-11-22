#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from .import community


@community.route('/')
def index():
    return render_template('index.html')