from pathlib import Path
from organizer.filerecord import FileRecord
import shutil
import logging


class Organizer:
    def __init__(self, dest_root: Path, dry_run: bool):
        # TODO: Add some way to ignore certain dirs. Moving . dirs may not be necessary
        self.dest_root = dest_root.expanduser()
        self.dry_run = dry_run

    def organize(self, file: FileRecord) -> bool:
        if not file.category:
            logging.warning(f"{file.path} has no recognized category.")
            return False

        dest_folder = self.dest_root / file.category

        if not dest_folder.exists() and not self.dry_run:
            # parents checks if any parents are missing, if yes then they are created
            # exist_ok ensures error only raised if given path exists and is not a dir
            dest_folder.mkdir(parents=True, exist_ok=True)
            logging.debug(f"Created folder: {dest_folder}")

        dest_path = self._get_unique_destination(dest_folder, file)

        if self.dry_run:
            logging.info(f"[DRY-RUN] Would move {file.path} -> {dest_path}")
            return True

        try:
            shutil.move(str(file.path), str(dest_path))
            logging.info(f"[MOVED] {file.path.name} -> {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to move {file.path}: {e}")
            return False

    def organize_all(self, files: list[FileRecord]):
        stats = {
            "moved": 0,
            "skipped": 0,
            "failed": 0,
            "by_category": {}
        }

        for file in files:
            result = self.organize(file)
            if result:
                stats["moved"] += 1
                cat = file.category or "uncategorized"
                stats["by_category"].setdefault(cat, 0)
                stats["by_category"][cat] += 1
            else:
                if not file.category:
                    stats["skipped"] += 1
                else:
                    stats["failed"] += 1

        logging.info("\n Summary:")
        logging.info(f"  -> Moved/simulated: {stats['moved']}")
        logging.info(f"  -> Skipped: {stats['skipped']}")
        logging.info(f"  -> Failed: {stats['failed']}")
        logging.info("  -> By category:")
        for cat, count in stats["by_category"].items():
            logging.info(f"    - {cat}: {count} file(s)")

    def _get_unique_destination(self, dest_folder: Path, file: FileRecord) -> Path:
        base = file.path.stem
        ext = file.path.suffix
        dest_path = dest_folder / f"{base}{ext}"
        counter = 1
        while dest_path.exists():
            dest_path = dest_folder / f"{base}_{counter}{ext}"
            counter += 1
        return dest_path
