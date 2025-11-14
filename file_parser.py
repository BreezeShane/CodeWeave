"""
    Concat text files into a single file.
"""
from pathlib import Path

from constant_variable import EXTENSION_MAP

def get_language_via_suffix(path: Path):
    """ Get the language used in the file. """
    return EXTENSION_MAP.get(path.suffix.lower(), 'text')
