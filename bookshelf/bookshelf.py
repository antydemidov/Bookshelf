"""Bookshelf Internal Module."""

# import csv
# import json
import os
from datetime import date, datetime

from bookshelf import utils
from bookshelf.database import Database
# from bookshelf.handlers import PDFFile
from bookshelf.models import BookModel, OrganizationModel, PersonModel


class Person:
    """Person representation for authors, translators, editors, etc."""

    def __init__(self, data: dict, database: Database):
        self._id = int(data['id'])
        self.database = database
        self.data = None
        self.years_str = None
        self.pic_url = None

        if data.get('full_name', None):
            data['full_name'] = utils.get_full_name(data)
        self.process(data)

    def get_id(self):
        return self._id

    def process(self, data: dict):
        self.data = PersonModel.model_validate(data)
        birth_date = self.data.birth_date.year if isinstance(
            self.data.birth_date, (date, datetime)) else 'n.d.'
        death_date = self.data.death_date.year if isinstance(
            self.data.death_date, (date, datetime)) else 'n.d.'
        self.years_str = f'{birth_date} ‒ {death_date}'
        self.pic_url = self.data.image
        if not self.pic_url:
            self.pic_url = utils.Constants.DEFAULT_PICTURE.value

    def update_record(self, data: dict):
        data = utils.clean_dict_from_none(data)
        data['full_name'] = utils.get_full_name(data)
        if 'member_of' in data:
            org_data = data.pop('member_of', None)
        data = self.data.model_copy(update=data).model_dump()
        if org_data:
            data['member_of'] = int(org_data)
        self.database.update_person(self._id, data)
        self.process(self.database.get_person(self._id))


class Persons:
    """Person manager."""

    def __init__(self, database: Database):
        self.database = database
        data = self.database.get_persons()
        self.persons = [self.get_person_obj(item) for item in data]

    def get_person(self, _id: int):
        for value in self.persons:
            if value.get_id() == _id:
                return value
        return None

    def get_person_obj(self, data: dict):

        person_id = data.get('id', None)
        if not person_id:
            return None
        return Person(data, self.database)

    def find_person(self, _id: int):

        data = self.database.get_person(_id)
        return self.get_person_obj(data)

    def list_full_names(self):

        names = [utils.get_full_name(person.data.model_dump(
            exclude_defaults=True)) for person in self.persons]
        return names

    def create_person(self):
        _id = self.database.add_person({'name': 'New Person'})
        data = self.database.get_person(_id)
        person = self.get_person_obj(data)
        self.persons.append(person)
        return _id

    def add_person(self, data: dict):

        if 'member_of' in data:
            org_data = self.database.get_organization(data['member_of'])
            data['member_of'] = None
            if org_data:
                data['member_of'] = org_data[0]

        person = PersonModel.model_validate(data)
        data = person.model_dump(exclude_defaults=True)
        if 'member_of' in data:
            data['member_of'] = data['member_of']['id']
        person_id = self.database.add_person(data)
        data = self.database.get_person(person_id)
        self.persons.append(self.get_person_obj(data))

    def delete_person(self, _id: int):
        self.database.delete_person(_id)
        for k, value in enumerate(self.persons):
            if value.get_id() == _id:
                del self.persons[k]


class Organization:
    """Represents the Organization object."""

    def __init__(self, data: dict, database: Database):
        self._id = int(data['id'])
        self.data = OrganizationModel.model_validate(data)
        self.database = database
        self.pic_url = self.data.image
        if not self.pic_url:
            self.pic_url = utils.Constants.DEFAULT_PICTURE.value

    def get_id(self):
        return self._id

    def update_record(self, data: dict):

        data = utils.clean_dict_from_none(data)
        data = self.data.model_copy(update=data).model_dump()
        self.database.update_organization(self._id, data)
        self.data = self.data.model_validate(self.database.get_organization(self._id))
        self.pic_url = self.data.image
        if not self.pic_url:
            self.pic_url = utils.Constants.DEFAULT_PICTURE.value


class Organizations:
    """Organizations manager."""

    def __init__(self, database: Database):
        self.database = database
        self.organizations = []
        data = self.database.get_organizations()
        if data:
            self.organizations = [self.get_organization_obj(item) for item in data]

    def get_organization(self, _id: int):

        for organization in self.organizations:
            if organization.get_id() == _id:
                return organization
        return None

    def get_organization_obj(self, data: dict):

        if not data.get('id', None):
            return None
        return Organization(data, self.database)

    def delete_organization(self, _id: int):
        self.database.delete_organization(_id)
        for k, value in enumerate(self.organizations):
            if value.get_id() == _id:
                del self.organizations[k]

    def create_organization(self):

        _id = self.database.add_organization({'name': 'New Organization'})
        data = self.database.get_organization(_id)
        organization = self.get_organization_obj(data)
        self.organizations.append(organization)
        return _id

    def add_organization(self, data: dict):

        organization = OrganizationModel.model_validate(data)
        data = organization.model_dump(exclude_defaults=True)
        organization_id = self.database.add_person(data)
        data = self.database.get_person(organization_id)
        self.organizations.append(self.get_organization_obj(data))

    def list_names(self):

        return [organization.data.name for organization in self.organizations]


