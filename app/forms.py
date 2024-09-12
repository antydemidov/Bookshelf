"""
Bookshelf Forms
"""

from typing import TYPE_CHECKING

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (BooleanField, DateField, EmailField, FieldList, FormField,
                     IntegerField, SelectField, StringField, SubmitField,
                     TextAreaField, URLField)
from wtforms.validators import DataRequired, Email, Regexp

from bookshelf.utils import Constants

if TYPE_CHECKING:
    from bookshelf.bookshelf import BookShelf


DISABLED = {'disabled':''}


def build_person_form(data: dict, bs: 'BookShelf'):

    class PersonForm(FlaskForm):

        alternate_name = StringField(bs.locale.get('person:form:alternate_name'))
        description = TextAreaField(bs.locale.get('person:form:description'), render_kw={'rows': 5})
        image = StringField(bs.locale.get('person:form:image'))
        url = StringField(bs.locale.get('person:form:url'))
        additional_name = StringField(bs.locale.get('person:form:additional_name'))
        birth_date = DateField(bs.locale.get('person:form:birth_date'))
        birth_place = StringField(bs.locale.get('person:form:birth_place'))
        death_date = DateField(bs.locale.get('person:form:death_date'))
        death_place = StringField(bs.locale.get('person:form:death_place'))
        email = EmailField(bs.locale.get('person:form:email'), validators=[Email()])
        family_name = StringField(bs.locale.get('person:form:family_name'))
        gender = StringField(bs.locale.get('person:form:gender'))
        given_name = StringField(bs.locale.get('person:form:given_name'))
        member_of = SelectField(bs.locale.get('person:form:member_of'), choices=[])
        nationality = StringField(bs.locale.get('person:form:nationality'))

        submit = SubmitField(bs.locale.get('person:form:submit'), render_kw={'class': 'button'})

    if data.get('member_of', None):
        data['member_of'] = data['member_of']['id']

    form = PersonForm(**data)

    organization_choices = bs.organization_choices()
    form.member_of.choices = organization_choices
    default = organization_choices[0]
    if 'member_of' in data:
        for choice in organization_choices:
            if choice[0] == data['member_of']:
                default = choice
        form.member_of.default = default

    return form


def build_organization_form(data: dict, bs: 'BookShelf'):

    class OrganizationForm(FlaskForm):

        name = StringField(bs.locale.get('organization:form:name'))
        description = TextAreaField(bs.locale.get('organization:form:description'), render_kw={'rows': 5})
        alternate_name = StringField(bs.locale.get('organization:form:alternate_name'))
        image = URLField(bs.locale.get('organization:form:image'))
        url = URLField(bs.locale.get('organization:form:url'))
        address = StringField(bs.locale.get('organization:form:address'))
        email = StringField(bs.locale.get('organization:form:email'), validators=[Email()])
        founding_date = DateField(bs.locale.get('organization:form:founding_date'))
        founding_location = SelectField(bs.locale.get('organization:form:founding_location'), choices=[])
        is_non_profit = BooleanField(bs.locale.get('organization:form:is_non_profit'))
        phone = StringField(bs.locale.get('organization:form:phone'))

        submit = SubmitField(bs.locale.get('organization:form:submit'), render_kw={'class': 'button'})

    return OrganizationForm(**data)


