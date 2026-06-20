from pathlib import Path

from config import load_config
from organizer.actions import Organizer
from organizer.classifier import Classifier
from organizer.duplicates import process_duplicates
from organizer.scanner import Scanner
from utils.logger import setup_logger


def run(
    source: Path,
    dest: Path,
    dry_run: bool,
    verbose: bool,
    check_duplicates: bool,
    delete_mode: str | None,
) -> None:
    config = load_config()
    if source:
        config["source"] = source
    if dest:
        config["dest"] = dest

    config["verbose"] = verbose
    config["dry_run"] = dry_run
    config["check_duplicates"] = check_duplicates

    setup_logger(verbose=config["verbose"])

    root = Path(config["source"]).expanduser()
    dest_root = Path(config["dest"]).expanduser()

    scanner = Scanner(root)
    classifier = Classifier(config["categories"])
    organizer = Organizer(dest_root, dry_run)

    files = scanner.scan()
    print(f"Found {len(files)} files.")

    for file in files:
        file.category = classifier.classify(file)

    organizer.organize_all(files)

    if check_duplicates:
        post_move_files = Scanner(dest_root).scan()
        process_duplicates(post_move_files, dry_run, delete_mode)
