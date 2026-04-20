import json
from pathlib import Path
from typing import Iterator
import logging
from app.core.models import Transaction
from app.core.exceptions import DataFormatError
from app.io.base_reader import BaseReader


logger = logging.getLogger(__name__)


class JSONReader(BaseReader):
    def read(self, file_path: str) -> Iterator[Transaction]:
        path = Path(file_path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise DataFormatError(
                f"Невалидный JSON в файле {file_path}: {e}"
            ) from e
        except OSError as e:
            raise DataFormatError(
                f"Ошибка доступа к файлу {file_path}: {e}"
            ) from e

        if not isinstance(data, list):
            raise DataFormatError(
                f"JSON файл {file_path} должен содержать массив объектов"
            )

        for idx, item in enumerate(data):
            try:
                required = {'id', 'amount', 'category', 'date'}
                if not all(k in item for k in required):
                    missing = [k for k in required if k not in item]
                    raise DataFormatError(
                        f"Объект #{idx} не содержит полей: {missing}"
                    )
                yield Transaction(
                    id=str(item['id']).strip(),
                    amount=float(item['amount']),
                    category=str(item['category']).strip(),
                    date=str(item['date']).strip(),
                    currency=str(item.get('currency', 'RUB')).strip()
                )
            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Пропущен объект #{idx} в {file_path}: {e}"
                )
                continue
