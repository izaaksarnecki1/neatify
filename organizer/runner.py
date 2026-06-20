from pathlib import Path

from config import load_config
from organizer.scanner import Scanner


def run(source: Path | None, dest: Path | None, dry_run: bool) -> None:
    config = load_config()
    if source:
        config["source"] = source
    if dest:
        config["dest"] = dest
    config["dry_run"] = dry_run

    root = Path(config["source"]).expanduser()
    print(f"Scanning files in: {root}")

    files = Scanner(root).scan()

    print(f"Found {len(files)} files.")
    for file in files[:10]:
        print(file)
