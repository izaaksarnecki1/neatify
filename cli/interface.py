import typer
from pathlib import Path

app = typer.Typer()


def validate_path(path: str) -> Path:
    expanded = Path(path).expanduser()
    if not expanded.exists():
        raise typer.BadParameter(f"Path doesn't exist: {expanded}")
    return expanded


# We use app.command to register a function as a CLI command
@app.command()
def organize(
    source: str = typer.Option(
        ..., "--source", "-s", help="Path to folder to organize"
    ),
    dest: str = typer.Option(
        "~/Organized", "--dest", "-d", help="Path to destination folder"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Run without applying changes"
    ),
    check_duplicates: bool = typer.Option(
        False, "--check-duplicates", "-cd", help="Enable duplicate checking and deletion"
    ),
    delete_mode: str = typer.Option(
        "none", "--delete-mode", "-dm", help="How to handle duplicates: none | oldest | manual",
        case_sensitive=False
    )

):
    """
    Organize files from SOURCE into categorized folders in DEST
    """
    source_path = validate_path(source)
    dest_path = Path(dest).expanduser()

    from main import run

    run(source_path, dest_path, dry_run, delete_mode, check_duplicates)