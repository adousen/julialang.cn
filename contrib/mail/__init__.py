#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'adousen'

from threading import Thread

from flask import current_app, Blueprint
from flask.ext.mail import Message
from flask import render_template


class SendMail(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint('contrib_mail', __name__, template_folder='templates')
        app.register_blueprint(blueprint)

    def send_email(self, to, subject, template, **kwargs):
        app = current_app._get_current_object()
        msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr


def send_async_email(app, msg):
    mail = app.config['ext_mail']

    with app.app_context():
        mail.send(msg)


