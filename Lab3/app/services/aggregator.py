from typing import Iterator, Dict
from app.core.models import Transaction

def aggregate_stream(transactions: Iterator[Transaction]) -> Dict[str, float]:
    """Агрегирует транзакции по категориям, потребляя итератор."""
    result: Dict[str, float] = {}
    for tx in transactions:
        result[tx.category] = result.get(tx.category, 0.0) + tx.amount
    return result