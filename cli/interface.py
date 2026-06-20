from pathlib import Path

import typer

from organizer.movelog import latest_run, list_runs
from organizer.runner import run
from organizer.undo import undo_run
from utils.logger import LOG_DIR, setup_logger

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
    ignore: list[str] = typer.Option(
        None,
        "--ignore",
        "-i",
        help="Extra glob pattern to ignore (repeatable). Adds to config 'ignore.patterns'.",
    ),
    include_hidden: bool = typer.Option(
        False,
        "--include-hidden",
        help="Don't skip dotfiles/dotdirs (overrides the default hidden-file filter).",
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
        extra_ignore=ignore,
        include_hidden=include_hidden,
    )


@app.command()
def undo(
    run_id: str = typer.Option(
        None, "--run", "-r", help="Run ID to undo (defaults to the most recent run)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print what would be restored without moving anything"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbose logging"
    ),
):
    """Reverse the moves recorded by a previous organize run."""
    setup_logger(verbose=verbose)

    if run_id:
        target = LOG_DIR.expanduser() / "runs" / f"{run_id}.jsonl"
        if not target.exists():
            raise typer.BadParameter(f"No log found for run {run_id} at {target}")
    else:
        latest = latest_run(LOG_DIR)
        if latest is None:
            typer.echo("No runs to undo.")
            raise typer.Exit(code=1)
        target = latest.path
        run_id = latest.run_id

    typer.echo(f"Undoing run {run_id} ({target})")
    undo_run(target, dry_run=dry_run)


@app.command()
def history():
    """List past organize runs that can be undone."""
    runs = list_runs(LOG_DIR)
    if not runs:
        typer.echo("No runs recorded yet.")
        return
    for info in runs:
        typer.echo(f"{info.run_id}  {info.move_count} move(s)  {info.path}")
