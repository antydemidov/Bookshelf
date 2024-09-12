"""The module for the localization class."""

import json
from bookshelf.errors import Errors


class Localization:
    """
    The class for the localization.
    
    Parameters
    ----------
    lang: str
        The 2 letters ISO language code.
    """

    default = 'en'

    def __init__(self, lang: str = None):
        if not lang:
            lang = self.default
        self._data = {}
        self.load(lang)

    def load(self, lang: str):
        """Loads the strings for the given language."""

        self._data = {}
        with open('locale/strings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        if lang not in data:
            lang = self.default
        for string_id, string_value in data[lang].items():
            _value = string_value
            if not string_value:
                _value = data[self.default][string_id] or Errors.I001.name
            self._data.update({string_id: _value})

    def get(self, string_id: str) -> str:
        """Returns the string by given string ID."""

        if string_id in self._data:
            return self._data[string_id]
        return Errors.I001.name
