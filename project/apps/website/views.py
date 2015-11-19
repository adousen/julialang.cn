from flask import render_template, render_template_string
from flask_flatpages.utils import pygmented_markdown

from . import website
from project import pages, freezer


def my_renderer(text):
    prerendered_body = render_template_string(text)
    return prerendered_body


@website.route('/')
def home():
    # posts = [page for page in pages]
    # Sort pages by date
    # sorted_posts = sorted(posts, reverse=True,
    #     key=lambda page: page.meta['date'])
    # return render_template('website/_layouts/default.html', pages=sorted_posts)
    page = pages.get_or_404('index')
    page_content = my_renderer(page.html)
    return render_template('website/_layouts/default.html', page=page.meta, content=page_content)


@website.route('/<any(downloads, community, learning, teaching, publications, jsoc):category>/')
@website.route('/<any(downloads, community, learning, teaching, publications, jsoc):category>/<path:path>/')
def page(category, path='index'):
    # 'path is the filename of a page, without the file extension'
    # e.g. "first-post"
    page = pages.get_or_404(category + '/' + path)
    page_content = my_renderer(page.html)
    return render_template('website/_layouts/default.html', page=page.meta, content=page_content)


