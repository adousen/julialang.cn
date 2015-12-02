#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def parent_dir(path):
    """Return the parent of a directory."""

    return os.path.abspath(os.path.join(path, os.pardir))


class Config(object):
    REPO_NAME = "julialang.cn"  # Used for FREEZER_BASE_URL
    DEBUG = True

    # In order to skip some route in test
    IN_FAKE_TEST = False

    APP_DIR = basedir

    PROJECT_ROOT = os.path.join(basedir, 'project')
    # In order to deploy to Github pages, you must build the static files to
    # the project root
    FREEZER_DESTINATION = PROJECT_ROOT
    # Since this is a repo page (not a Github user page),
    # we need to set the BASE_URL to the correct url as per GH Pages' standards
    FREEZER_BASE_URL = "http://localhost/"
    FREEZER_REMOVE_EXTRA_FILES = False  # IMPORTANT: If this is True, all app files
                                        # will be deleted when you run the freezer
    FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
    FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
    FLATPAGES_EXTENSION = '.md'

    # CREATE DATABASE IF NOT EXISTS juliacn DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    SQLALCHEMY_DATABASE_URI = 'mysql://juliacn:somepass@localhost/juliacn?charset=utf8'
    SQLALCHEMY_ECHO = True  # 打开数据库调试模式
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 数据库调试

    # Enable CSRF
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'CSRF KEY juliacn'

    # Settings for sendmail
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'julialang'
    MAIL_PASSWORD = 'dtxpaeftaqxggfve'
    MAIL_SENDER = 'julialang@163.com'
    MAIL_SUBJECT_PREFIX = '[JuliaLang.cn]'
    MAIL_TEST_ACCOUNT = 'adousen@126.com'

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    DEBUG = True
    CSRF_ENABLED= False
    WTF_CSRF_ENABLED = False

    # CREATE DATABASE IF NOT EXISTS juliacn DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://juliacn:somepass@localhost/juliacn_test?charset=utf8'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'default': Config,
    'test': TestConfig,
    'production': ProductConfig,
}