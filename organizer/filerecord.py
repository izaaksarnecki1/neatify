from pathlib import Path
import hashlib



class FileRecord:
    """
    Wrapper class around files to capture metadata.
    Can be further extended quite easily
    """

    def __init__(self, path: Path):
        self.path = path
        self.extension = path.suffix.lower()
        self.category = None
        self.hash = None
        self.size = path.stat().st_size


    def compute_hash(self, chunk_size: int = 8192) -> str:
        if self.hash is None:
            h = hashlib.md5()
            with self.path.open('rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b''):
                    h.update(chunk)
            self.hash = h.hexdigest()
        return self.hash

    def __repr__(self):
        return f"<FileRecord path={self.path} ext={self.extension} cat={self.category}>"
