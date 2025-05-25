from pathlib import Path


class FileRecord:
    """
    Wrapper class around files to capture metadata.
    Can be further extended quite easily
    """

    def __init__(self, path: Path):
        self.path = path
        self.extension = path.suffix.lower()
        self.category = None

    def __repr__(self):
        return f"<FileRecord path={self.path} ext={self.extension} cat={self.category}>"
