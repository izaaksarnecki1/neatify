from pathlib import Path

import typer

from organizer.runner import run

app = typer.Typer()


@app.command()
def organize(
    source: Path = typer.Option(
        ...,
        "--source",
        "-s",
        help="Path to folder to organize",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    dest: Path = typer.Option(
        Path("~/Organized"),
        "--dest",
        "-d",
        help="Path to destination folder (created if missing)",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Run without applying changes"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Use a verbose logging system"
    ),
    check_duplicates: bool = typer.Option(
        False,
        "--check-duplicates",
        "-cd",
        help="Enable duplicate checking and deletion",
    ),
    delete_mode: str = typer.Option(
        None,
        "--delete-mode",
        "-dm",
        help="How to handle duplicates: clean | manual",
        case_sensitive=False,
    ),
):
    """Organize files from SOURCE into categorized folders in DEST."""
    run(
        source=source.expanduser(),
        dest=dest.expanduser(),
        dry_run=dry_run,
        verbose=verbose,
        check_duplicates=check_duplicates,
        delete_mode=delete_mode,
    )
