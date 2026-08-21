import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """Set up the logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Создаём абсолютный путь к логам относительно корня проекта
    base_dir = Path(__file__).parent.parent  # src/ -> корень проекта
    log_path = base_dir / log_file  # корень/logs/masks.log

    # Создаём папку, если её нет
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter_file = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter_file)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
