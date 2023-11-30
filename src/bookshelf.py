"""Bookshelf Internal Module."""


import json
import os

import pypdf as pdf

from app.utils import get_size_format


class Book:
    """Represents the Book object."""

    def __init__(self, path: str, _id: int = 1):
        self._id: int = _id
        self.link: str = f'/book/{self._id}'
        self.path = path
        self.abs_path = os.path.abspath(path)
        self.status = self.check()
        file_name, extension = os.path.splitext(self.path)
        self.file_name: str = file_name
        self.extension: str = extension
        self.size: int = os.stat(self.path).st_size
        self.formatted_size: str = get_size_format(self.size)

        properties = self.__get_properties()
        self.title: str = properties.get('title', None)
        self.author: str = properties.get('author', None)
        self.creator = properties.get('creator', None)
        self.producer = properties.get('producer', None)
        self.creation_date = properties.get('creation_date', None)
        self.modification_date = properties.get('modification_date', None)

    def check(self):
        """Description."""

        return os.path.exists(self.path)

    def __get_properties(self):
        """Extracts the data from the file."""

        properties = {}
        if self.extension == '.pdf':
            properties = self.__pdf_handler()

        return properties

    def __pdf_handler(self):
        file = pdf.PdfReader(self.path)
        creation_date = file.metadata.creation_date
        modification_date = file.metadata.modification_date
        if creation_date:
            creation_date = creation_date.date()
        if modification_date:
            modification_date = modification_date.date()
        properties = {
            'title': file.metadata.title,
            'creator': file.metadata.creator,
            'producer': file.metadata.producer,
            'creation_date': creation_date,
            'modification_date': modification_date,
            'author': file.metadata.author
        }
        return properties

    def set_properties(self, properties: dict):
        """Updates the properties of the pdf file with the given properties."""

    def get_properties(self):
        """Returns the properties of the book."""

        return self.__dict__


class BookShelf:
    """Represents your library."""

    def __init__(self) -> None:
        self.settings: dict = self.get_settings()
        self.status: bool = self.check()
        self.books = self.scan_library()

    def get_settings(self):
        """Loads settings from the settings file."""

        with open('settings.json', 'r', encoding='utf8') as f:
            settings = json.load(f)
        return settings

    def check(self):
        """Checks the folder, etc."""

        return os.path.exists(self.settings['library_path'])

    def get_size(self):
        """Description."""

        size = 0
        for i in os.scandir('./library/'):
            size += i.stat().st_size
        return size

    def get_book(self, path) -> Book:
        """Returns a Book object for the given path."""

        return Book(path)

    def scan_library(self, file_types: str | list[str] = None) -> tuple[int, list[str]]:
        """Scanning the folder specified as a library.
        
        Parameters
        ----------
        file_types : str or list[str]
            File types to scan in the library folder. You must enter the
            extensions in the format like '.pdf', '.djvu', etc.
        """

        lst = []
        scan = os.scandir(self.settings['library_path'])

        if isinstance(file_types, str):
            file_types = [file_types]

        if file_types is None:
            for i in scan:
                if i.is_file():
                    lst.append(i.path)
        else:
            for i in scan:
                if (i.is_file() and os.path.splitext(i.path)[1].lower() in file_types):
                    lst.append(i.path)

        books = [Book(i, lst.index(i)) for i in lst]

        return books

    def __iter__(self):
        for book in self.books:
            yield book

    def __getitem__(self, index) -> Book:
        return self.books[index]

    def export_to_csv(self): ...
