import fnmatch
from organizer.filerecord import FileRecord


class Classifier:
    """
    Class utilized to categorize files based on extensions
    """

    def __init__(self, categories: dict):
        self.categories = categories

    def classify(self, file: FileRecord) -> str:
        """
        Returns category as str determined on file's extension
        """
        filename = file.path.name.lower()

        for cat, patterns in self.categories.items():
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    return cat

        return "uncategorized"
