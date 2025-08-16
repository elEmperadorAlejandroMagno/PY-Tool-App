from abc import ABC, abstractmethod
from collections.abc import Callable
import os

class FileTranslatorInterface(ABC):
    def __init__(self) -> None:
        # map of file suffix to handler function
        self.suffixes_enable: dict[str, Callable[..., str]] = {}

    @abstractmethod
    def translate_file(self, file_path: str, entry_lang: str, output_lang: str) -> str:
        """Translate a file located at file_path using specified languages."""
        raise NotImplementedError

    @staticmethod
    def validate_path(path: str) -> None:
        if not os.path.isfile(path):
            raise ValueError("Invalid file path provided.")

