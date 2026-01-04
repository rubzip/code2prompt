import os
from typing import Set, List, Optional
import pathspec


def filter_gitignore(
    files: List[str], root_path: str, spec: Optional[pathspec.PathSpec]
) -> List[str]:
    if spec is None:
        return files
    filtered_files = []
    for file_path in files:
        rel_path = os.path.relpath(file_path, root_path)
        if not spec.match_file(rel_path):
            filtered_files.append(file_path)
    return filtered_files


def _normalize_extensions(extensions: List[str]) -> Set[str]:
    return {ext if ext.startswith(".") else f".{ext}" for ext in extensions}


def filter_exclude_extensions(
    files: List[str], extensions: List[str] = None
) -> List[str]:
    if extensions is None:
        return files

    ext_set = _normalize_extensions(extensions)

    kept_files = []
    for f in files:
        _, ext = os.path.splitext(f)
        if ext.lower() not in ext_set:
            kept_files.append(f)

    return kept_files


def filter_include_extensions(
    files: List[str], extensions: List[str] = None
) -> List[str]:
    if extensions is None:
        return files

    ext_set = _normalize_extensions(extensions)

    kept_files = []
    for f in files:
        _, ext = os.path.splitext(f)
        if ext.lower() in ext_set:
            kept_files.append(f)

    return kept_files
