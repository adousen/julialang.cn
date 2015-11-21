#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from extensions import pages, bootstrap, db, login_manager, moment, mail, sendmail


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.jinja_env.add_extension('jinja2_highlight.HighlightExtension')

    # register extensions
    configure_extensions(app)

    # register blueprints:
    from apps.website import website as website_blueprint
    app.register_blueprint(website_blueprint)

    return app


def configure_extensions(app):
    pages.init_app(app)

    bootstrap.init_app(app)
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True

    db.init_app(app)
    db.echo = app.config['DB_ECHO']

    login_manager.init_app(app)
    app.config['ext_login_manager'] = login_manager

    moment.init_app(app)

    mail.init_app(app)
    app.config['ext_mail'] = mail

    sendmail.init_app(app)
    app.config['contrib_sendmail'] = sendmail
