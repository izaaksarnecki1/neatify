import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")


def setup_logger(verbose: bool = False, log_dir: Path | str = LOG_DIR) -> None:
    level = logging.DEBUG if verbose else logging.INFO

    log_path = Path(log_dir).expanduser()
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / f"neatify-{datetime.now().strftime('%Y%m%dT%H%M%S')}.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
