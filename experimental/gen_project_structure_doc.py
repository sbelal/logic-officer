import ast
import glob
import os
import fnmatch


def is_public(name):
    """Checks if a name is public (doesn't start with an underscore)."""
    return not name.startswith('_')


def parse_python_file(file_path):
    """Parses a Python file and extracts public classes and functions."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception:
            return [], []  # Ignore files with syntax errors

    standalone_functions = []
    classes = []

    # Top-level functions and classes
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and is_public(node.name):
            standalone_functions.append(node.name)
        elif isinstance(node, ast.ClassDef) and is_public(node.name):
            class_info = {
                'name': node.name,
                'methods': []
            }
            # Methods in class
            for method_node in node.body:
                if isinstance(method_node, ast.FunctionDef) and is_public(method_node.name):
                    class_info['methods'].append(method_node.name)
            classes.append(class_info)

    return standalone_functions, classes


def get_gitignore_patterns(project_root):
    """
    Reads .gitignore and returns a list of patterns.
    This is a simplified parser and does not support all .gitignore features.
    """
    gitignore_path = os.path.join(project_root, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns


def is_path_ignored(relative_path, gitignore_patterns):
    """
    Checks if a path matches any of the .gitignore patterns.
    Handles root-only and any-level directory ignores.
    """
    path_components = relative_path.split('/')

    for pattern in gitignore_patterns:
        is_root_pattern = pattern.startswith('/')
        if is_root_pattern:
            pattern = pattern.lstrip('/')

        # Handle directory patterns (e.g., 'foo/' or '/foo/')
        if pattern.endswith('/'):
            dir_name = pattern.rstrip('/')
            if is_root_pattern:
                # Anchored to root: matches '/foo/'
                if path_components and path_components[0] == dir_name:
                    return True
            else:
                # Any level: matches 'foo/'
                if dir_name in path_components:
                    return True

        # Handle file/glob patterns
        else:
            if fnmatch.fnmatch(relative_path, pattern):
                return True
            # If not a root pattern and no slashes in pattern, match basename anywhere
            if not is_root_pattern and '/' not in pattern:
                if fnmatch.fnmatch(os.path.basename(relative_path), pattern):
                    return True
    return False


def main():
    """
    Scans for python files, parses them, and generates a markdown documentation file.
    """
    project_root = os.getcwd()
    all_py_files = glob.glob(os.path.join(project_root, '**', '*.py'), recursive=True)

    gitignore_patterns = get_gitignore_patterns(project_root)
    gitignore_patterns.extend([
        '.venv/',
        'tests/',
        '.gemini/'
    ])

    docs_by_folder = {}

    for file_path in sorted(all_py_files):
        relative_path = os.path.relpath(file_path, project_root).replace('\\', '/')

        if is_path_ignored(relative_path, gitignore_patterns):
            continue

        standalone_functions, classes = parse_python_file(file_path)

        if not standalone_functions and not classes:
            continue

        folder = os.path.dirname(relative_path)
        if folder not in docs_by_folder:
            docs_by_folder[folder] = {}

        docs_by_folder[folder][relative_path] = {
            'functions': standalone_functions,
            'classes': classes
        }

    markdown_content = "# Project Structure\n\n"

    for folder in sorted(docs_by_folder.keys()):
        markdown_content += f"## Folder: `{folder}`\n\n"
        markdown_content += "**Purpose:** [FOLDER PURPOSE]\n\n"

        for file_path, doc_info in docs_by_folder[folder].items():
            markdown_content += f"- **File:** `{file_path}`\n\n"

            if doc_info['functions']:
                markdown_content += "  - **Standalone Functions**\n"
                for func_name in doc_info['functions']:
                    markdown_content += f"    - **`{func_name}()`**\n"
                    markdown_content += f"      - **Summary:** [FUNCTION SUMMARY]\n"

            if doc_info['classes']:
                markdown_content += "  - **Classes**\n"
                for class_info in doc_info['classes']:
                    markdown_content += f"    - **Class:** `{class_info['name']}`\n"
                    markdown_content += f"      - **Purpose:** [CLASS PURPOSE]\n"
                    if class_info['methods']:
                        markdown_content += f"      - **Methods**\n"
                        for method_name in class_info['methods']:
                            markdown_content += f"        - **`{method_name}()`**\n"
                            markdown_content += f"          - **Summary:** [FUNCTION SUMMARY]\n"
            markdown_content += "\n"

        markdown_content += "---\n\n"

    output_file = os.path.join(project_root, '.gemini', 'project_structure.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Project Structure Documentation generated at: {output_file}")


if __name__ == "__main__":
    main()
