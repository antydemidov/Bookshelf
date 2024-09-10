"""The set of errors in this project."""

from dataclasses import dataclass


@dataclass
class Error:
    code: str
    name: str
    description: str


class Errors(object):
    I001 = Error('I001',
                 'I001: Translation error',
                 'The translation is missing. Check the file `strings.json`')
    """Translation error."""
