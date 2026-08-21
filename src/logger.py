import logging

def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """Set up the logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter_file = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    formatter_console = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File Handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter_file)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger