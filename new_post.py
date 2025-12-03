#!/usr/bin/env python3

import datetime
import glob
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CONTENT_PATH = Path(__file__).parent / "content"


def find_next_number():
    """Find the next available number for the markdown file."""
    pattern = str(CONTENT_PATH / "[0-9][0-9][0-9][0-9][0-9][0-9].md")
    existing_files = glob.glob(pattern)
    assert existing_files

    numbers = []
    for filepath in existing_files:
        filename = os.path.basename(filepath)
        match = re.match(r"^(\d{6})\.md$", filename)
        if match:
            numbers.append(int(match.group(1)))

    assert numbers
    return max(numbers) + 1


def launch_editor(filepath: str):
    """Launch the editor with the given file."""
    try:
        subprocess.run(["nvim", filepath], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching editor: {e}")
        sys.exit(1)


def get_body() -> str:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    launch_editor(tmp.name)
    with open(tmp.name) as f:
        return f.read()


def save_final_file(body: str, next_num: int) -> Path:
    """Save the edited content to the final numbered file and commit to git."""
    header = f"""---
slug: {next_num}
title: #{next_num}
date: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")}
---

"""
    content = header + body
    if not body:
        print("Aborting because no content was written")
        sys.exit(1)

    final_filepath = CONTENT_PATH / f"{next_num:06d}.md"
    with open(final_filepath, "w") as f:
        f.write(content)

    print(f"Created: {final_filepath}")
    return final_filepath


def git_commit_file(filepath: Path, next_num: int):
    """Add the file to git and create a commit."""
    try:
        # Get the repository root (where this script is located)
        repo_root = Path(__file__).parent

        # Get relative path from repo root
        relative_path = filepath.relative_to(repo_root)

        # Add the file to git
        subprocess.run(
            ["git", "add", str(relative_path)],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )

        # Create commit
        commit_message = f"feat({next_num:06d}): write new post #{next_num}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"Committed to git: {commit_message}")

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        print(f"Error output: {e.stderr}")
        print("The file was created but not committed to git.")
    except Exception as e:
        print(f"Unexpected error during git operation: {e}")
        print("The file was created but not committed to git.")


def main():
    """Main function."""
    next_num = find_next_number()
    print(f"Creating post #{next_num}")

    try:
        body = get_body()
        final_filepath = save_final_file(body, next_num)
        git_commit_file(final_filepath, next_num)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()
