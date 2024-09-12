"""The set of errors in this project."""


__all__ = [
    'TranslationError',
    'SettingsError',
    'WrongFileType',

    'ConversionError'
]


class TranslationError(Exception):
    """
    `I001`: Translation error

    The translation is missing. Check the file `strings.json`.
    """


class SettingsError(Exception):
    """
    `I002`: Settings error
    
    The settings file is missing or has some mistakes. Check the file `settings.json`.
    """


class WrongFileType(Exception):
    """
    `I003`: Wrong file type
    
    This error is raised when a file type is not recognized. Currently the
    application works only with pdf-files.
    """


# ============ Future errors ============
class ConversionError(Exception):
    """
    `I004`: Conversion error
    
    This error is raised when a conversion process fails, e.g., during the
    conversion from docx to pdf.
    """
