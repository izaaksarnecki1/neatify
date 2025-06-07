import logging
import datetime


def setup_logger(verbose: bool = False, log_file: str = "logs/neatify"):
    level = logging.DEBUG if verbose else logging.INFO
    log_file += "-" + str(datetime.datetime.now()) + ".log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
