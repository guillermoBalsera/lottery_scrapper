import logging
from datetime import datetime


def set_logging():
    log_format = '%(levelname)s - %(message)s'

    logging.basicConfig(
        filename=f'{datetime.now().strftime("%Y%m%d%H%M")}.log',
        level=logging.INFO,
        format=log_format
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))

    logging.getLogger().addHandler(console_handler)
