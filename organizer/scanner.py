from pathlib import Path
from organizer.filerecord import FileRecord


class Scanner:
    """
    Class used to recursively scan through some folder to collect all files
    """

    def __init__(self, root: Path):
        self.root = root

    def scan(self):
        files = []

        for path in self.root.rglob("*"):
            if path.is_file():
                files.append(FileRecord(path))

        return files
