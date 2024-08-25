"""Database manipulations."""

import sqlite3

from bookshelf import utils
from bookshelf.utils import Constants


class Database:
    """Database."""

    def __init__(self, database_name: str = None):
        if not database_name:
            database_name = Constants.DATABASE_NAME.value
        self.database_name = database_name

    def setup_database(self):
        """Sets up tables in the database."""

        with sqlite3.connect(self.database_name) as database:
            database.execute('PRAGMA foreign_keys = ON')
            cursor = database.cursor()
            for table_name in Constants.TABLES_LIST.value:
                command = utils.read_sql(table_name)
                cursor.execute(command)
            database.commit()

    def query(self, sql: str, data = None):
        """The query the operation on the given table."""

        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            row_id = cursor.lastrowid
            db.commit()
        if not row_id:
            return 0
        return row_id

    def select_query(self, sql: str, data = None):
        """The query for the select operation on the given table."""

        with sqlite3.connect(self.database_name) as db:
            cursor = db.cursor()
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            field_list = [i[0] for i in cursor.description]
            results = [dict(zip(field_list, data)) for data in cursor.fetchall()]
        return results

    def insert_query(self, table_name: str, data: dict):
        """Inserts new record into the database. Returns the last row id."""

        fields = data.keys()
        value_points = ', '.join(['?'] * len(fields))
        sql = f'INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({value_points})'
        row_id = self.query(sql, tuple(data.values()))
        return row_id

    def update_query(self, table_name: str, _id: int, data: dict):
        """The query for the update operation on the given table."""

        field_list = ', '.join(data.keys())
        value_questions = ', '.join(['?'] * len(data.keys()))
        sql = f'''UPDATE {table_name}
        SET ({field_list}) = ({value_questions})
        WHERE id = {_id}'''
        self.query(sql, tuple(data.values()))

    def delete_query(self, table: str, column: str, value):
        """The query to delete records from the table."""
        sql = f'DELETE FROM {table} WHERE {column} = "{value}"'
        return self.query(sql)

    def check_book(self, title: str = None, isbn: str = None, fields: list[str] = None):
        """Checks if the book is already exists."""

        result = None
        if not fields:
            fields = ['id']
        fields = ', '.join(fields)

        if title:
            result = self.select_query(f'SELECT {fields} FROM Books WHERE name = "{title}";')
        if isbn:
            result = self.select_query(f'SELECT {fields} FROM Books WHERE isbn = "{isbn}";')
        if result:
            return result
        return None

    def check_person(self, given_name: str = None, family_name: str = None,
                     birth_year: int = None):
        """Checks if the person is already exists."""

        if given_name and family_name and birth_year:
            sql = f'''SELECT id
            FROM Persons
            WHERE given_name = "{given_name}"
                AND family_name = "{family_name}"
                AND strftime("%Y", birth_date) = {birth_year};'''
        else:
            if given_name and family_name:
                sql = f'''SELECT id FROM Persons WHERE given_name = "{given_name}"
                    AND family_name = "{family_name}";'''
            else:
                if given_name:
                    sql = f'SELECT id FROM Persons WHERE given_name = "{given_name}";'
                if family_name:
                    sql = f'SELECT id FROM Persons WHERE family_name = "{family_name}";'
        result = self.select_query(sql)
        if result:
            return result
        return None

    def check_organization(self, name: str):
        """Checks if the organization is already exists."""

        result = self.select_query(f'SELECT id FROM Organizations WHERE name = "{name}";')
        if result:
            return result
        return None

    def add_book(self, data: dict):
        """Adds data with the given data into the database."""

        title = data.get('title', None)
        isbn = data.get('isbn', None)
        if not self.check_book(title, isbn):
            return self.insert_query('Books', data)
        return 0

    def add_person(self, data: dict):
        """Adds person with the given data into the database."""

        return self.insert_query('Persons', data)

    def add_organization(self, data: dict):
        """Adds organization with the given data into the database."""

        name = data.get('name', None)
        if not self.check_organization(name):
            return self.insert_query('Organizations', data)
        return 0

    def search_by(self, table_name: str, filter_field: str, value: str,
                  fields: list[str] = None):

        if not fields:
            fields = '*'
        else:
            fields = ', '.join(fields)
        sql = f'SELECT {fields} FROM {table_name} WHERE {filter_field} = "{value}"'
        return self.select_query(sql)

    def get_person(self, _id: int) -> dict | None:
        """Gets the person with the given _id from the database."""

        data = self.select_query(f'SELECT * FROM Persons WHERE id = {_id}')
        if not data:
            return None
        data = data[0]
        data = utils.clean_dict_from_none(data)
        if data['member_of'] == 0:
            data['member_of'] = None
        if data['member_of']:
            org_data = self.get_organization(data['member_of'])
            data['member_of'] = None
            if org_data:
                data['member_of'] = org_data
        return data

    def get_persons(self) -> list[dict] | None:
        """Gets the persons from the database."""

        data = self.select_query('SELECT * FROM Persons')
        if not data:
            return None
        for item in data:
            item = utils.clean_dict_from_none(item)
            if item['member_of'] == 0:
                item['member_of'] = None
            if item['member_of']:
                org_data = self.get_organization(item['member_of'])
                item['member_of'] = None
                if org_data:
                    item['member_of'] = org_data
        return data

    def get_organization(self, _id: int) -> dict | None:
        """Gets the organization with the given _id from the database."""

        data = self.select_query(f'SELECT * FROM Organizations WHERE id = {_id}')
        if not data:
            return None
        data = data[0]
        return data

    def get_organizations(self) -> list[dict] | None:
        """Gets all organizations from the database."""

        data = self.select_query('SELECT * FROM Organizations')
        if not data:
            return None
        return data

    def process_book(self, data: dict):
        """Adds organizations and persons to the data of the book."""

        pers_org_records = {}
        book_id = data['id']

        for pers_org_type in Constants.PERS_ORG_TYPES.value:
            pers_org_type = pers_org_type.lower() + 's'
            pers_org_records[pers_org_type] = []

        sql = f'SELECT * FROM BooksPersons WHERE book_id = {book_id}'
        books_persons = self.select_query(sql)
        for book_person in books_persons:
            person = self.get_person(book_person['person_id'])
            if person:
                if not person.get('full_name', None):
                    person['full_name'] = utils.get_full_name(person)
                entry = {
                    'id': book_person['person_id'],
                    'type': 'person',
                    'title': person['full_name']
                }
                pers_org_records[book_person['type'].lower() + 's'].append(entry)

        sql = f'SELECT * FROM BooksOrganizations WHERE book_id = {book_id}'
        books_organizations = self.select_query(sql)
        for book_organization in books_organizations:
            organization = self.get_organization(book_organization['organization_id'])
            if organization:
                entry = {
                    'id': book_organization['organization_id'],
                    'type': 'organization',
                    'title': organization['name']
                }
                pers_org_records[book_organization['type'].lower() + 's'].append(entry)

        for key, value in pers_org_records.items():
            data[key] = value

        return data

    def get_book(self, _id: int = None, uuid: str = None):
        """Gets the book with the given _id from the database."""

        if _id:
            data = self.select_query(f'SELECT * FROM Books WHERE id = {_id}')
        if uuid:
            data = self.select_query(f'SELECT * FROM Books WHERE identifier = "{uuid}"')
        if not data:
            return None
        return self.process_book(data[0])

    def get_books(self):
        """Gets the books from the database."""

        books = []
        data = self.select_query('SELECT * FROM Books')
        if not data:
            return None
        for item in data:
            books.append(self.process_book(item))
        return books

    def search_by_author(self, given_name: str = None, family_name: str = None,
                         birth_year: int = None, fields: list[str] = None):

        author_id = self.check_person(given_name, family_name, birth_year)
        if author_id:
            author_id = author_id['id']
        self.search_by('Books', 'Author', author_id, fields)

    def update_book(self, _id: int, data: dict):
        """Updates the book with the given _id from the database."""

        self.update_query('Books', _id, data)
        return True

    def update_person(self, _id: int, data: dict):
        """Updates the person with the given _id from the database."""

        if 'id' in data:
            del data['id']
        if 'member_of' in data:
            if data['member_of'] == 0:
                data['member_of'] = None
        self.update_query('Persons', _id, data)
        return True

    def update_organization(self, _id: int, data: dict):
        """Updates the organizations with the given _id from the database."""

        if 'id' in data:
            del data['id']
        self.update_query('Organizations', _id, data)
        return True

    def delete_book(self, _id):
        """Deletes the book with the given _id from the database."""

        self.query(f'DELETE FROM Books WHERE id = {_id}')

    def delete_person(self, _id):
        """Deletes the person with the given _id from the database."""

        self.query(f'DELETE FROM Persons WHERE id = {_id}')

    def delete_organization(self, _id):
        """Deletes the organization with the given _id from the database."""

        self.query(f'DELETE FROM Organizations WHERE id = {_id}')