class Book:
    """Represents the Book object."""

    def __init__(self, _id: int, data: dict, database: Database):
        self._id = _id

        for key, value in data.items():
            if value == '':
                data[key] = None
        self.data = BookModel.model_validate(data)

        path = os.path.join(utils.Constants.LIBRARY_DIR.value,
                            f'{self.data.identifier}.pdf')
        if os.path.exists(path):
            self.data.file_size = os.stat(path).st_size
            self.data.file_type = 'pdf'

        self.database = database
        self.authors_str = '; '.join([author['title'] for author in self.data.authors])

    def get_id(self):
        return self._id

    # def get_file(self):
    #     """Returns the special object for the each kind of files."""

    #     if self.extension == '.pdf':
    #         file = PDFFile(self.path)
    #     elif self.extension in ['.docx', '.doc']:
    #         file = DOCXFile(self.path)
    #     elif self.extension == '.djvu':
    #         file = DJVUFile(self.path)
    #     return file

    def update(self, data: dict):

        pers_book_records = []
        org_book_records = []

        for key, value in data.items():
            if key.startswith('is_'):
                data[key] = value not in [False, 'False', 'false', '']

        for key, value in data.items():
            if value in ['-', '0', None, 'None', '']:
                data[key] = None

        for pers_org_type in utils.Constants.PERS_ORG_TYPES.value:
            field_name = pers_org_type.lower() + 's'
            for key, value in data.items():
                if field_name in key and value:
                    _id, _type = int(value.split(':')[0]), value.split(':')[1]
                    if _type == 'person':
                        row_value = {
                            'book_id': self._id,
                            'person_id': _id,
                            'type': pers_org_type
                        }
                        pers_book_records.append(row_value)
                    elif _type == 'organization':
                        row_value = {
                            'book_id': self._id,
                            'organization_id': _id,
                            'type': pers_org_type
                        }
                        org_book_records.append(row_value)

        self.database.delete_query('BooksPersons', 'book_id', self._id)
        for pers_book_record in pers_book_records:
            self.database.insert_query('BooksPersons', pers_book_record)

        self.database.delete_query('BooksOrganizations', 'book_id', self._id)
        for org_book_record in org_book_records:
            self.database.insert_query('BooksOrganizations', org_book_record)

        excluded_fields = [item.lower() + 's' for item in utils.Constants.PERS_ORG_TYPES.value]
        data = self.data.model_copy(update=data).model_dump(
            exclude=excluded_fields, exclude_defaults=True, exclude_none=True)

        self.database.update_book(self._id, data)
        data = self.database.get_book(self._id)
        self.data = self.data.model_validate(data)
        self.authors_str = '; '.join([author['title'] for author in self.data.authors])


class Books:
    """Books manager."""

    def __init__(self, database: Database):
        self.database = database
        data = self.database.get_books()
        self.books = [self.get_book_obj(item) for item in data]

    def clean_library(self):
        """Deletes files without records in the database."""

        books_ids = [book.data.identifier for book in self.books]

        for file in os.scandir(utils.Constants.LIBRARY_DIR.value):
            if file.name.split('.')[0] not in books_ids:
                os.remove(file.path)

    def get_book(self, _id: int = None, uuid: str = None):

        for book in self.books:
            if book.get_id() == _id or book.data.identifier == uuid:
                return book

    def get_book_obj(self, data: dict):

        book_id = data.pop('id')
        if not book_id:
            return None
        return Book(book_id, data, self.database)

    def get_books(self, author_id: int = None):
        if not author_id:
            return self.books
        books = []
        for book in self.books:
            for author in book.data.authors:
                if author['id'] == author_id:
                    books.append(book)
        return books

    def add_book(self, data: dict):
        """Adds a book into the database."""

        for pers_org_type in utils.Constants.PERS_ORG_TYPES.value:
            field = pers_org_type.lower() + 's'
            if field in data:
                for item in data.pop(field):
                    book_person = {'book_id': data['id'],
                                   'person_id': item['id'],
                                   'type': pers_org_type}
                    self.database.insert_query('BooksPersons', book_person)

        book = BookModel.model_validate(data)
        book_id = self.database.add_book(book.model_dump(exclude_defaults=True))
        data = self.database.get_book(book_id)
        book = self.get_book_obj(data)
        self.books.append(book)
        return book

    def add_book_from_file(self, data):

        identifier = utils.generate_uuid()
        file_name = identifier + '.pdf'
        file_path = os.path.join(utils.Constants.LIBRARY_DIR.value, file_name)
        with open(file_path, 'wb') as file:
            file.write(data)
        book_id = self.database.add_book({'identifier': identifier})
        data = self.database.get_book(book_id)
        if not data:
            return None
        book = self.get_book_obj(data)
        self.books.append(book)
        return book

    def import_from_directory(self, directory: str):
        """Copies all files from the given directory to the directory of library
        and adds it into the database."""

        for file in os.scandir(directory):
            if file.path.split('.')[-1] in utils.Constants.FILE_TYPES.value:
                with open(file.path, 'rb') as src_file:
                    self.add_book_from_file(src_file.read())

    def list_book_titles(self):
        """Returns a list of book titles."""

        return [book.data.name for book in self.books]

    def delete_book(self, uuid: str):
        book = self.get_book(uuid=uuid)
        self.database.delete_book(book.get_id())
        for k, value in enumerate(self.books):
            if value.data.identifier == uuid:
                del self.books[k]
        path = os.path.join(utils.Constants.LIBRARY_DIR.value, f'{uuid}.pdf')
        if os.path.exists(path):
            os.remove(path)


