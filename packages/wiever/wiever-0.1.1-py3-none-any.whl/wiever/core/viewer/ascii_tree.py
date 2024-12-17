import os
import re

class AsciiTree:
    def __init__(
        self, 
        root_dir: str, 
        max_depth: int, 
        include: list[str] = None, 
        exclude: list[str] = None, 
        regex: str = None
    ):
        self.root_dir = root_dir
        self.max_depth = max_depth
        self.include = set(include) if include else None
        self.exclude = set(exclude) if exclude else None
        self.regex = re.compile(regex) if regex else None

    def display(self):
        if not os.path.exists(self.root_dir):
            print(f"Error: The directory '{self.root_dir}' does not exist.")
            return

        print(self.root_dir)
        self._print_tree(self.root_dir, prefix="", current_depth=0)

    def _print_tree(self, directory: str, prefix: str, current_depth: int):
        if self.max_depth != 0 and current_depth >= self.max_depth:
            return

        entries = sorted(os.listdir(directory))

        if self.include:
            entries = [entry for entry in entries if entry in self.include]
        if self.exclude:
            entries = [entry for entry in entries if entry not in self.exclude]
        if self.regex:
            entries = [entry for entry in entries if self.regex.search(entry)]

        entries_count = len(entries)

        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            connector = "└── " if i == entries_count - 1 else "├── "
            print(f"{prefix}{connector}{entry}")

            if os.path.isdir(path):
                new_prefix = f"{prefix}    " if i == entries_count - 1 else f"{prefix}│   "
                self._print_tree(path, new_prefix, current_depth + 1)
