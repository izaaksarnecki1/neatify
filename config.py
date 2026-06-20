import yaml
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config(path: Path | str | None = None) -> dict:
    path = Path(path).expanduser() if path else DEFAULT_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)
