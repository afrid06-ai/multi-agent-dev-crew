"""
Documentation tools for the Research Agent.
Enables reading project files and directories for technical context.
"""
from pathlib import Path
from typing import Optional

from crewai.tools import tool


_PROJECT_ROOT = Path(__file__).parent.parent.parent


@tool("Read file contents")
def read_file_tool(file_path: str) -> str:
    """
    Read the contents of a file from the project.
    Use this to fetch documentation, configs, or source code.
    Input: Absolute or relative file path (e.g., 'ARCHITECTURE.md', 'src/main.py').
    """
    root = _PROJECT_ROOT.resolve()
    full_path = (root / file_path).resolve()
    try:
        full_path.relative_to(root)
    except ValueError:
        return "Error: File must be within the project directory."
    if not full_path.exists():
        return f"Error: File not found: {file_path}"
    if full_path.is_dir():
        return "Error: Path is a directory. Use read_directory_tool instead."
    try:
        return full_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file: {e}"


@tool("List directory contents")
def read_directory_tool(directory: str, pattern: Optional[str] = None) -> str:
    """
    List files and subdirectories in a directory.
    Use this to explore project structure and find relevant files.
    Input: Directory path (e.g., 'src/', '.').
    Optional: pattern filter like '*.py' for Python files.
    """
    root = _PROJECT_ROOT.resolve()
    path = (root / directory).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return "Error: Directory must be within the project."
    if not path.exists() or not path.is_dir():
        return f"Error: Directory not found: {directory}"
    try:
        if pattern:
            items = list(path.rglob(pattern))
        else:
            items = list(path.iterdir())
        items.sort(key=lambda p: (not p.is_dir(), str(p)))
        lines = []
        for p in items[:50]:  # Limit output
            rel = p.relative_to(path) if path != Path(".") else p
            lines.append(f"  {'[DIR]' if p.is_dir() else '[FILE]'} {rel}")
        return "\n".join(lines) if lines else "(empty)"
    except Exception as e:
        return f"Error listing directory: {e}"
