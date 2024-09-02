"""Here must be the string"""
# import os

from flask import redirect, render_template, send_file, request

from app import app, bookshelf, utils
from app.forms import (OrganizationForm, PersonForm, FileForm,
                       build_book_form, build_settings_form)


@app.route('/')
def index():
    """
    The main page.
    """

    title = '🌠 Bookshelf: a manager for your books'
    heading = 'Welcome! This is your library :)'
    content = '; '.join(['Directory size: ' + utils.get_size_format(bookshelf.get_size()),
                         'Number of books: ' + str(len(bookshelf.books.books)),
                         'Number of files: ' + str(4)])  # TODO: count files in the directory
    return render_template(
        'index.html',
        title=title,
        heading=heading,
        content=content,
        books=bookshelf.books.books
    )


@app.route('/books')
def books():
    """
    The page of books.

    Features
    --------
    """

    title = '🌠 Bookshelf | Books'
    heading = 'Books'

    author_id = request.args.get('author_id', None, int)
    books_list = bookshelf.books.get_books(author_id)

    return render_template(
        'books.html',
        title=title,
        heading=heading,
        books=books_list
    )


@app.route('/book/<uuid>', methods=['GET', 'POST'])
def book(uuid: str):
    """
    Book page

    Features
    --------
    - Properties of the book;
    - Reading of the book;
    - Detailed book management.
    """

    book_obj = bookshelf.books.get_book(uuid=uuid)
    title = f'🌠 Bookshelf | {book_obj.data.name}'
    view_url = f'/file/{uuid}'
    delete_url = f'/book/{uuid}/delete'
    data = book_obj.data.model_dump()
    data['file_size'] = utils.get_size_format(data['file_size'])
    pers_org_choices = bookshelf.pers_org_choices()
    form = build_book_form(data, pers_org_choices)

    book_choices = bookshelf.book_choices()
    form.part_of.choices = book_choices
    form.translation_of_work.choices = book_choices

    if request.method == 'POST':
        result = request.form.to_dict()
        if 'file_size' in result:
            result.pop('file_size')
        book_obj.update(result)
        return redirect(f'/book/{book_obj.data.identifier}')

    return render_template(
        'book.html',
        title=title,
        delete_url=delete_url,
        view_url=view_url,
        book=book_obj,
        form=form
    )


@app.route('/book/<uuid>/delete')
def delete_book(uuid: str):
    bookshelf.books.delete_book(uuid)
    return redirect('/books')


@app.route('/person/<_id>/delete')
def delete_person(_id):
    _id = int(_id)
    bookshelf.persons.delete_person(_id)
    return redirect('/persons')


@app.route('/organization/<_id>/delete')
def delete_organization(_id):
    _id = int(_id)
    bookshelf.organizations.delete_organization(_id)
    return redirect('/organizations')


@app.route('/clean_library')
def clean_library():

    bookshelf.books.clean_library()
    return redirect('/books')


@app.route('/add_person')
def add_person():

    _id = bookshelf.persons.create_person()
    return redirect(f'/person/{_id}')


@app.route('/add_organization')
def add_organization():

    _id = bookshelf.organizations.create_organization()
    return redirect(f'/organization/{_id}')


@app.route('/file/<uuid>')
def get_file(uuid):

    return send_file('../library/' + uuid + '.pdf')


@app.route('/upload', methods=['GET', 'POST'])
def upload_book():
    title = '🌠 Bookshelf | Upload file'
    form = FileForm()
    if request.method == 'POST':
        if form.file.data:
            file_data = form.file.data.stream.read()
            book_obj = bookshelf.books.add_book_from_file(file_data)
            return redirect(f'/book/{book_obj.data.identifier}')
    return render_template(
        'upload_book.html',
        title=title,
        form=form
    )


@app.route('/persons')
def persons():

    title = '🌠 Bookshelf | Persons'
    heading = 'Persons'

    return render_template(
        'persons.html',
        title=title,
        heading=heading,
        persons=bookshelf.persons.persons
    )


@app.route('/person/<_id>', methods=['GET', 'POST'])
def person(_id: str):

    _id = int(_id)
    person_obj = bookshelf.persons.get_person(_id)
    title = f'🌠 Bookshelf | {person_obj.data.full_name}'
    delete_url = f'/person/{_id}/delete'
    data = person_obj.data.model_dump()
    if data.get('member_of', None):
        data['member_of'] = data['member_of']['id']
    form = PersonForm(**data)
    pic_url = person_obj.data.image
    if not pic_url:
        pic_url = '../static/person_default.png'

    organization_choices = bookshelf.organization_choices()
    form.member_of.choices = organization_choices
    if person_obj.data.member_of:
        for choice in organization_choices:
            if choice[0] == person_obj.data.member_of.id:
                default = choice
        form.member_of.default = default

    if request.method == 'POST':
        data = request.form.to_dict()
        person_obj.update_record(data)
        return redirect(f'/person/{_id}')

    return render_template(
        'person.html',
        title=title,
        person=person_obj,
        pic_url=pic_url,
        delete_url=delete_url,
        form=form
    )


@app.route('/organizations')
def organizations():
    """
    The page of books.

    Features
    --------
    """

    title = '🌠 Bookshelf | Organizations'
    heading = 'Organizations'

    organizations_list = bookshelf.organizations.organizations

    return render_template(
        'organizations.html',
        title=title,
        heading=heading,
        organizations=organizations_list
    )


@app.route('/organization/<_id>', methods=['GET', 'POST'])
def organization(_id: int):

    _id = int(_id)
    organization_obj = bookshelf.organizations.get_organization(_id)
    title = f'🌠 Bookshelf | {organization_obj.data.name}'
    data = organization_obj.data.model_dump()
    delete_url = f'/organization/{_id}/delete'
    form = OrganizationForm(**data)
    pic_url = organization_obj.data.image
    if not pic_url:
        pic_url = '../static/person_default.png'

    if request.method == 'POST':
        data = request.form.to_dict()
        organization_obj.update_record(data)
        return redirect(f'/organization/{_id}')

    return render_template(
        'organization.html',
        title=title,
        pic_url=pic_url,
        organization=organization_obj,
        delete_url=delete_url,
        form=form
    )


@app.route('/settings', methods=['GET', 'POST'])
def settings():

    data = bookshelf.settings.data.model_dump()
    form = build_settings_form(data)

    if request.method == 'POST':
        data = request.form.to_dict()
        bookshelf.settings.update(data)
        return redirect('/settings')

    return render_template(
        'settings.html',
        form=form
    )


@app.errorhandler(Exception)
def error_page(error):
    title = f'🌠 Bookshelf | {error}'
    return render_template('error.html', title=title, error=error)
