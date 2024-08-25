"""Bookshelf Handlers"""

import abc
import os
# from datetime import datetime

import pypdf

# import docx


__all__ = [
    'PDFFile',
    # 'DJVUFile',
    # 'DOCXFile'
]


class _BasicFile(metaclass=abc.ABCMeta):
    def __init__(self, path: str) -> None:
        self._check_path(path)
        self.path = path
        self.size: int = os.stat(path).st_size
        self.pages: list
        self.properties: dict

    @abc.abstractmethod
    def get_metadata(self): ...

    @abc.abstractmethod
    def set_metadata(self, data: dict = None): ...

    # @abc.abstractmethod
    # def remove_metadata(self): ...

    # @abc.abstractmethod
    # def iter_pages(self): ...

    # @abc.abstractmethod
    # def get_annotation(self): ...

    # @abc.abstractmethod
    # def set_annotation(self): ...

    # @abc.abstractmethod
    # def remove_annotation(self): ...

    def _check_path(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(path, 'does not exist')
        if os.path.isdir(path):
            raise FileNotFoundError(path, 'is not a file')

    def __repr__(self):
        return f'{self.__class__.__name__}(path={self.path})'

    def __iter__(self):
        if isinstance(self.pages, list):
            for page in self.pages:
                yield page

    def __len__(self):
        if self.pages:
            return len(self.pages)
        return 0

    def __getitem__(self, index):
        if isinstance(self.pages, list):
            return self.pages[index]
        return None


class PDFFile(_BasicFile):
    """Reads and writes the `.pdf`-file."""

    def __init__(self, path: str):
        super().__init__(path)
        self.file = pypdf.PdfReader(path)

    def get_metadata(self) -> dict:
        """Get the metadata from the file."""
        metadata = self.file.metadata
        data = {
            'authors': [metadata.get('/Author', None)],
            'title': metadata.get('/Title', None),
            'subjects': [metadata.get('/Subject', None)],
            'keywords': str(metadata.get('/Keywords', None)).split(', '),
        }
        return data

    def set_metadata(self, data: dict = None):
        """Set the metadata from the file."""

        writer = pypdf.PdfWriter(clone_from=self.file)
        metadata = {
            '/Author': ', '.join(data.get('author')),
            # '/Producer': data.get('producer'),
            '/Title': data.get('title'),
            '/Subject': ', '.join(data.get('subjects')),
            '/Keywords': ', '.join(data.get('keywords')),
            # '/CreationDate': data.get('creation_date'),
            # '/ModDate': data.get('modification_date'),
            # '/Creator': data.get('creator'),
            # '/CustomField': data.get('custom_field'),
        }
        props = {k:v for k,v in metadata.items() if v is not None}
        writer.add_metadata(props)


# class DJVUFile(_BasicFile):
#     """Reads and writes the `.djvu`-file."""

#     def __init__(self, path: str):
#         super().__init__(path)


# class DOCXFile(_BasicFile):
#     """Reads and writes the `.docx`-file."""

#     def __init__(self, path: str) -> None:
#         super().__init__(path)
#         # file = docx.Document(path)
#         self.author: str
#         self.category: str
#         self.comments: str
#         self.content_status: str
#         self.created: datetime
#         self.identifier: str
#         self.keywords: str
#         self.language: str
#         self.last_modified_by: str
#         self.last_printed: datetime
#         self.modified: datetime
#         self.revision: int
#         self.subject: str
#         self.title: str
#         self.version: str


# class OpenLibrary:
#     def __init__(self):
#         pass
    
#     def search(self, q: str, fields: list, sort: str,
#                lang: str, page: int, limit: int):
#         base_url = 'https://openlibrary.org/search.json'
#         req