class BookShelf:
    """Represents your library."""

    def __init__(self) -> None:
        self.database = Database()
        self.books = Books(self.database)
        self.persons = Persons(self.database)
        self.organizations = Organizations(self.database)

    # def get_settings(self):
    #     """Loads settings from the settings file."""

    #     with open(utils.Constants.SETTINGS_FILE, 'r', encoding='utf8') as f:
    #         settings = json.load(f)
    #     return settings

    def get_size(self):
        """Description."""

        size = 0
        for file in os.scandir(utils.Constants.LIBRARY_DIR.value):
            size += file.stat().st_size
        return size

    def book_choices(self):

        book_choices = [(0, '-')] + [(book.get_id(), book.data.name) for book in self.books.books]
        return book_choices

    def person_choices(self):

        person_org_list = [(0, '-')]
        for person in self.persons.persons:
            person_org_list.append((person.get_id(), person.data.full_name))
        return person_org_list

    def pers_org_choices(self):

        person_org_list = [('0', '-')]
        for person in self.persons.persons:
            full_name = person.data.full_name
            if not full_name:
                full_name = 'Unknown'
            person_org_list.append((f'{person.get_id()}:person',
                                    full_name + ' (Person)'))
        for organization in self.organizations.organizations:
            person_org_list.append((f'{organization.get_id()}:organization',
                                    organization.data.name + ' (Organization)'))
        return person_org_list

    def organization_choices(self):

        person_org_list = [(0, '-')]
        for organization in self.organizations.organizations:
            person_org_list.append((organization.get_id(), organization.data.name))
        return person_org_list

    # def scan_library(self, file_types: str | list[str] = None) -> list[Book]:
    #     """
    #     Scanning the folder specified as a library.
        
    #     Parameters
    #     ----------
    #     file_types : str or list[str]
    #         File types to scan in the library folder. You must enter the
    #         extensions in the format like '.pdf', '.djvu', etc.
    #     """

    #     lst = []
    #     scan = os.scandir(utils.Constants.LIBRARY_DIR)

    #     if isinstance(file_types, str):
    #         file_types = [file_types]

    #     if file_types is None:
    #         for file in scan:
    #             if file.is_file():
    #                 lst.append(file.path)
    #     else:
    #         for file in scan:
    #             if (file.is_file() and
    #                 os.path.splitext(file.path)[1].lower() in file_types):
    #                 lst.append(file.path)

    #     books = [self.get_book(_id, uuid) for path in lst]
    #     return books

    # def __iter__(self):
    #     for book in self.books:
    #         yield book

    # def __getitem__(self, index: int | str) -> Book:
    #     for book in self.books:
    #         if book._id == index or book.identifier == index:
    #             return book
    #     return None

    # def __len__(self):
    #     return len(self.books)

    # def __bool__(self):
    #     return len(self) > 0

    # --------------------------------
    # ============ EXPORT ============
    # --------------------------------

    # def export_to_csv(self, path: str = None):
    #     """Exports the library to a CSV file."""

    #     data = []
    #     dt = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    #     for book in self.books:
    #         data.append(book.file.get_metadata())
    #     default_path = f'./reports/library_{dt}.csv'
    #     folder = os.path.dirname(default_path)
    #     if not os.path.exists(folder):
    #         os.mkdir(folder)
    #     path = path or default_path
    #     if len(data) != 0:
    #         with open(path, 'w', newline='', encoding='utf-8') as csvfile:
    #             fieldnames = list(data[0].keys())
    #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #             writer.writeheader()
    #             for item in data:
    #                 writer.writerow(item)

    # def export_to_bib(): ...
