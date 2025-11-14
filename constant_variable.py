"""
    Constant Variables.
"""

TEMPLATE = """
## File Path: {}

```{}
{}
```
"""

TEMPLATE_FOR_CODEBLOCK = """
## File Path: {}

````{}
{}
````
"""

EXTENSION_MAP = {
        '.py': 'python', '.js': 'javascript', '.jsx': 'javascript',
        '.ts': 'typescript', '.tsx': 'typescript', '.java': 'java',
        '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.hpp': 'cpp',
        '.html': 'html', '.css': 'css', '.scss': 'scss', '.sass': 'sass',
        '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml', '.ini': 'ini',
        '.md': 'markdown', '.xml': 'xml', '.sql': 'sql',
        '.sh': 'bash', '.bash': 'bash', '.zsh': 'bash',
        '.php': 'php', '.rb': 'ruby', '.go': 'go',
        '.rs': 'rust', '.swift': 'swift', '.kt': 'kotlin',
    }
