import logging
import shutil
from pathlib import Path

from organizer.movelog import MoveEntry, load_entries


def undo_run(log_path: Path, dry_run: bool) -> dict:
    """Reverse the moves recorded in a single run log.

    Walks entries in reverse so files that were renamed via the
    `_get_unique_destination` collision suffix don't trip over each other.
    """
    entries = load_entries(log_path)
    stats = {"restored": 0, "missing": 0, "blocked": 0, "failed": 0}

    for entry in reversed(entries):
        result = _undo_one(entry, dry_run)
        stats[result] += 1

    logging.info("\n Undo summary:")
    logging.info(f"  -> Restored: {stats['restored']}")
    logging.info(f"  -> Missing (dest gone): {stats['missing']}")
    logging.info(f"  -> Blocked (src reoccupied): {stats['blocked']}")
    logging.info(f"  -> Failed: {stats['failed']}")
    return stats


def _undo_one(entry: MoveEntry, dry_run: bool) -> str:
    src = Path(entry.src)
    dest = Path(entry.dest)

    if not dest.exists():
        logging.warning(f"[SKIP] Dest no longer exists: {dest}")
        return "missing"

    if src.exists():
        logging.warning(
            f"[SKIP] Original path is occupied, refusing to overwrite: {src}"
        )
        return "blocked"

    if dry_run:
        logging.info(f"[DRY-RUN] Would restore {dest} -> {src}")
        return "restored"

    try:
        src.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dest), str(src))
        logging.info(f"[RESTORED] {dest} -> {src}")
        return "restored"
    except Exception as e:
        logging.error(f"Failed to restore {dest} -> {src}: {e}")
        return "failed"
