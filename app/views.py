"""Here must be the string"""
from flask import render_template, send_file
from .utils import get_size_format

from . import app, bookshelf


@app.route('/')
def index():
    title = '🌠 Bookshelf'
    heading = 'Welcome'
    content = get_size_format(bookshelf.get_size())
    return render_template(
        'index.html',
        title=title,
        heading=heading,
        content=content,
        books=bookshelf.books
    )


@app.route('/book/<_id>')
def book_page(_id):
    _id = int(_id)
    book = bookshelf[_id]
    title = f'🌠 Bookshelf | {book.title}'
    return render_template(
        'book.html',
        title=title,
        heading=book.title,
        book=book
    )


@app.route('/file/<_id>')
def get_file(_id):
    _id = int(_id)
    book = bookshelf[_id]
    return send_file(book.abs_path)
