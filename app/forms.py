"""
Bookshelf Forms
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (BooleanField, DateField, EmailField, FieldList, FormField,
                     IntegerField, SelectField, StringField, SubmitField,
                     TextAreaField, URLField)
from wtforms.validators import DataRequired, Email, Regexp

from bookshelf.utils import Constants

DISABLED = {'disabled':''}


class PersonForm(FlaskForm):

    alternate_name = StringField('Alternate Name')
    description = TextAreaField('Description', render_kw={'rows': 5})
    image = StringField('Image')
    url = StringField('URL')
    additional_name = StringField('Additional Name')
    birth_date = DateField('Birth Date')
    birth_place = StringField('Birth Place')
    death_date = DateField('Death Date')
    death_place = StringField('Death Place')
    email = EmailField('Email', validators=[Email()])
    family_name = StringField('Family Name')
    gender = StringField('Gender')
    given_name = StringField('Given Name')
    member_of = SelectField('Member Of', choices=[])
    nationality = StringField('Nationality')

    submit = SubmitField('Save')


class OrganizationForm(FlaskForm):

    name = StringField('Name')
    description = TextAreaField('Description', render_kw={'rows': 5})
    alternate_name = StringField('Alternate Name')
    image = URLField('Image')
    url = URLField('URL')
    address = StringField('Address')
    email = StringField('Email', validators=[Email()])
    founding_date = DateField('Founding Date')
    founding_location = SelectField('Founding Location', choices=[])
    is_non_profit = BooleanField('Is Non-profit')
    phone = StringField('Phone')

    submit = SubmitField('Save')


class BookForm(FlaskForm):

    identifier = StringField('Identifier', render_kw=DISABLED)
    name = StringField('Title', validators=[DataRequired()])
    authors = FieldList(SelectField('Authors'), label='Authors')
    publishers = FieldList(SelectField('Publishers'), label='Publishers')
    translators = FieldList(SelectField('Translators'), label='Translators')
    illustrators = FieldList(SelectField('Illustrators'), label='Illustrators')
    characters = FieldList(SelectField('Characters'), label='Characters')
    description = TextAreaField('Description', render_kw={'rows': 5})
    image = StringField('Image')
    url = URLField('Url')
    badges = SelectField('Badges', default='-', choices=Constants.BADGES.value)
    abstract = TextAreaField('Abstract', render_kw={'rows': 5})
    comment = TextAreaField('Comment', render_kw={'rows': 5})
    content_location = StringField('Content Location')
    content_rating = StringField('Content Rating')
    content_reference_time = StringField('Content Reference Time')
    country_of_origin = StringField('Country of Origin')
    date_created = DateField('Date Created')
    date_modified = DateField('Date Modified')
    date_published = DateField('Date Published')
    genres = SelectField('Genres', default='-', choices=[])
    in_language = SelectField('In Language', default='-', choices=['-', 'RU', 'EN'])
    is_accessible_for_free = BooleanField('Is Accessible For Free')
    is_family_friendly = BooleanField('Is Family Friendly')
    is_in_original_language = BooleanField('Is in Original Language')
    is_abridged = BooleanField('Is Abridged')
    part_of = SelectField('Part of', default='-', choices=[])
    keywords = StringField('Keywords')
    license = URLField('License')
    position = IntegerField('Position')
    thumbnail = URLField('Thumbnail')
    translation_of_work = SelectField('Translation of Work', default='-', choices=[])
    location_created = SelectField('Location Created', default='-', choices=[])
    book_edition = StringField('Book Edition')
    book_format = SelectField('Book Format', default='-', choices=Constants.BOOK_FORMATS.value)
    isbn = StringField('ISBN')
    number_of_pages = IntegerField('Number of Pages')
    file_size = StringField('File Size', render_kw=DISABLED)
    file_type = StringField('File Type', render_kw=DISABLED)

    # submit = SubmitField('Save')


def build_book_form(data: dict, choices: list):
    """Build the form for the book."""

    form_data = data.copy()
    default = choices[0]

    for field_title in Constants.PERS_ORG_TYPES.value:
        field_name = field_title.lower() + 's'
        del form_data[field_name]

    form = BookForm(**form_data)

    for field_title in Constants.PERS_ORG_TYPES.value:
        field_name = field_title.lower() + 's'
        field_data = data[field_name]
        field_list = getattr(form, field_name)
        if not field_data:
            field = field_list.append_entry('0')
            field.choices = choices
            field.default = choices[0]
        else:
            for item in field_data:
                choice_id = str(item['id']) + ':' + item['type']
                for choice in choices:
                    if choice[0] == choice_id:
                        default = choice
                field = field_list.append_entry(choice_id)
                field.choices = choices
                field.default = default

    return form


class FilterForm(FlaskForm):

    year = IntegerField('Year')
    author = SelectField('Author', choices=[])
    genre = StringField('Genre')
    keyword = StringField('Keyword')
    isbn = StringField('ISBN')
    language = SelectField('Language', choices=[])
    badge = SelectField('Badge', choices=Constants.BADGES.value)

    # submit = SubmitField('Search')


class FileForm(FlaskForm):

    file = FileField('File', name='file', validators=[FileRequired()])

    # submit = SubmitField('Upload')


class OtherIDsForm(FlaskForm):

    id_type = StringField('Type', validators=[DataRequired()],
                          render_kw = {'class': 'info-form-field-row-type'})
    url = StringField('URL', validators=[DataRequired(), Regexp(
        r'{placeholder}', message=r'Must contain "{placeholder}"')],
                      render_kw = {'class': 'info-form-field-row-url'})


class SettingsForm(FlaskForm):

    default_picture = StringField()
    other_ids_links = FieldList(FormField(OtherIDsForm, 'ID'), 'IDs')


def build_settings_form(data: dict):

    form_data = {'default_picture': data.copy().pop('default_picture')}

    form = SettingsForm(**form_data)

    field_name = 'other_ids_links'
    field_data = data[field_name]
    field_list: FieldList = getattr(form, field_name)
    if not field_data:
        field_list.append_entry('0')
    else:
        for key, value in field_data.items():
            field_list.append_entry(
                {
                    'id_type': key,
                    'url': value
                }
            )

    return form
