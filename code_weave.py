"""
    Concat text files into a single file.
"""
import argparse
from pathlib import Path
from typing import Optional

import chardet
from tqdm import tqdm

try:
    from _version import __version__
except ImportError:
    __version__ = "dev"

TEMPLATE = """
## File Path: {}

```{}
{}
```
"""

def parse_excluded(reg_string: str, split_char: str = "|"):
    """ Parse the string to a list of excluded file paths. """
    if reg_string is None:
        return None
    return reg_string.split(split_char)

def detect_encoding(file_path):
    """ Detect encoding. """
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        return result.get('encoding', 'utf-8')

def filter_dirs(
        dir_path,
        max_size=1024*1024,
        excluded_dirs=None,
        excluded_files=None,
        excluded_extensions=None,
        exclude_hidden=True
    ):
    """ Filter the dirs to exclude specified paths. """
    if excluded_dirs is None:
        excluded_dirs = set()
    if excluded_files is None:
        excluded_files = set()
    if excluded_extensions is None:
        excluded_extensions = set()

    if isinstance(excluded_dirs, list):
        excluded_dirs = set(excluded_dirs)
    if isinstance(excluded_files, list):
        excluded_files = set(excluded_files)
    if isinstance(excluded_extensions, list):
        excluded_extensions = set(excluded_extensions)

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

def get_language(path: Path):
    """ Get the language used in the file. """
    extension_map = {
        '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
        '.ts': 'typescript', '.tsx': 'typescript', '.java': 'java',
        '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.hpp': 'cpp',
        '.html': 'html', '.css': 'css', '.scss': 'scss', '.sass': 'sass',
        '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml',
        '.md': 'markdown', '.xml': 'xml', '.sql': 'sql',
        '.sh': 'bash', '.bash': 'bash', '.zsh': 'bash',
        '.php': 'php', '.rb': 'ruby', '.go': 'go',
        '.rs': 'rust', '.swift': 'swift', '.kt': 'kotlin'
    }
    return extension_map.get(path.suffix.lower(), 'text')

def should_process_file(file_path: Path, max_size=1024*1024):
    """ Check if the file should be processed. """
    try:
        return file_path.stat().st_size <= max_size
    except Exception as _:
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
    except Exception as _e:
        return False

def read_file_safe(file_path) -> Optional[str]:
    """ Read file safely, handle problems of encoding and permissions. """
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            encoding_format = detect_encoding(file_path)
            return file_path.read_text(encoding=encoding_format)
        except Exception as e:
            print(f"# Unable to read file: {file_path} (Might be binary file.) - {e}\n")
    except PermissionError:
        print(f"# No permission to read file: {file_path}\n")
    except Exception as e:
        print(f"# Error while reading file: {file_path} - {e}\n")

    return None

def main():
    """ Concatenate all files in project into a single markdown file. """
    parser = argparse.ArgumentParser(
        description='Concat files into a single file.',
        epilog=f'CodeWeave v{__version__} - https://github.com/BreezeShane/CodeWeave'
    )
    parser.add_argument("-v", "--version", action="version", version=f"CodeWeave v{__version__}",
                        help="Show version information and exit")
    parser.add_argument("path", type=str, help="The root dir path to scan.")
    parser.add_argument("-E", "--exclude-dirs", type=str,
                            help="Exclude directories (separated by |)")
    parser.add_argument("-F", "--exclude-files", type=str,
                            help="Exclude files (separated by |)")
    parser.add_argument("-X", "--exclude-extensions", type=str,
                            help="Exclude file extensions (separated by |)")
    parser.add_argument("-o", "--output", type=str, default="./concatenated.md",
                            help="Output file path")
    parser.add_argument("--max-file-size", type=int, default=1024*1024,
                            help="Max file size to process (bytes)")
    parser.add_argument("--include-hidden", action="store_true",
                            help="Include hidden files and directories")
    args = parser.parse_args()

    file_count = 0

    concatenated_text = "# Contents of all files\n"
    for file_path in tqdm(filter_dirs(
        Path(args.path),
        args.max_file_size,
        parse_excluded(args.exclude_dirs),
        parse_excluded(args.exclude_files),
        parse_excluded(args.exclude_extensions),
        not args.include_hidden
    ), desc="Processing files..."):
        if not file_path.is_file():
            continue
        lang = get_language(file_path)

        content = read_file_safe(file_path)
        if content is None:
            continue

        concatenated_text += TEMPLATE.format(file_path, lang, content)
        file_count += 1
    concatenated_text += f"\n\n---\n**Total files processed:** {file_count}\n"

    dest_file_path = Path(args.output)
    dest_file_path.write_text(concatenated_text, encoding="utf-8")
    print(f"Success: Processed {file_count} files to {dest_file_path}")

if __name__ == "__main__":
    main()
