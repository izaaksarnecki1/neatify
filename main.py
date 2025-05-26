from cli.interface import app
from pathlib import Path
from organizer.scanner import Scanner
from config import load_config
from collections import defaultdict
from send2trash import send2trash


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

        scanner = Scanner(source)
        files = scanner.scan()

        size_map = defaultdict(list)
        for file in files:
            size_map[file.size].append(file)

        duplicates = []
        for size, group in size_map.items():
            if len(group) > 1:
                hash_map = defaultdict(list)
                for file in group:
                    file_hash = file.compute_hash()
                    hash_map[file_hash].append(file)

                for dup_group in hash_map.values():
                    if len(dup_group) > 1:
                        duplicates.append(dup_group)

        if duplicates:
            print("Found duplicate files:")
            for group in duplicates:
                print("\n - Duplicate set:")
                for file in group:
                    print(f"{file.path}")
            if delete_mode == "none":
                delete_mode = input("\nEnter delete mode (none | oldest | manual): \n").strip().lower()

            if delete_mode in ["oldest", "manual"]:
                delete_duplicates(duplicates, dry_run, delete_mode)
        else:
            print("No duplicates found.\n")

    # print(f"Found {len(files)} files.")
    # for file in files[:10]:
    #     print(file)


def main():
    app()


if __name__ == "__main__":
    main()
