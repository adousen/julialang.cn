This is a static site blog like Jekyll for Github pages, but it uses python and flask instead of ruby to generate the static pages.

##Installation

1. clone the repo
2. set up virtual environment: `virtualenv venv`
3. activate vitual environment: `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. This one's a little tricky.  If you want to use this generator to set up your own github pages website:
    1. delete the .git folder for this repo (`rm -rf .git`)
    2. reimplement .git folder using direction on the [github pages site](https://pages.github.com/)

##Use

1. `python manage.py runserver`
2. visit `http://localhost:5000`
