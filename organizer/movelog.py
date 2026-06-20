import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


RUNS_SUBDIR = "runs"


@dataclass
class MoveEntry:
    src: str
    dest: str
    ts: str

    @classmethod
    def from_json(cls, line: str) -> "MoveEntry":
        data = json.loads(line)
        return cls(src=data["src"], dest=data["dest"], ts=data["ts"])


@dataclass
class RunInfo:
    run_id: str
    path: Path
    move_count: int


class MoveLog:
    """Append-only JSONL log of one organize run's successful moves."""

    def __init__(self, log_dir: Path, run_id: str):
        self.run_id = run_id
        self.dir = Path(log_dir).expanduser() / RUNS_SUBDIR
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"{run_id}.jsonl"

    def record(self, src: Path, dest: Path) -> None:
        entry = MoveEntry(
            src=str(src),
            dest=str(dest),
            ts=datetime.now().isoformat(timespec="seconds"),
        )
        with self.path.open("a") as f:
            f.write(json.dumps(entry.__dict__) + "\n")


def list_runs(log_dir: Path) -> list[RunInfo]:
    runs_dir = Path(log_dir).expanduser() / RUNS_SUBDIR
    if not runs_dir.exists():
        return []

    runs: list[RunInfo] = []
    for path in sorted(runs_dir.glob("*.jsonl")):
        with path.open() as f:
            count = sum(1 for _ in f)
        runs.append(RunInfo(run_id=path.stem, path=path, move_count=count))
    return runs


def latest_run(log_dir: Path) -> RunInfo | None:
    runs = list_runs(log_dir)
    return runs[-1] if runs else None


def load_entries(path: Path) -> list[MoveEntry]:
    with Path(path).open() as f:
        return [MoveEntry.from_json(line) for line in f if line.strip()]
