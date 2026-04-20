from abc import ABC, abstractmethod
from typing import Iterator
from app.core.models import Transaction

class BaseReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> Iterator[Transaction]:
        """Возвращает итератор (генератор) транзакций."""
        pass