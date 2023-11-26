"""
app
===
The module to make the app.
"""

from flask import Flask

from src import BookShelf


class Config(object):
    SECRET_KEY = 'you-will-never-guess'


config = Config()
app = Flask(__name__)
app.config.from_object(config)

bookshelf = BookShelf()

from . import views
