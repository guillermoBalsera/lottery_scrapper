import logging
from datetime import datetime
from pathlib import Path


def set_logging():
    log_format = '%(levelname)s - %(message)s'

    Path(f"./logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=f'./logs/{datetime.now().strftime("%Y%m%d%H%M%S")}.log',
        level=logging.INFO,
        format=log_format
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))

    logging.getLogger().addHandler(console_handler)
