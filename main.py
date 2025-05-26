from cli.interface import app
from pathlib import Path
from organizer.scanner import Scanner
from config import load_config
from organizer.duplicates import find_duplicates, prompt_delete_mode, delete_duplicates

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
        print(f"Checking for duplicate files in: {source}\n")

        scanner = Scanner(source)
        files = scanner.scan()
        
        duplicates = find_duplicates(files)

        if duplicates:
            print("Found duplicate files:")
            for group in duplicates:
                print("\n - Duplicate set:")
                for file in group:
                    print(f"{file.path}")
            if delete_mode is None:
                delete_mode = delete_mode = prompt_delete_mode()

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
