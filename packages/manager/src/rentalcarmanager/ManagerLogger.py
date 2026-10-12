from __future__ import annotations
from logging import Logger, FileHandler, Formatter
from pathlib import Path

from .types import LogLevel


class RentalLogger(Logger):
    def __init__(self, name: str, filepath: Path | str = Path("./rental.log"), level: LogLevel = "DEBUG") -> None:
        super().__init__(name, level)

        handler: FileHandler = FileHandler(str(filepath))
        self.addHandler(handler)

        handler.setFormatter(
            Formatter("{asctime} - {levelname} - {name} - ({filename}@{lineno}): {message}", style="{"))
