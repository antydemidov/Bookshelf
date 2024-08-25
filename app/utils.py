"""A set of utilities for the web app of Bookshelf."""


def get_size_format(size, factor=1024, suffix='B'):
    """
    Scale bytes to its proper byte format.

    Example
    -------
    ```python
    >>> get_size_format(1253656)
    '1.196 MB'
    >>> get_size_format(1253656678)
    '1.168 GB'
    >>> get_size_format(2000, factor=1000, suffix='m')
    '2.000 Km'
    ```
    """

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if size < factor:
            return f'{size:.3f} {unit}{suffix}'
        size /= factor
    return f'{size:.3f} Y{suffix}'
