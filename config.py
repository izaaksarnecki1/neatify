import yaml
from pathlib import Path


def load_config(path="config.yaml"):
    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")

    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config
