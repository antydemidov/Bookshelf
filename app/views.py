"""Here must be the string"""
from flask import redirect, render_template, send_file, request
from werkzeug.datastructures import MultiDict
from app.forms import PdfForm

from . import app, bookshelf
from .utils import get_size_format


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


@app.route('/book/<_id>', methods=['GET', 'POST'])
def book_page(_id):
    _id = int(_id)
    book = bookshelf[_id]
    title = f'🌠 Bookshelf | {book.title}'
    data = MultiDict([(k, v) for k, v in book.get_properties().items()])
    form = PdfForm(formdata=data)
    if form.is_submitted():
        result = dict(request.form)
        for k, v in result.items():
            if k != 'csrf_token':
                setattr(book, k, v)
        return redirect(f'/book/{_id}')
    return render_template(
        'book.html',
        title=title,
        heading=book.title,
        book=book,
        form=form
    )


@app.route('/file/<_id>')
def get_file(_id):
    _id = int(_id)
    book = bookshelf[_id]
    return send_file(book.abs_path)
