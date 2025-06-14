from pathlib import Path

from config import load_config

from utils.logger import setup_logger

from cli.interface import app

from organizer.actions import Organizer
from organizer.classifier import Classifier
from organizer.scanner import Scanner
from organizer.duplicates import process_duplicates


def run(
        source: Path,
        dest: Path,
        dry_run: bool,
        delete_mode: str,
        check_duplicates: bool,
        verbose: bool) -> None:

    config = load_config()

    if source:
        config["source"] = source
    if dest:
        config["dest"] = dest

    config["verbose"] = verbose
    config["dry_run"] = dry_run
    config["check_duplicates"] = check_duplicates

    setup_logger(verbose=config["verbose"])

    scanner = Scanner(config)
    classifier = Classifier(config["categories"])
    organizer = Organizer(dest, dry_run)
    files = scanner.scan()

    print(f"Found {len(files)} files.")
    for file in files:
        file.category = classifier.classify(file)

    organizer.organize_all(files)

    scanner = Scanner(source)
    files = scanner.scan()

    if check_duplicates:
        process_duplicates(files, dry_run, delete_mode)


def main():
    app()


if __name__ == "__main__":
    main()
