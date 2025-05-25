from pathlib import Path
from organizer.filerecord import FileRecord


class Scanner:
    """
    Class used to recursively scan through some folder to collect all files
    """

    def __init__(self, config: dict):
        self.root = Path(config["source"]).expanduser()

    def scan(self):
        """
        Returns a list of FileRecord objects
        """
        files = []
        for path in self.root.rglob("*"):
            if path.is_file():
                files.append(FileRecord(path))
        return files
