from cli.interface import app
from pathlib import Path
from organizer.scanner import Scanner
from config import load_config


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
    files = scanner.scan()

    print(f"Found {len(files)} files.")
    for file in files[:10]:
        print(file)


def main():
    app()


if __name__ == "__main__":
    main()
