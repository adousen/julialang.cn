from flask import Flask
from flask.ext.flatpages import FlatPages
from flask.ext.frozen import Freezer
from flask.ext.bootstrap import Bootstrap
from config import config

from flask.ext.flatpages import Page
import operator
from itertools import takewhile
from werkzeug.utils import import_string


class myFlatPages(FlatPages):
    def _parse(self, content, path):
        """Parse a flatpage file, i.e. read and parse its meta data and body.

        :return: initialized :class:`Page` instance.
        """
        lines = iter(content.split('\n'))

        # Read lines until an empty line is encountered.
        meta = '\n'.join(takewhile(operator.methodcaller('strip'), lines)).strip('---\n')
        # The rest is the content. `lines` is an iterator so it continues
        # where `itertools.takewhile` left it.
        content = '\n'.join(lines)

        # Now we ready to get HTML renderer function
        html_renderer = self.config('html_renderer')

        # If function is not callable yet, import it
        if not callable(html_renderer):
            html_renderer = import_string(html_renderer)

        # Make able to pass custom arguments to renderer function
        html_renderer = self._smart_html_renderer(html_renderer)

        # Initialize and return Page instance
        return Page(path, meta, content, html_renderer)

pages = myFlatPages()
freezer = Freezer()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.jinja_env.add_extension('jinja2_highlight.HighlightExtension')

    freezer.init_app(app)
    pages.init_app(app)
    bootstrap.init_app(app)

    # register blueprints:
    from apps.website import website as website_blueprint
    app.register_blueprint(website_blueprint)

    return app
