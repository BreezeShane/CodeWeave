"""
    Concat text files into a single file.
"""
from pathlib import Path

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
