#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil
from datetime import datetime
from project import create_app
from project.extensions import freezer
from flask.ext.script import Manager, Shell, prompt_bool

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def freeze(debug=False):
    if debug:
        freezer.run(debug=True)
    freezer.freeze()

from config import basedir
pagesdir = os.path.join(basedir, 'pages')

@manager.command
def new_post(title):
    """
    creates a new file in 'pages' directory with 
    indicated title, formatted yaml header, and opens
    new file in sublime text editor
    """
    
    yaml_header = 'title: %s' % title + '\n' +\
                  'date: %s' % datetime.now()[:-7] + '\n\n'
    
    filename = title.replace(' ','_') + '.md'
    filepath = os.path.join(pagesdir, filename)
    with open(filepath, 'w') as thefile:
        thefile.write(yaml_header)
    os.system("subl %s" % filepath)


if __name__ == '__main__':
    manager.run()
