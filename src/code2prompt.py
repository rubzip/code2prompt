import os
import argparse
from typing import List, Optional

# Adjust import based on your project structure
from .io_utils import load_all_files, load_gitignore, load_with_path
from .filtering import (
    filter_gitignore,
    filter_exclude_extensions,
    filter_include_extensions,
)


def code2prompt(
    path: str,
    exclude_extensions: Optional[List[str]] = None,
    include_extensions: Optional[List[str]] = None,
    comment_symbol: str = "#",
    output_file: Optional[str] = None
):
    root_abs_path = os.path.abspath(path)

    spec = load_gitignore(root_abs_path)
    files = load_all_files(root_abs_path)

    files = filter_gitignore(files, root_abs_path, spec)
    files = filter_exclude_extensions(files, exclude_extensions)
    files = filter_include_extensions(files, include_extensions)

    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for file in files:
                    content = load_with_path(file, comment_symbol)
                    if content:
                        f.write(content + "\n")
        except Exception as e:
            return

    else:
        for file in files:
            content = load_with_path(file, comment_symbol)
            if content:
                print(content)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate code files into a single context string."
    )
    parser.add_argument("path", nargs="?", default=".", help="Target directory path")
    parser.add_argument(
        "--exclude", nargs="+", help="Extensions to exclude (e.g. .pyc .lock)"
    )
    parser.add_argument(
        "--include", nargs="+", help="Extensions to include (e.g. .py .js)"
    )
    
    parser.add_argument(
        "-o", "--output", help="Path to output file (e.g. prompt.txt)"
    )

    args = parser.parse_args()

    code2prompt(
        args.path, 
        exclude_extensions=args.exclude, 
        include_extensions=args.include,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
