#!/usr/bin/env python3
"""
create_context.py - Generate a single text file with project structure and file contents
for easy loading into NotebookLM or other LLM tools.

Usage:
    python create_context.py [--output OUTPUT] [--root ROOT] [--exclude EXCLUDE PATTERNS]

Example:
    python create_context.py --output context.txt --root . --exclude "*.log" "*.tmp" "__pycache__" ".git"
"""

import argparse
import os
from pathlib import Path
import fnmatch


def is_binary_file(filepath):
    """Check if file is binary by trying to read as text."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read()
        return False
    except UnicodeDecodeError:
        return True


def get_project_structure(root_dir):
    """Generate a tree-like representation of the project structure."""
    structure = []
    root_path = Path(root_dir).resolve()

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories
        dirnames[:] = [
            d for d in dirnames if not should_exclude(Path(dirpath) / d, exclude_dirs)
        ]

        level = dirpath.replace(str(root_path), "").count(os.sep)
        indent = " " * 4 * level
        structure.append(f"{indent}{os.path.basename(dirpath)}/")

        subindent = " " * 4 * (level + 1)
        for f in filenames:
            if not should_exclude(Path(dirpath) / f, exclude_files):
                structure.append(f"{subindent}{f}")

    return "\n".join(structure)


def should_exclude(path, patterns):
    """Check if path matches any of the exclude patterns."""
    path_str = str(path)
    for pattern in patterns:
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate context file for LLM")
    parser.add_argument(
        "--output",
        "-o",
        default="context.txt",
        help="Output file name (default: context.txt)",
    )
    parser.add_argument(
        "--root",
        "-r",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--exclude",
        "-e",
        action="append",
        default=[],
        help="Patterns to exclude (can be used multiple times)",
    )
    args = parser.parse_args()

    # Default exclusions - add your own via --exclude
    global exclude_dirs, exclude_files
    exclude_dirs = [
        "__pycache__",
        ".git",
        ".venv",
        "node_modules",
        ".idea",
        ".vscode",
        "sandbox",
        ".git",
        "data_pipeline.egg-info",
    ]
    exclude_files = [
        "*.tmp",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".gitignore",
        "config.yaml",
        "*.sample",
        ".gitkeep",
        "create_context.py",
        "context.txt",
    ]

    # Add user-specified exclusions
    exclude_dirs.extend(args.exclude)
    exclude_files.extend(args.exclude)

    root_path = Path(args.root).resolve()
    output_path = root_path / args.output

    print(f"Scanning: {root_path}")
    print(f"Output: {output_path}")
    print(f"Excluding directories: {exclude_dirs}")
    print(f"Excluding files: {exclude_files}")

    with open(output_path, "w", encoding="utf-8") as out_file:
        # Write project structure
        out_file.write("=== PROJECT STRUCTURE ===\n")
        out_file.write(get_project_structure(root_path))
        out_file.write("\n\n=== FILE CONTENTS ===\n\n")

        # Walk and write file contents
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Modify dirnames in-place to skip excluded directories
            dirnames[:] = [
                d
                for d in dirnames
                if not should_exclude(Path(dirpath) / d, exclude_dirs)
            ]

            for filename in filenames:
                filepath = Path(dirpath) / filename
                if should_exclude(filepath, exclude_files):
                    continue

                rel_path = filepath.relative_to(root_path)
                out_file.write(f"--- {rel_path} ---\n")

                try:
                    if is_binary_file(filepath):
                        out_file.write("[BINARY FILE - SKIPPED]\n\n")
                    else:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        out_file.write(content)
                        if not content.endswith("\n"):
                            out_file.write("\n")
                        out_file.write("\n")
                except Exception as e:
                    out_file.write(f"[ERROR READING FILE: {e}]\n\n")

    print(f"\nDone! Output written to: {output_path}")


if __name__ == "__main__":
    main()
