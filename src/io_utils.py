import os
from typing import List, Optional

import pathspec

from .constants import ALWAYS_IGNORE_DIRS, ALWAYS_IGNORE_FILES


def load_all_files(path: str) -> List[str]:
    all_files = []
    abs_path = os.path.abspath(path)
    for root, dirs, files in os.walk(abs_path):
        dirs[:] = [d for d in dirs if d not in ALWAYS_IGNORE_DIRS]
        for file in files:
            if file in ALWAYS_IGNORE_FILES:
                continue

            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files


def load_gitignore(root_path: str) -> Optional[pathspec.PathSpec]:
    gitignore_path = os.path.join(root_path, ".gitignore")
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r") as f:
                return pathspec.PathSpec.from_lines("gitwildmatch", f)
        except Exception as e:
            print(f"Error loading .gitignore: {e}")
            return None
    return None


def _is_binary(file_path: str) -> bool:
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except Exception:
        return True


def _open_file(file_path: str) -> Optional[str]:
    if _is_binary(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def load_with_path(path: str, comment_symbol: str = "#") -> Optional[str]:
    content = _open_file(path)
    if content is None:
        return None

    return f"{comment_symbol} {path}\n{content}"
