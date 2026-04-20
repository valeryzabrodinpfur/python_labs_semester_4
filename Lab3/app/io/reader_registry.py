from typing import Dict, Type
from app.io.base_reader import BaseReader
from app.io.csv_reader import CSVReader
from app.io.json_reader import JSONReader


class ReaderRegistry:
    """Реестр обработчиков по расширению файла (Registry Pattern)."""
    _readers: Dict[str, Type[BaseReader]] = {
        '.csv': CSVReader,
        '.json': JSONReader,
    }

    @classmethod
    def get_reader(cls, extension: str) -> Type[BaseReader]:
        ext = extension.lower()
        if ext not in cls._readers:
            raise ValueError(f"Нет зарегистрированного обработчика для расширения '{ext}'")
        return cls._readers[ext]

    @classmethod
    def register(cls, extension: str, reader_class: Type[BaseReader]):
        cls._readers[extension.lower()] = reader_class