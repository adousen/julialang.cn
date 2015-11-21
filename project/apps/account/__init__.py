#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from models import User
account = Blueprint('account', __name__)

import views_main


