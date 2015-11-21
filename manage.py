#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil
from datetime import datetime
from project import create_app
from flask.ext.script import Manager, Shell, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

from project.apps.account.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db = app.config['db']
manager = Manager(app)
migrate = Migrate().init_app(app, db)


def _make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
