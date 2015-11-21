#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

website = Blueprint('website', __name__, static_folder='static', static_url_path='/website')

from . import views, errors

