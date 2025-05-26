from pathlib import Path
from config import load_config

from cli.interface import app

from organizer.classifier import Classifier
from organizer.scanner import Scanner
from organizer.actions import Organizer


def delete_duplicates(duplicates, dry_run: bool, mode: str):
    for group in duplicates:
        if mode == "oldest":
            group.sort(key=lambda f: f.path.stat().st_mtime)  # sort by last modified
            keep = group[0]
            to_delete = group[1:]
            print(f"Keeping (oldest): {keep.path}\n")
        elif mode == "manual":
            print("Duplicate group:\n")
            for idx, fr in enumerate(group):
                print(f"{idx}: {fr.path}")
            choice = input("Enter the number of the file to keep: ")
            try:
                keep = group[int(choice)]
                to_delete = [f for f in group if f != keep]
            except (IndexError, ValueError):
                print("Invalid choice. Skipping group.\n")
                continue
        else:
            continue  # skip deletion in "none" mode

        for file in to_delete:
            if dry_run:
                print(f"[DRY RUN] Would send to trash: {file.path}\n")
            else:
                try:
                    send2trash(str(file.path))
                    print(f"Sent to trash: {file.path}\n")
                except Exception as e:
                    print(f"Failed to delete {file.path}: {e}\n")




def run(source: Path, dest: Path, dry_run: bool, delete_mode: str, check_duplicates: bool) -> None:
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

    if check_duplicates:
        print(f"Scanning files in: {source}\n")

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
