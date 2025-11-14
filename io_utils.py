"""
    Definitions of IO functions.
"""

from typing import Optional
from pathlib import Path
import chardet

def filter_dirs(
        dir_path,
        excluded_dict: dict,
        max_size=1024*1024,
        exclude_hidden=True
    ):
    """ Filter the dirs to exclude specified paths. """
    excluded_dirs       = excluded_dict.get("dirs"),
    excluded_files      = excluded_dict.get("files"),
    excluded_extensions = excluded_dict.get("extensions")
    dir_path = Path(dir_path)

    for path in dir_path.rglob("*"):
        if not should_process_file(path, max_size):
            continue
        if exclude_hidden and any(part.startswith('.') for part in path.parts):
            continue
        if any(exclude_dir in path.parts for exclude_dir in excluded_dirs):
            continue
        if path.parts[-1] in excluded_files:
            continue
        if path.suffix.lower() in excluded_extensions:
            continue
        if not is_text_file(path):
            continue
        yield path

def should_process_file(file_path: Path, max_size=1024*1024):
    """ Check if the file should be processed. """
    try:
        return file_path.stat().st_size <= max_size
    except OSError:
        return False

def is_text_file(file_path):
    """ Check if text file. """
    try:
        binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', '.dll'}
        if file_path.suffix.lower() in binary_extensions:
            return False
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False
        return True
    except OSError:
        return False

def read_file_safe(file_path) -> Optional[str]:
    """ Read file safely, handle problems of encoding and permissions. """
    print(file_path)
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            encoding_format = detect_encoding(file_path)
            return file_path.read_text(encoding=encoding_format)
        except IOError as e:
            raise IOError(f"# Unable to read file: {file_path} (Might be binary file.)") from e
    except PermissionError as e:
        raise PermissionError(f"# No permission to read file: {file_path}") from e
    except OSError as e:
        raise OSError(f"# Error while reading file: {file_path}") from e

def detect_encoding(file_path):
    """ Detect encoding. """
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        return result.get('encoding', 'utf-8')
