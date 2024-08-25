"""
app
===
The module to make the app.
"""

from flask import Flask

from bookshelf import BookShelf


class Config(object):
    SECRET_KEY = 'you-will-never-guess'


config = Config()
app = Flask(__name__)
app.config.from_object(config)

bookshelf = BookShelf()

from app import views
