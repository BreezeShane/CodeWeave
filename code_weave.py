"""
    Main process flow.
"""

import argparse
from pathlib import Path
from tqdm import tqdm

from constant_variable import TEMPLATE, TEMPLATE_FOR_CODEBLOCK
from file_parser import get_language_via_suffix
from io_utils import (
    filter_dirs,
    read_file_safe,
    check_code_block_exists
)

try:
    from project_version import __version__
except ImportError:
    __version__ = "dev"

def main():
    """ Concatenate all files in project into a single markdown file. """
    args = parse_arguments()
    file_count = 0

    excluded = wrap_exclude_dict(
        excluded_dirs=args.exclude_dirs,
        excluded_files=args.exclude_files,
        excluded_extensions=args.exclude_extensions
    )

    concatenated_text = "# Contents of all files\n"
    for file_path in tqdm(filter_dirs(
        dir_path=args.path,
        max_size=args.max_file_size,
        excluded_dict=excluded,
        exclude_hidden=not args.include_hidden
    ), desc="Processing files..."):
        if not file_path.is_file():
            continue

        content = read_file_safe(file_path)
        lang = get_language_via_suffix(file_path)
        if content is None:
            continue

        current_template = TEMPLATE_FOR_CODEBLOCK if check_code_block_exists(content) else TEMPLATE
        concatenated_text += current_template.format(file_path, lang, content)
        file_count += 1
    concatenated_text += f"\n\n---\n\n**Total files processed:** {file_count}\n"

    dest_file_path = Path(args.output)
    dest_file_path.write_text(concatenated_text, encoding="utf-8")
    print(f"Success: Processed {file_count} files to {dest_file_path}")

def parse_arguments():
    """ Parse console arguments. """
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
    parser.add_argument("-H", "--include-hidden", action="store_true",
                            help="Include hidden files and directories")
    return parser.parse_args()

def parse_excluded(reg_string: str, split_char: str = "|"):
    """ Parse the string to a list of excluded file paths. """
    if reg_string is None:
        return None
    return reg_string.split(split_char)

def wrap_exclude_dict(
        excluded_dirs: str,
        excluded_files: str,
        excluded_extensions: str
    ) -> dict:
    """ Wrap exclude dict. """
    excluded_dirs       = parse_excluded(excluded_dirs)
    excluded_files      = parse_excluded(excluded_files)
    excluded_extensions = parse_excluded(excluded_extensions)

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

    return {
        "dirs"        : excluded_dirs,
        "files"       : excluded_files,
        "extensions"  : excluded_extensions,
    }

if __name__ == "__main__":
    main()
