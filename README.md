# CodeWeave

A Python tool that concatenates all text files in a project into a single Markdown file with syntax highlighting.

## Features

- **Smart File Detection**: Automatically detects and processes text files while excluding binary files
- **Syntax Highlighting**: Automatically applies appropriate language syntax highlighting based on file extensions
- **Flexible Filtering**: Exclude directories, files, and file extensions using command-line options
- **Encoding Detection**: Handles various text encodings automatically using chardet
- **Progress Tracking**: Shows processing progress with a progress bar
- **Size Limits**: Configurable maximum file size to prevent processing large files
- **Hidden File Control**: Option to include or exclude hidden files and directories

## Installation

### Option 1: Pre-compiled Binaries (Recommended)

Download the latest pre-compiled binaries from the [Releases](https://github.com/BreezeShane/CodeWeave/releases) page:

- **Linux/macOS**: Download `cw` binary
- **Windows**: Download `cw.exe` binary

Make the binary executable (Linux/macOS only):
```bash
chmod +x cw
```

### Option 2: Python Script

#### Prerequisites

- Python 3.6 or higher

#### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install chardet tqdm
```

## Why Use Pre-compiled Binaries?

The pre-compiled binaries offer several advantages:

- **No Python Installation Required**: Works on systems without Python installed
- **No Dependencies**: All required libraries are bundled into the binary
- **Faster Execution**: Optimized binary execution without Python interpreter overhead
- **Cross-Platform**: Separate binaries for Linux, macOS, and Windows
- **Easy Distribution**: Single executable file that can be easily shared

## Usage

### Using Pre-compiled Binaries

#### Basic Usage

**Linux/macOS:**
```bash
./cw /path/to/your/project
```

**Windows:**
```cmd
cw.exe C:\path\to\your\project
```

This will scan all files in the specified directory and create a `concatenated.md` file in the current directory.

#### Advanced Usage

> 💡 **Tip**: Run `./cw --help` or `./cw -h` (binary) to see all available options.

**Linux/macOS:**
```bash
./cw /path/to/your/project \
    --output ./my_project_summary.md \
    --exclude-dirs "node_modules|.git|__pycache__" \
    --exclude-files "package-lock.json|yarn.lock" \
    --exclude-extensions ".log|.tmp|.cache" \
    --max-file-size 2048000 \
    --include-hidden
```

**Windows:**
```cmd
cw.exe C:\path\to\your\project ^
    --output .\my_project_summary.md ^
    --exclude-dirs "node_modules|.git|__pycache__" ^
    --exclude-files "package-lock.json|yarn.lock" ^
    --exclude-extensions ".log|.tmp|.cache" ^
    --max-file-size 2048000 ^
    --include-hidden
```

### Using Python Script

#### Basic Usage

```bash
python code_weave.py /path/to/your/project
```

This will scan all files in the specified directory and create a `concatenated.md` file in the current directory.

#### Advanced Usage

> 💡 **Tip**: Run `python code_weave.py --help` or `python code_weave.py -h` to see all available options.

```bash
python code_weave.py /path/to/your/project \
    --output ./my_project_summary.md \
    --exclude-dirs "node_modules|.git|__pycache__" \
    --exclude-files "package-lock.json|yarn.lock" \
    --exclude-extensions ".log|.tmp|.cache" \
    --max-file-size 2048000 \
    --include-hidden
```

### Getting Help

For detailed information about all available command-line options:

- **Binary**: `./cw --help` or `./cw -h` (Linux/macOS) / `cw.exe --help` or `cw.exe -h` (Windows)
- **Script**: `python code_weave.py --help` or `python code_weave.py -h`

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `path` | Root directory path to scan | Required |
| `-o, --output` | Output file path | `./concatenated.md` |
| `-E, --exclude-dirs` | Exclude directories (separated by \|) | None |
| `-F, --exclude-files` | Exclude files (separated by \|) | None |
| `-X, --exclude-extensions` | Exclude file extensions (separated by \|) | None |
| `--max-file-size` | Maximum file size to process (bytes) | 1048576 (1MB) |
| `--include-hidden` | Include hidden files and directories | False |
| `-v, --version` | Show version information | - |

## Supported File Types

CodeWeave automatically detects and applies syntax highlighting for the following file types:

- **Programming Languages**: Python (.py), JavaScript (.js, .jsx), TypeScript (.ts, .tsx), Java (.java), C/C++ (.c, .cpp, .h, .hpp), Go (.go), Rust (.rs), Swift (.swift), Kotlin (.kt), PHP (.php), Ruby (.rb)
- **Web Technologies**: HTML (.html), CSS (.css), SCSS (.scss), SASS (.sass)
- **Data Formats**: JSON (.json), YAML (.yaml, .yml), XML (.xml), SQL (.sql)
- **Documentation**: Markdown (.md)
- **Scripts**: Bash (.sh, .bash, .zsh)

## Output Format

The generated Markdown file follows this structure:

```markdown
# Contents of all files

## File Path: /path/to/file.py

```python
# File content here
```

## File Path: /path/to/another/file.js

```javascript
// File content here
```

**Total files processed:** 42
```

## Examples

### Exclude Common Directories

**Using Binary:**
```bash
./cw ./my_project --exclude-dirs "node_modules|.git|dist|build|__pycache__|.venv"
```

**Using Python Script:**
```bash
python code_weave.py ./my_project \
    --exclude-dirs "node_modules|.git|dist|build|__pycache__|.venv"
```

### Exclude Large Files

**Using Binary:**
```bash
./cw ./my_project --max-file-size 512000
```

**Using Python Script:**
```bash
python code_weave.py ./my_project \
    --max-file-size 512000
```

### Include Hidden Files

**Using Binary:**
```bash
./cw ./my_project --include-hidden
```

**Using Python Script:**
```bash
python code_weave.py ./my_project \
    --include-hidden
```

## Use Cases

- **Code Documentation**: Create comprehensive documentation of your entire codebase
- **Code Review**: Generate a single file containing all project files for review
- **AI Analysis**: Prepare code for AI analysis tools that require single-file input
- **Project Backup**: Create a text-based backup of your project structure
- **Learning**: Study codebases by having all files in one document

## Error Handling

CodeWeave handles various error conditions gracefully:

- **Permission Errors**: Files without read permissions are skipped with a warning
- **Encoding Issues**: Automatically detects and handles different text encodings
- **Binary Files**: Automatically skips binary files (images, executables, etc.)
- **Large Files**: Configurable size limits prevent processing oversized files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
