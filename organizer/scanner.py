import os
from pathlib import Path

from organizer.filerecord import FileRecord
from organizer.ignore import Ignorer


class Scanner:
    """Recursively walks a folder and yields FileRecord objects for each file.

    When an Ignorer is provided, matching directories are pruned before
    descent (so for example `.git/` is never opened), and matching files are
    dropped from the result.
    """

    def __init__(self, root: Path, ignorer: Ignorer | None = None):
        self.root = Path(root).expanduser()
        self.ignorer = ignorer

    def scan(self) -> list[FileRecord]:
        files: list[FileRecord] = []
        for dirpath, dirnames, filenames in os.walk(self.root, followlinks=False):
            current = Path(dirpath)

            if self.ignorer is not None:
                dirnames[:] = [
                    d for d in dirnames if not self.ignorer.should_skip_dir(current / d)
                ]

            for name in filenames:
                path = current / name
                if self.ignorer is not None and self.ignorer.should_skip_file(path):
                    continue
                files.append(FileRecord(path))
        return files
