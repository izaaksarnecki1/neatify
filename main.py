from pathlib import Path
from config import load_config

from cli.interface import app

from organizer.classifier import Classifier
from organizer.scanner import Scanner
from organizer.actions import Organizer


def run(source: Path, dest: Path, dry_run: bool) -> None:
    # function where main logic will be placed. Called from interface.py
    # print(f"Source: {source}")
    # print(f"Destination: {dest}")
    # print(f"Dry run: {dry_run}")

    config = load_config()
    if source:
        config["source"] = source
    if dest:
        config["dest"] = dest

    config["dry_run"] = dry_run

    print(f"Scanning files in: {source}")

    scanner = Scanner(config)
    classifier = Classifier(config["categories"])
    organizer = Organizer(dest, dry_run)
    files = scanner.scan()

    print(f"Found {len(files)} files.")
    for file in files:
        file.category = classifier.classify(file)

    organizer.organize_all(files)


def main():
    app()


if __name__ == "__main__":
    main()
