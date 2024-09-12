"""Utilities for Bookshelf."""

import logging
import os
import re
import uuid
from datetime import date, datetime
from enum import Enum


class Constants(Enum):
    """Constants for Bookshelf."""

    TABLES_LIST = ['Organizations', 'Persons', 'Books', 'OtherIDs', 'BooksPersons', 'BooksOrganizations']
    PERS_ORG_TYPES = ['Author', 'Translator', 'Illustrator', 'Character', 'Publisher']
    BOOK_FORMATS = ['-', 'AudiobookFormat', 'EBook', 'GraphicNovel', 'Hardcover', 'Paperback']
    OTHER_IDS_TYPES = ['ISSN', 'DOI', 'OLID']
    BADGES = ['-', '1', '2']
    DATABASE_NAME: str = 'book.db'
    SETTINGS_FILE: str = 'settings.json'
    FILE_TYPES = ['pdf']
    LIBRARY_DIR: str = 'library'
    DEFAULT_PICTURE: str = '../static/person_default.png'


def generate_uuid():
    return str(uuid.uuid4())

def rename_file(path: str) -> str:
    """Renames file with given path to uuid-like path.
    
    Returns
    -------
    str : new file path."""
    dirname = os.path.dirname(path)
    ext = os.path.splitext(path)[1]
    new_path = os.path.join(dirname, str(uuid.uuid4()) + ext)
    os.rename(path, new_path)
    return new_path

def check_uuid(s: str):
    """Checks if given string is a valid uuid.
    
    Returns
    -------
    bool: True if string is a valid uuid."""
    ptrn = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    reg = re.compile(ptrn)
    return reg.fullmatch(s) is not None

def read_sql(name: str):
    """Read a SQL statement from the file."""

    with open(f'sql_requests/build_{name}.sql', encoding='utf-8') as file:
        sql = file.read()
    return sql

def view_datetime(dt: datetime | date, frmt: str = None):
    if not frmt:
        frmt = '%d.%m.%Y'
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime(frmt)


def get_logger(name: str, level: int = 20):
    """
    Logger builder. Returns logger with given name and level.

    Parameters
    ----------
    name : str
        The name of the logger.
    level : int
        See levels in logging.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    handler = logging.FileHandler(f"logs/{name}.log", mode='w')
    formatter = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def get_full_name(data: dict) -> str:
    """Returns string representation of person."""

    given_name = data.get('given_name', None)
    family_name = data.get('family_name', None)
    additional_name = data.get('additional_name', None)

    if given_name and family_name and additional_name:
        return f'{family_name}, {given_name} {additional_name}'
    if family_name and given_name:
        return f'{family_name}, {given_name}'
    return family_name or given_name

def clean_dict_from_none(_dict: dict):
    for key, value in _dict.items():
        if value in ['', 'None', None]:
            _dict[key] = None
    return _dict
