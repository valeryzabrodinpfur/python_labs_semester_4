from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    id: str
    amount: float
    category: str
    date: str
    currency: Optional[str] = "RUB"   # по умолчанию рубли

    def __post_init__(self):
        # Простейшая нормализация строк
        self.category = self.category.strip()