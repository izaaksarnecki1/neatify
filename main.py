from cli.interface import app
from pathlib import Path


def run(source: Path, dest: Path, dry_run: bool) -> None:
    # function where main logic will be placed. Called from interface.py
    # print(f"Source: {source}")
    # print(f"Destination: {dest}")
    # print(f"Dry run: {dry_run}")

    pass


def main():
    app()


if __name__ == "__main__":
    main()