def build_book_form(data: dict, choices: list, bs: 'BookShelf'):
    """Build the form for the book."""

    class BookForm(FlaskForm):

        identifier = StringField(bs.locale.get('book:form:identifier'), render_kw=DISABLED)
        name = StringField(bs.locale.get('book:form:name'), validators=[DataRequired()])
        authors = FieldList(SelectField(), bs.locale.get('book:form:authors'))
        publishers = FieldList(SelectField(), bs.locale.get('book:form:publishers'))
        translators = FieldList(SelectField(), bs.locale.get('book:form:translators'))
        illustrators = FieldList(SelectField(), bs.locale.get('book:form:illustrators'))
        characters = FieldList(SelectField(), bs.locale.get('book:form:characters'))
        description = TextAreaField(bs.locale.get('book:form:description'), render_kw={'rows': 5})
        image = StringField(bs.locale.get('book:form:image'))
        url = URLField(bs.locale.get('book:form:url'))
        badges = SelectField(bs.locale.get('book:form:badges'), default='-', choices=Constants.BADGES.value)
        abstract = TextAreaField(bs.locale.get('book:form:abstract'), render_kw={'rows': 5})
        comment = TextAreaField(bs.locale.get('book:form:comment'), render_kw={'rows': 5})
        content_location = StringField(bs.locale.get('book:form:content_location'))
        content_rating = StringField(bs.locale.get('book:form:content_rating'))
        content_reference_time = StringField(bs.locale.get('book:form:content_reference_time'))
        country_of_origin = StringField(bs.locale.get('book:form:country_of_origin'))
        date_created = DateField(bs.locale.get('book:form:date_created'))
        date_modified = DateField(bs.locale.get('book:form:date_modified'))
        date_published = DateField(bs.locale.get('book:form:date_published'))
        genres = SelectField(bs.locale.get('book:form:genres'))
        in_language = SelectField(bs.locale.get('book:form:in_language'), default='-', choices=['-', 'RU', 'EN'])
        is_accessible_for_free = BooleanField(bs.locale.get('book:form:is_accessible_for_free'))
        is_family_friendly = BooleanField(bs.locale.get('book:form:is_family_friendly'))
        is_in_original_language = BooleanField(bs.locale.get('book:form:is_in_original_language'))
        is_abridged = BooleanField(bs.locale.get('book:form:is_abridged'))
        part_of = SelectField(bs.locale.get('book:form:part_of'))
        keywords = StringField(bs.locale.get('book:form:keywords'))
        license = URLField(bs.locale.get('book:form:license'))
        position = IntegerField(bs.locale.get('book:form:position'))
        thumbnail = URLField(bs.locale.get('book:form:thumbnail'))
        translation_of_work = SelectField(bs.locale.get('book:form:translation_of_work'))
        location_created = SelectField(bs.locale.get('book:form:location_created'))
        book_edition = StringField(bs.locale.get('book:form:book_edition'))
        book_format = SelectField(bs.locale.get('book:form:book_format'), default='-', choices=Constants.BOOK_FORMATS.value)
        isbn = StringField(bs.locale.get('book:form:isbn'))
        number_of_pages = IntegerField(bs.locale.get('book:form:number_of_pages'))
        file_size = StringField(bs.locale.get('book:form:file_size'), render_kw=DISABLED)
        file_type = StringField(bs.locale.get('book:form:file_type'), render_kw=DISABLED)

        submit = SubmitField(bs.locale.get('book:form:submit'), render_kw={'class': 'button'})


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


def build_filter_form(bs: 'BookShelf'):

    class FilterForm(FlaskForm):

        year = IntegerField(bs.locale.get('filter:form:year'))
        author = SelectField(bs.locale.get('filter:form:author'), choices=[])
        genre = StringField(bs.locale.get('filter:form:genre'))
        keyword = StringField(bs.locale.get('filter:form:keyword'))
        isbn = StringField(bs.locale.get('filter:form:isbn'))
        language = SelectField(bs.locale.get('filter:form:language'), choices=[])
        badge = SelectField(bs.locale.get('filter:form:badge'), choices=Constants.BADGES.value)

        submit = SubmitField(bs.locale.get('filter:form:submit'), render_kw={'class': 'button'})


    return FilterForm()


def build_file_form(bs: 'BookShelf'):

    class FileForm(FlaskForm):

        file = FileField(bs.locale.get('file:form:file'), name='file', validators=[FileRequired()])

        submit = SubmitField(bs.locale.get('file:form:submit'), render_kw={'class': 'button'})

    return FileForm()


def build_settings_form(data: dict, bs: 'BookShelf'):

    class OtherIDsForm(FlaskForm):

        id_type = StringField(
            bs.locale.get('settings:form:id_type'),
            validators=[DataRequired()],
            render_kw = {'class': 'info-form-field-row-type'}
        )
        url = StringField(
            bs.locale.get('settings:form:url'),
            validators=[DataRequired(), Regexp(
                r'{placeholder}', message=r'Must contain "{placeholder}"')],
            render_kw = {'class': 'info-form-field-row-url'}
        )


    class SettingsForm(FlaskForm):

        default_picture = StringField(bs.locale.get('settings:form:default_picture'))
        other_ids_links = FieldList(FormField(OtherIDsForm, 'ID'),
                                    bs.locale.get('settings:form:other_ids_links'))

        submit = SubmitField(bs.locale.get('settings:form:submit'), render_kw={'class': 'button'})


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
