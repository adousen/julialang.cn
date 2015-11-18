from flask import Flask
from flask.ext.flatpages import FlatPages
from flask.ext.frozen import Freezer
from flask.ext.bootstrap import Bootstrap
from config import config

import jinja2_highlight

pages = FlatPages()
freezer = Freezer()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    freezer.init_app(app)
    pages.init_app(app)
    bootstrap.init_app(app)

    # register blueprints:
    from apps.website import website as website_blueprint
    app.register_blueprint(website_blueprint)

    return app
