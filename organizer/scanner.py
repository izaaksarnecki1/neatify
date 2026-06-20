from pathlib import Path

from organizer.filerecord import FileRecord


class Scanner:
    """Recursively walks a folder and yields FileRecord objects for each file."""

    def __init__(self, root: Path):
        self.root = Path(root).expanduser()

    def scan(self) -> list[FileRecord]:
        return [FileRecord(path) for path in self.root.rglob("*") if path.is_file()]
